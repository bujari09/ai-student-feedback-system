from app.config import get_settings
from app.models.feedback import Sentiment


def label_for_score(score: float) -> Sentiment:
    """Map a sentiment score (-1..1) to positive / neutral / negative.

    Scores close to zero are neutral; mixed feedback ("good lectures, hard exams")
    also lands near zero, which is why it is treated as neutral.
    """
    settings = get_settings()
    if score >= settings.sentiment_positive_threshold:
        return Sentiment.POSITIVE
    if score <= settings.sentiment_negative_threshold:
        return Sentiment.NEGATIVE
    return Sentiment.NEUTRAL
