"""Normalize raw topics (NLP entities or Gemini labels) into dashboard topics.

Topics are not limited to a fixed list: known academic topics are mapped to one
canonical label (so "lecture", "lectures" and "ligjëratat" count together), and
any other topic is kept in a cleaned, singular form.
"""

import re
import unicodedata

MAX_TOPICS = 5

# canonical label -> English synonyms (exact words or phrases)
_SYNONYMS: dict[str, set[str]] = {
    "lectures": {"lecture", "lectures", "class", "classes", "lesson", "lessons", "lecture content"},
    "assignments": {"assignment", "assignments", "homework", "homeworks", "task", "tasks", "exercise", "exercises"},
    "exams": {"exam", "exams", "test", "tests", "midterm", "midterms", "final exam", "quiz", "quizzes"},
    "professor": {"professor", "professors", "teacher", "teachers", "lecturer", "lecturers", "instructor", "instructors"},
    "laboratory": {"laboratory", "laboratories", "lab", "labs", "lab session", "lab sessions", "laboratory session", "laboratory sessions"},
    "course material": {"course material", "course materials", "material", "materials", "slides", "textbook", "resources", "course content"},
    "projects": {"project", "projects", "group project", "group projects"},
    "workload": {"workload", "work load"},
    "grading": {"grade", "grades", "grading", "marks"},
}

# Albanian word stems -> canonical label, used when raw topics are Albanian words
_ALBANIAN_STEMS: dict[str, str] = {
    "ligjerat": "lectures",
    "leksion": "lectures",
    "detyr": "assignments",
    "provim": "exams",
    "profesor": "professor",
    "mesimdhen": "professor",
    "laborator": "laboratory",
    "material": "course material",
    "projekt": "projects",
    "vleresim": "grading",
}

# Generic words that entity analysis returns but that are not useful topics
_GENERIC = {"way", "thing", "lot", "bit", "time", "concept", "idea", "part", "day", "week", "semester", "course"}

_LOOKUP = {synonym: label for label, synonyms in _SYNONYMS.items() for synonym in synonyms}
_NON_WORD = re.compile(r"[^\w\s-]")


def _strip_accents(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn")


def _clean(topic: str) -> str:
    topic = _NON_WORD.sub(" ", topic.lower())
    return " ".join(topic.split())


def _singular(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def normalize_topic(raw: str) -> str | None:
    topic = _clean(raw)
    if len(topic) < 2 or topic.isdigit():
        return None

    if topic in _LOOKUP:
        return _LOOKUP[topic]

    ascii_topic = _strip_accents(topic)
    for stem, label in _ALBANIAN_STEMS.items():
        if any(word.startswith(stem) for word in ascii_topic.split()):
            return label

    words = [_singular(word) for word in topic.split()]
    singular = " ".join(words)
    if singular in _LOOKUP:
        return _LOOKUP[singular]
    if words[-1] in _LOOKUP:  # e.g. "weekly lectures" -> "lectures"
        return _LOOKUP[words[-1]]
    if singular in _GENERIC:
        return None
    return singular


def normalize_topics(raw_topics: list[str]) -> list[str]:
    topics: list[str] = []
    for raw in raw_topics:
        topic = normalize_topic(raw)
        if topic and topic not in topics:
            topics.append(topic)
    return topics[:MAX_TOPICS]
