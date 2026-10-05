"""End-to-end test of the running API with a fixed set of student feedback.

For every test case it POSTs the feedback, compares the returned sentiment and
topics with the expected values, then checks that GET /api/feedback and
GET /api/analytics agree with what was stored. Results are printed and written
as a Markdown table for the report.

Usage (from the backend folder, with the API running):
    python -m scripts.run_test_cases                       # local API
    python -m scripts.run_test_cases --base-url http://136.115.200.121
"""

import argparse
import json
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

# (student id, text, expected sentiment, expected topics)
# "mixed" cases praise one thing and criticise another; they are expected neutral.
TEST_CASES = [
    ("student_001", "The lectures were excellent and very practical.", "positive", ["lectures"]),
    ("student_002", "The assignments were too difficult.", "negative", ["assignments"]),
    ("student_003", "The course material was useful.", "positive", ["course material"]),
    ("student_004", "The laboratory sessions were boring.", "negative", ["laboratory"]),
    ("student_005", "The professor explained the concepts clearly.", "positive", ["professor"]),
    ("student_006", "The exams were fair and well organized.", "positive", ["exams"]),
    ("student_007", "The group project was a great way to apply what we learned.", "positive", ["projects"]),
    ("student_008", "The workload this semester was overwhelming and stressful.", "negative", ["workload"]),
    ("student_009", "The lectures were interesting, but the exams were far too hard.", "neutral", ["lectures", "exams"]),
    ("student_010", "The slides for each lecture were uploaded on Monday.", "neutral", ["course material"]),
    ("student_011", "Profesori i shpjegoi konceptet shumë qartë.", "positive", ["professor"]),
    ("student_012", "Detyrat ishin shumë të vështira dhe shumë të gjata.", "negative", ["assignments"]),
    ("student_013", "Laboratori ishte i mërzitshëm.", "negative", ["laboratory"]),
    ("student_014", "Materialet e kursit ishin shumë të dobishme.", "positive", ["course material"]),
    ("student_015", "Provimi ishte i drejtë, por ligjëratat ishin të mërzitshme.", "neutral", ["exams", "lectures"]),
]

# Input that must be rejected by validation (HTTP 422)
INVALID_CASES = [
    ("Real name as ID", {"anonymous_student_id": "Bujar Bushi", "feedback_text": "The lectures were great."}),
    ("Text too short", {"anonymous_student_id": "student_099", "feedback_text": "Good"}),
    ("Missing text", {"anonymous_student_id": "student_099"}),
]


def call(base_url: str, method: str, path: str, payload: dict | None = None) -> tuple[int, dict]:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        base_url.rstrip("/") + path, data=data, method=method, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.status, json.loads(response.read())
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b"{}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--output", default="../docs/testing/test_results.md")
    args = parser.parse_args()

    rows, passed = [], 0
    print(f"Running {len(TEST_CASES)} feedback test cases against {args.base_url}\n")
    for i, (student, text, expected_sentiment, expected_topics) in enumerate(TEST_CASES, 1):
        status, body = call(args.base_url, "POST", "/api/feedback", {"anonymous_student_id": student, "feedback_text": text})
        stored = status == 201 and body.get("status") == "analyzed"
        sentiment_ok = body.get("sentiment") == expected_sentiment
        topics = body.get("topics", [])
        topics_ok = all(t in topics for t in expected_topics)
        ok = stored and sentiment_ok and topics_ok
        passed += ok
        rows.append({
            "n": i, "text": text, "lang": body.get("language", "–"), "provider": body.get("nlp_provider", "–"),
            "expected": expected_sentiment, "actual": body.get("sentiment", "–"),
            "score": body.get("sentiment_score"), "expected_topics": expected_topics, "topics": topics,
            "result": "PASS" if ok else "FAIL",
        })
        print(f"{i:>2}. {'PASS' if ok else 'FAIL'}  {body.get('sentiment', '-'):<8} {body.get('sentiment_score', 0):+.2f}  "
              f"{', '.join(topics):<35} | {text[:55]}")

    validation_rows = []
    for name, payload in INVALID_CASES:
        status, _ = call(args.base_url, "POST", "/api/feedback", payload)
        validation_rows.append((name, status, "PASS" if status == 422 else "FAIL"))
        print(f"    {'PASS' if status == 422 else 'FAIL'}  validation: {name} -> HTTP {status}")

    # Consistency: analytics must match the documents actually stored
    _, listing = call(args.base_url, "GET", "/api/feedback?limit=200")
    _, analytics = call(args.base_url, "GET", "/api/analytics?top_n=50")
    items = listing["items"]
    stored_counts = Counter(f["sentiment"] for f in items if f["status"] == "analyzed")
    stored_topics = Counter(t for f in items if f["status"] == "analyzed" for t in f["topics"])
    checks = [
        ("Total feedback = documents in database", analytics["total_feedback"] == len(items)),
        ("Sentiment counts match database", all(analytics["sentiment_counts"][s] == stored_counts[s] for s in ("positive", "neutral", "negative"))),
        ("Percentages sum to ~100%", abs(sum(analytics["sentiment_distribution"].values()) - 100) <= 0.2 if analytics["analyzed"] else True),
        ("Topic frequencies match database", {t["topic"]: t["count"] for t in analytics["top_topics"]} == dict(stored_topics)),
    ]
    print()
    for name, ok in checks:
        print(f"    {'PASS' if ok else 'FAIL'}  {name}")

    total = len(TEST_CASES)
    print(f"\nFeedback cases: {passed}/{total} passed ({100 * passed / total:.0f}%)")
    print(f"Analytics: {analytics['sentiment_distribution']}  top topics: "
          f"{[(t['topic'], t['count']) for t in analytics['top_topics'][:5]]}")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Test results – AI Student Feedback System",
        "",
        f"Run: {datetime.now():%Y-%m-%d %H:%M} · API: `{args.base_url}`",
        "",
        f"## Feedback analysis ({passed}/{total} passed)",
        "",
        "| # | Feedback | Lang | Provider | Expected | Actual | Score | Expected topics | Detected topics | Result |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        score = f"{r['score']:+.2f}" if r["score"] is not None else "–"
        lines.append(
            f"| {r['n']} | {r['text']} | {r['lang']} | {r['provider']} | {r['expected']} | {r['actual']} | {score} | "
            f"{', '.join(r['expected_topics'])} | {', '.join(r['topics'])} | {r['result']} |"
        )
    lines += ["", "## Input validation", "", "| Case | HTTP status | Result |", "|---|---|---|"]
    lines += [f"| {name} | {status} | {result} |" for name, status, result in validation_rows]
    lines += ["", "## Dashboard consistency", "", "| Check | Result |", "|---|---|"]
    lines += [f"| {name} | {'PASS' if ok else 'FAIL'} |" for name, ok in checks]
    lines += [
        "",
        "## Analytics snapshot",
        "",
        "```json",
        json.dumps({k: analytics[k] for k in ("total_feedback", "sentiment_counts", "sentiment_distribution", "top_topics")}, indent=2),
        "```",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out.resolve()}")


if __name__ == "__main__":
    main()
