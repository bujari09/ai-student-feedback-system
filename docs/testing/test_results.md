# Test results – AI Student Feedback System

Run: 2026-10-05 16:29 · API: `http://127.0.0.1:8000`

## Feedback analysis (15/15 passed)

| # | Feedback | Lang | Provider | Expected | Actual | Score | Expected topics | Detected topics | Result |
|---|---|---|---|---|---|---|---|---|---|
| 1 | The lectures were excellent and very practical. | en | natural_language | positive | positive | +0.93 | lectures | lectures | PASS |
| 2 | The assignments were too difficult. | en | natural_language | negative | negative | -0.92 | assignments | assignments | PASS |
| 3 | The course material was useful. | en | natural_language | positive | positive | +0.96 | course material | course material | PASS |
| 4 | The laboratory sessions were boring. | en | natural_language | negative | negative | -0.92 | laboratory | laboratory | PASS |
| 5 | The professor explained the concepts clearly. | en | natural_language | positive | positive | +0.93 | professor | professor | PASS |
| 6 | The exams were fair and well organized. | en | natural_language | positive | positive | +0.95 | exams | exams | PASS |
| 7 | The group project was a great way to apply what we learned. | en | natural_language | positive | positive | +0.93 | projects | projects | PASS |
| 8 | The workload this semester was overwhelming and stressful. | en | natural_language | negative | negative | -0.92 | workload | workload | PASS |
| 9 | The lectures were interesting, but the exams were far too hard. | en | natural_language | neutral | neutral | -0.01 | lectures, exams | exams, lectures | PASS |
| 10 | The slides for each lecture were uploaded on Monday. | en | natural_language | neutral | neutral | +0.02 | course material | lectures, course material | PASS |
| 11 | Profesori i shpjegoi konceptet shumë qartë. | sq | gemini | positive | positive | +1.00 | professor | professor | PASS |
| 12 | Detyrat ishin shumë të vështira dhe shumë të gjata. | sq | gemini | negative | negative | -0.80 | assignments | assignments, workload | PASS |
| 13 | Laboratori ishte i mërzitshëm. | sq | gemini | negative | negative | -0.70 | laboratory | laboratory | PASS |
| 14 | Materialet e kursit ishin shumë të dobishme. | sq | gemini | positive | positive | +0.80 | course material | course material | PASS |
| 15 | Provimi ishte i drejtë, por ligjëratat ishin të mërzitshme. | sq | gemini | neutral | neutral | +0.00 | exams, lectures | exams, lectures | PASS |

## Input validation

| Case | HTTP status | Result |
|---|---|---|
| Real name as ID | 422 | PASS |
| Text too short | 422 | PASS |
| Missing text | 422 | PASS |

## Dashboard consistency

| Check | Result |
|---|---|
| Total feedback = documents in database | PASS |
| Sentiment counts match database | PASS |
| Percentages sum to ~100% | PASS |
| Topic frequencies match database | PASS |

## Analytics snapshot

```json
{
  "total_feedback": 15,
  "sentiment_counts": {
    "positive": 7,
    "neutral": 3,
    "negative": 5
  },
  "sentiment_distribution": {
    "positive": 46.7,
    "neutral": 20.0,
    "negative": 33.3
  },
  "top_topics": [
    {
      "topic": "lectures",
      "count": 4,
      "sentiment": {
        "positive": 1,
        "neutral": 3,
        "negative": 0
      }
    },
    {
      "topic": "exams",
      "count": 3,
      "sentiment": {
        "positive": 1,
        "neutral": 2,
        "negative": 0
      }
    },
    {
      "topic": "course material",
      "count": 3,
      "sentiment": {
        "positive": 2,
        "neutral": 1,
        "negative": 0
      }
    },
    {
      "topic": "professor",
      "count": 2,
      "sentiment": {
        "positive": 2,
        "neutral": 0,
        "negative": 0
      }
    },
    {
      "topic": "laboratory",
      "count": 2,
      "sentiment": {
        "positive": 0,
        "neutral": 0,
        "negative": 2
      }
    },
    {
      "topic": "assignments",
      "count": 2,
      "sentiment": {
        "positive": 0,
        "neutral": 0,
        "negative": 2
      }
    },
    {
      "topic": "workload",
      "count": 2,
      "sentiment": {
        "positive": 0,
        "neutral": 0,
        "negative": 2
      }
    },
    {
      "topic": "projects",
      "count": 1,
      "sentiment": {
        "positive": 1,
        "neutral": 0,
        "negative": 0
      }
    }
  ]
}
```
