"""
Dedicated keyword scoring module for the Dynamic Resume Tailoring Engine.

Implements a mathematical scoring function that computes the percentage of
job-description keywords present in a resume — providing transparent proof
that the AI-optimized resume improved keyword coverage over the original.
"""

import re
from collections import Counter


# ── Stop-words ────────────────────────────────────────────────────────────────
# Extended English stop-word list; intentionally broad to keep only
# meaningful/technical terms in the keyword sets.
_STOP_WORDS: frozenset[str] = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "need",
    "dare", "ought", "used", "not", "no", "nor", "so", "yet", "both",
    "either", "neither", "each", "every", "all", "any", "few", "more",
    "most", "other", "some", "such", "than", "too", "very", "just",
    "because", "if", "while", "although", "though", "since", "until",
    "unless", "during", "about", "against", "between", "into", "through",
    "above", "below", "this", "that", "these", "those", "their", "they",
    "them", "we", "our", "you", "your", "he", "she", "it", "its", "his",
    "her", "who", "what", "which", "when", "where", "how", "why",
    "also", "much", "many", "work", "role", "team", "position", "job",
    "company", "years", "year", "plus", "like", "make", "well", "must",
    "will", "able", "want", "good", "get", "use", "using", "experience",
    "strong", "excellent", "understanding", "knowledge", "ability",
    "including", "related", "following", "provide", "support", "ensure",
    "manage", "help", "new", "own", "high", "time", "etc", "within",
})

# Minimum character length for a token to be considered a keyword.
_MIN_KEYWORD_LEN = 3


# ── Internal helpers ──────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """
    Lower-case and split text into alpha-numeric tokens of at least
    _MIN_KEYWORD_LEN characters, removing stop-words.
    """
    tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#./]*\b", text)
    return [
        t.lower()
        for t in tokens
        if len(t) >= _MIN_KEYWORD_LEN and t.lower() not in _STOP_WORDS
    ]


def _extract_jd_keywords(jd_text: str) -> dict[str, int]:
    """
    Extract keywords from a job description weighted by frequency.

    Returns a mapping of  keyword → frequency  for all tokens that appear at
    least once.  Higher-frequency tokens represent more important requirements.
    """
    tokens = _tokenize(jd_text)
    return dict(Counter(tokens))


def _normalize_for_lookup(text: str) -> set[str]:
    """Return the set of de-duplicated keyword tokens present in *text*."""
    return set(_tokenize(text))


# ── Public API ────────────────────────────────────────────────────────────────

def score_keyword_match(
    resume_text: str,
    jd_text: str,
    *,
    top_n: int = 40,
) -> dict:
    """
    Compute a mathematical keyword-match score between a resume and a job
    description.

    The score is defined as:

        score = (matched_weighted / total_weighted) × 100

    where *weighted* means each JD keyword is counted proportionally to its
    frequency in the JD (more-mentioned requirements count more).

    Args:
        resume_text: Plain text of the resume.
        jd_text:     Plain text of the job description.
        top_n:       Maximum number of JD keywords to consider (highest TF).

    Returns:
        A dict with the following keys:
            score            float  – keyword match percentage 0–100
            matched_count    int    – number of unique JD keywords found
            total_count      int    – total unique JD keywords considered
            matched_keywords list   – sorted list of matched keyword strings
            missing_keywords list   – sorted list of missing keyword strings
    """
    jd_keyword_freq = _extract_jd_keywords(jd_text)

    if not jd_keyword_freq:
        return {
            "score": 0.0,
            "matched_count": 0,
            "total_count": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    # Take the top-N most frequent JD keywords for a manageable, meaningful set.
    sorted_jd_keywords = sorted(
        jd_keyword_freq.items(), key=lambda kv: kv[1], reverse=True
    )[:top_n]

    resume_tokens = _normalize_for_lookup(resume_text)

    matched_weighted = 0.0
    total_weighted = 0.0
    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword, freq in sorted_jd_keywords:
        total_weighted += freq
        if keyword in resume_tokens:
            matched_weighted += freq
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = (matched_weighted / total_weighted * 100) if total_weighted > 0 else 0.0
    score = round(min(100.0, max(0.0, score)), 1)

    return {
        "score": score,
        "matched_count": len(matched_keywords),
        "total_count": len(sorted_jd_keywords),
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
    }
