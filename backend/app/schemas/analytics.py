from datetime import date

from pydantic import BaseModel


class SentimentCounts(BaseModel):
    positive: int = 0
    neutral: int = 0
    negative: int = 0


class SentimentDistribution(BaseModel):
    """Percentages of analyzed feedback, rounded to one decimal."""

    positive: float = 0.0
    neutral: float = 0.0
    negative: float = 0.0


class TopicStat(BaseModel):
    topic: str
    count: int
    sentiment: SentimentCounts


class DailyStat(BaseModel):
    date: date
    total: int
    sentiment: SentimentCounts


class Analytics(BaseModel):
    total_feedback: int
    analyzed: int
    pending: int
    failed: int
    sentiment_counts: SentimentCounts
    sentiment_distribution: SentimentDistribution
    average_sentiment_score: float | None
    top_topics: list[TopicStat]
    feedback_over_time: list[DailyStat]
    languages: dict[str, int]
