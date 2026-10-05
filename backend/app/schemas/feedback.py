from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.models.feedback import FeedbackStatus, Sentiment
from app.utils.text import clean_text


class FeedbackCreate(BaseModel):
    anonymous_student_id: str = Field(
        ...,
        pattern=r"^[A-Za-z0-9_-]{3,40}$",
        examples=["student_001"],
        description="Anonymous identifier. Do not use real names.",
    )
    feedback_text: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        examples=["The lectures were very useful and practical."],
    )

    @field_validator("feedback_text", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return clean_text(value) if isinstance(value, str) else value


class FeedbackOut(BaseModel):
    id: str
    anonymous_student_id: str
    feedback_text: str
    language: str | None = None
    sentiment: Sentiment | None = None
    sentiment_score: float | None = None
    sentiment_magnitude: float | None = None
    topics: list[str] = []
    nlp_provider: str | None = None
    status: FeedbackStatus
    error: str | None = None
    created_at: datetime
    analyzed_at: datetime | None = None


class FeedbackList(BaseModel):
    count: int
    items: list[FeedbackOut]
