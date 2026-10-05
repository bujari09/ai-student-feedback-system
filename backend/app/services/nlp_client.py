"""Calls to the Google Cloud NLP services.

Strategy:
1. Cloud Natural Language API v2 `analyzeSentiment` runs for every text. It also
   detects the language.
2. If the language is officially supported for entity analysis, `analyzeEntities`
   provides the raw topics.
3. Otherwise (e.g. Albanian), Gemini on Vertex AI returns a sentiment score and
   English topic labels as structured JSON, so topics from all languages group
   together on the dashboard. If Gemini fails, the Natural Language sentiment is kept.
"""

import logging
from dataclasses import dataclass, field
from functools import lru_cache

from google import genai
from google.cloud import language_v2
from google.genai import types
from pydantic import BaseModel, Field

from app.config import get_settings

logger = logging.getLogger(__name__)

PROVIDER_NATURAL_LANGUAGE = "natural_language"
PROVIDER_GEMINI = "gemini"

# Entity types that are never topics.
_IGNORED_ENTITY_TYPES = {
    language_v2.Entity.Type.PHONE_NUMBER,
    language_v2.Entity.Type.ADDRESS,
    language_v2.Entity.Type.DATE,
    language_v2.Entity.Type.NUMBER,
    language_v2.Entity.Type.PRICE,
}

_GEMINI_PROMPT = (
    "You analyze student feedback about a university course.\n"
    "Return:\n"
    "- language: ISO 639-1 code of the feedback\n"
    "- sentiment_score: from -1.0 (very negative) to 1.0 (very positive); 0 for neutral or mixed\n"
    "- topics: 1 to 4 short topics that the feedback explicitly mentions, in English, lowercase, "
    "e.g. 'lectures', 'assignments', 'exams', 'professor', 'laboratory', 'course material', "
    "'projects', 'workload'. Do not infer topics that are not mentioned. "
    "Never include people's names.\n\n"
    "Feedback:\n"
)


class _GeminiAnalysis(BaseModel):
    language: str
    sentiment_score: float = Field(ge=-1.0, le=1.0)
    topics: list[str]


@dataclass
class NLPResult:
    language: str
    score: float
    magnitude: float | None
    raw_topics: list[str] = field(default_factory=list)
    provider: str = PROVIDER_NATURAL_LANGUAGE


@lru_cache
def _language_client() -> language_v2.LanguageServiceClient:
    return language_v2.LanguageServiceClient()


@lru_cache
def _gemini_client() -> genai.Client:
    settings = get_settings()
    return genai.Client(vertexai=True, project=settings.gcp_project_id, location=settings.gemini_location)


def _document(text: str) -> language_v2.Document:
    return language_v2.Document(content=text, type_=language_v2.Document.Type.PLAIN_TEXT)


def _is_topic(entity: language_v2.Entity) -> bool:
    if entity.type_ in _IGNORED_ENTITY_TYPES:
        return False
    if entity.type_ == language_v2.Entity.Type.PERSON:
        # Keep roles such as "professor" (common noun) but never store a person's
        # name (proper noun) as a topic – privacy.
        return all(m.type_ == language_v2.EntityMention.Type.COMMON for m in entity.mentions)
    return True


def _entity_topics(text: str) -> list[str]:
    response = _language_client().analyze_entities(document=_document(text))
    return [entity.name for entity in response.entities if _is_topic(entity)]


def _analyze_with_gemini(text: str) -> _GeminiAnalysis:
    response = _gemini_client().models.generate_content(
        model=get_settings().gemini_model,
        contents=_GEMINI_PROMPT + text,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=_GeminiAnalysis,
            temperature=0,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
        ),
    )
    return response.parsed


def analyze_text(text: str) -> NLPResult:
    sentiment = _language_client().analyze_sentiment(document=_document(text))
    language = sentiment.language_code or "und"
    result = NLPResult(
        language=language,
        score=sentiment.document_sentiment.score,
        magnitude=sentiment.document_sentiment.magnitude,
    )

    if language in get_settings().nl_supported_language_list:
        result.raw_topics = _entity_topics(text)
        return result

    try:
        gemini = _analyze_with_gemini(text)
        return NLPResult(
            language=gemini.language or language,
            score=gemini.sentiment_score,
            magnitude=None,
            raw_topics=gemini.topics,
            provider=PROVIDER_GEMINI,
        )
    except Exception:
        logger.exception("Gemini analysis failed; keeping Natural Language sentiment without topics")
        return result
