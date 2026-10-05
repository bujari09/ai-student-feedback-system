from fastapi import APIRouter, Query, status

from app.schemas.feedback import FeedbackCreate, FeedbackList, FeedbackOut
from app.services import feedback_service

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackOut, status_code=status.HTTP_201_CREATED)
def create_feedback(payload: FeedbackCreate) -> FeedbackOut:
    return feedback_service.create_feedback(payload)


@router.get("", response_model=FeedbackList)
def list_feedback(limit: int = Query(50, ge=1, le=200)) -> FeedbackList:
    items = feedback_service.list_feedback(limit)
    return FeedbackList(count=len(items), items=items)
