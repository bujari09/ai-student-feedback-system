"""Dashboard statistics, always computed from the documents in Firestore.

The whole collection is read and aggregated in Python. That is simple and cheap
for an academic dataset (hundreds of documents, well inside the Firestore free
tier). At larger scale this would move to Firestore aggregation queries or
pre-computed counters.
"""

from collections import Counter, defaultdict

from app.database import get_feedback_collection
from app.models.feedback import FeedbackStatus, Sentiment
from app.schemas.analytics import (
    Analytics,
    DailyStat,
    SentimentCounts,
    SentimentDistribution,
    TopicStat,
)

_FIELDS = ["status", "sentiment", "sentiment_score", "topics", "language", "created_at"]


def get_analytics(top_n: int = 10) -> Analytics:
    status_counts: Counter[str] = Counter()
    sentiment_counts: Counter[str] = Counter()
    topic_counts: Counter[str] = Counter()
    topic_sentiment: dict[str, Counter[str]] = defaultdict(Counter)
    daily: dict = defaultdict(Counter)
    languages: Counter[str] = Counter()
    scores: list[float] = []

    for doc in get_feedback_collection().select(_FIELDS).stream():
        data = doc.to_dict()
        status_counts[data.get("status")] += 1
        day = data["created_at"].date()
        daily[day]["total"] += 1

        if data.get("status") != FeedbackStatus.ANALYZED.value:
            continue

        sentiment = data["sentiment"]
        sentiment_counts[sentiment] += 1
        daily[day][sentiment] += 1
        scores.append(data["sentiment_score"])
        if data.get("language"):
            languages[data["language"]] += 1
        for topic in data.get("topics", []):
            topic_counts[topic] += 1
            topic_sentiment[topic][sentiment] += 1

    analyzed = status_counts[FeedbackStatus.ANALYZED.value]

    def percent(label: Sentiment) -> float:
        return round(100 * sentiment_counts[label.value] / analyzed, 1) if analyzed else 0.0

    return Analytics(
        total_feedback=sum(status_counts.values()),
        analyzed=analyzed,
        pending=status_counts[FeedbackStatus.PENDING.value],
        failed=status_counts[FeedbackStatus.FAILED.value],
        sentiment_counts=SentimentCounts(**{s.value: sentiment_counts[s.value] for s in Sentiment}),
        sentiment_distribution=SentimentDistribution(**{s.value: percent(s) for s in Sentiment}),
        average_sentiment_score=round(sum(scores) / len(scores), 3) if scores else None,
        top_topics=[
            TopicStat(
                topic=topic,
                count=count,
                sentiment=SentimentCounts(**{s.value: topic_sentiment[topic][s.value] for s in Sentiment}),
            )
            for topic, count in topic_counts.most_common(top_n)
        ],
        feedback_over_time=[
            DailyStat(
                date=day,
                total=counts["total"],
                sentiment=SentimentCounts(**{s.value: counts[s.value] for s in Sentiment}),
            )
            for day, counts in sorted(daily.items())
        ],
        languages=dict(languages.most_common()),
    )
