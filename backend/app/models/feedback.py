"""Firestore document model for the `feedback` collection.

Document shape (collection: feedback, document id: auto-generated):

    anonymous_student_id  string           e.g. "student_001" (never a real name)
    feedback_text         string           cleaned input text
    language              string | null    ISO code detected by the NLP API ("en", "sq", ...)
    sentiment             string | null    "positive" | "neutral" | "negative"
    sentiment_score       number | null    -1.0 ... 1.0
    sentiment_magnitude   number | null    strength of emotion (Natural Language API only)
    topics                array<string>    normalized topics, e.g. ["lectures", "assignments"]
    nlp_provider          string | null    "natural_language" | "gemini"
    status                string           "pending" | "analyzed" | "failed"
    error                 string | null    reason when status == "failed"
    created_at            timestamp        UTC
    analyzed_at           timestamp | null UTC
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any


class FeedbackStatus(str, Enum):
    PENDING = "pending"
    ANALYZED = "analyzed"
    FAILED = "failed"


class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


def new_feedback_document(anonymous_student_id: str, feedback_text: str) -> dict[str, Any]:
    """Build the initial document stored before NLP analysis runs."""
    return {
        "anonymous_student_id": anonymous_student_id,
        "feedback_text": feedback_text,
        "language": None,
        "sentiment": None,
        "sentiment_score": None,
        "sentiment_magnitude": None,
        "topics": [],
        "nlp_provider": None,
        "status": FeedbackStatus.PENDING.value,
        "error": None,
        "created_at": datetime.now(timezone.utc),
        "analyzed_at": None,
    }
