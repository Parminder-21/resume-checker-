import re
import hashlib


def clean_text(text: str) -> str:
    """Remove excessive whitespace and non-printable characters."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 8000) -> str:
    """Truncate text to max_chars, keeping complete sentences."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    return truncated


def hash_text(text: str) -> str:
    """SHA256 hash for caching keys."""
    return hashlib.sha256(text.encode()).hexdigest()


def normalize_score(raw: float, min_val: float = 0.2, max_val: float = 0.9, floor: float = 10.0) -> float:
    """
    Normalize cosine similarity [min_val, max_val] → [0, 100].
    Cosine scores between unrelated texts rarely go below 0.2.
    """
    normalized = (raw - min_val) / (max_val - min_val)
    score = max(floor, min(100.0, normalized * 100))
    return round(score, 1)


def extract_bullets(text: str) -> list[str]:
    """
    Extract bullet-point lines from resume text.
    Looks for lines starting with -, •, *, or numbered lists.
    """
    lines = text.split('\n')
    bullets = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^[-•*●◦▪]\s+', stripped):
            bullet = re.sub(r'^[-•*●◦▪]\s+', '', stripped)
            if len(bullet) > 20:
                bullets.append(bullet)
        elif re.match(r'^\d+\.\s+', stripped) and len(stripped) > 25:
            bullet = re.sub(r'^\d+\.\s+', '', stripped)
            bullets.append(bullet)
    return bullets


def split_into_sentences(text: str) -> list[str]:
    """Simple sentence splitter for resume text."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 15]