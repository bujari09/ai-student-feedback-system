import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")


def clean_text(text: str) -> str:
    """Normalize unicode, drop control characters and collapse whitespace."""
    text = unicodedata.normalize("NFC", text)
    text = "".join(ch for ch in text if ch in "\n\t" or unicodedata.category(ch)[0] != "C")
    return _WHITESPACE.sub(" ", text).strip()
