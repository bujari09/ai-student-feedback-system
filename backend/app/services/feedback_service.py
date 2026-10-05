import logging

from google.cloud import firestore

from app.database import get_feedback_collection
from app.models.feedback import new_feedback_document
from app.schemas.feedback import FeedbackCreate, FeedbackOut

logger = logging.getLogger(__name__)


def _to_schema(doc_id: str, data: dict) -> FeedbackOut:
    return FeedbackOut(id=doc_id, **data)


def create_feedback(payload: FeedbackCreate) -> FeedbackOut:
    """Store a new feedback document with status 'pending'.

    NLP analysis is added in Phase 6; until then documents stay pending.
    """
    data = new_feedback_document(payload.anonymous_student_id, payload.feedback_text)
    doc_ref = get_feedback_collection().document()
    doc_ref.set(data)
    logger.info("Stored feedback %s from %s", doc_ref.id, payload.anonymous_student_id)
    return _to_schema(doc_ref.id, data)


def list_feedback(limit: int = 50) -> list[FeedbackOut]:
    query = (
        get_feedback_collection()
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )
    return [_to_schema(doc.id, doc.to_dict()) for doc in query.stream()]
