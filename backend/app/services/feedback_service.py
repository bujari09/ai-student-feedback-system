import logging
from datetime import datetime, timezone

from google.cloud import firestore

from app.database import get_feedback_collection
from app.models.feedback import FeedbackStatus, new_feedback_document
from app.schemas.feedback import FeedbackCreate, FeedbackOut
from app.services import nlp_client
from app.services.sentiment_service import label_for_score
from app.services.topic_service import normalize_topics

logger = logging.getLogger(__name__)


def _to_schema(doc_id: str, data: dict) -> FeedbackOut:
    return FeedbackOut(id=doc_id, **data)


def _analyze(text: str) -> dict:
    """Run the NLP pipeline and return the fields to store on the document."""
    try:
        result = nlp_client.analyze_text(text)
    except Exception as exc:
        logger.exception("NLP analysis failed")
        return {
            "status": FeedbackStatus.FAILED.value,
            "error": f"{type(exc).__name__}: {exc}"[:300],
            "analyzed_at": datetime.now(timezone.utc),
        }

    return {
        "language": result.language,
        "sentiment": label_for_score(result.score).value,
        "sentiment_score": round(result.score, 3),
        "sentiment_magnitude": round(result.magnitude, 3) if result.magnitude is not None else None,
        "topics": normalize_topics(result.raw_topics),
        "nlp_provider": result.provider,
        "status": FeedbackStatus.ANALYZED.value,
        "error": None,
        "analyzed_at": datetime.now(timezone.utc),
    }


def create_feedback(payload: FeedbackCreate) -> FeedbackOut:
    """Store the feedback, analyze it, then store the analysis on the same document.

    The document is saved as 'pending' first, so the feedback is never lost even
    if the NLP services are unavailable; it is then marked 'analyzed' or 'failed'.
    """
    data = new_feedback_document(payload.anonymous_student_id, payload.feedback_text)
    doc_ref = get_feedback_collection().document()
    doc_ref.set(data)
    logger.info("Stored feedback %s from %s", doc_ref.id, payload.anonymous_student_id)

    analysis = _analyze(payload.feedback_text)
    doc_ref.update(analysis)
    data.update(analysis)
    logger.info("Feedback %s -> %s (%s)", doc_ref.id, data["status"], data.get("sentiment"))
    return _to_schema(doc_ref.id, data)


def reanalyze_pending(limit: int = 100) -> int:
    """Analyze documents left 'pending' or 'failed' (e.g. after an NLP outage)."""
    query = (
        get_feedback_collection()
        .where(filter=firestore.FieldFilter("status", "in", [FeedbackStatus.PENDING.value, FeedbackStatus.FAILED.value]))
        .limit(limit)
    )
    count = 0
    for doc in query.stream():
        doc.reference.update(_analyze(doc.to_dict()["feedback_text"]))
        count += 1
    return count


def list_feedback(limit: int = 50) -> list[FeedbackOut]:
    query = (
        get_feedback_collection()
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    return [_to_schema(doc.id, doc.to_dict()) for doc in query.stream()]
