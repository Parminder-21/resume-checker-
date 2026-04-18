"""
Dedicated keyword scoring module for the Dynamic Resume Tailoring Engine.

Implements a mathematical scoring function that computes the percentage of
job-description keywords present in a resume — providing transparent proof
that the AI-optimized resume improved keyword coverage over the original.

Supports both exact and stem-based matching so that morphological variants
(e.g. "develop" / "developing" / "development") are correctly credited.
"""

import re
from collections import Counter


# ── Stop-words ────────────────────────────────────────────────────────────────
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

_MIN_KEYWORD_LEN = 3


# ── Simple stemmer (porter-style prefix truncation) ───────────────────────────

def _stem(word: str) -> str:
    """
    Lightweight, dependency-free stemmer that strips common English suffixes.
    Good enough to match "developing" → "develop", "managed" → "manag", etc.
    """
    w = word.lower()
    for suffix in ("ational", "tional", "enci", "anci", "izer", "iser",
                   "alism", "ation", "ator", "alism", "aliti", "ousli",
                   "entli", "ibili", "ness", "ment", "tion", "sion",
                   "ing", "ied", "ies", "ied", "ers", "ess", "ful",
                   "ous", "ive", "ize", "ise", "ate", "ble", "ed",
                   "er", "ly", "al", "ic", "es", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) >= 3:
            w = w[: len(w) - len(suffix)]
            break
    return w


# ── Internal helpers ──────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """Lower-case and split text into meaningful tokens, removing stop-words."""
    tokens = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#./]*\b", text)
    return [
        t.lower()
        for t in tokens
        if len(t) >= _MIN_KEYWORD_LEN and t.lower() not in _STOP_WORDS
    ]


def _extract_jd_keywords(jd_text: str) -> dict[str, int]:
    """Extract keywords from a job description weighted by frequency."""
    tokens = _tokenize(jd_text)
    return dict(Counter(tokens))


def _token_set(text: str) -> set[str]:
    """Return the set of unique keyword tokens present in *text*."""
    return set(_tokenize(text))


def _stem_set(tokens: set[str]) -> set[str]:
    """Return a set of stemmed versions of tokens for fuzzy matching."""
    return {_stem(t) for t in tokens}


# ── Public API ────────────────────────────────────────────────────────────────

def score_keyword_match(
    resume_text: str,
    jd_text: str,
    *,
    top_n: int = 50,
    stem_weight: float = 0.75,
) -> dict:
    """
    Compute a mathematical keyword-match score between a resume and a JD.

    Scoring formula:
        For each JD keyword (up to top_n by frequency):
          - +freq  if keyword found exactly in resume
          - +freq * stem_weight  if stemmed form found (partial credit)

        score = matched_weighted / total_weighted × 100

    Args:
        resume_text:  Plain text of the resume.
        jd_text:      Plain text of the job description.
        top_n:        Maximum number of JD keywords to consider.
        stem_weight:  Fractional credit for stem-only matches (default 0.75).

    Returns:
        dict with keys: score, matched_count, total_count,
                        matched_keywords, missing_keywords
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

    # Take the top-N most frequent JD keywords
    sorted_jd_keywords = sorted(
        jd_keyword_freq.items(), key=lambda kv: kv[1], reverse=True
    )[:top_n]

    resume_tokens = _token_set(resume_text)
    resume_stems  = _stem_set(resume_tokens)

    matched_weighted = 0.0
    total_weighted   = 0.0
    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword, freq in sorted_jd_keywords:
        total_weighted += freq

        if keyword in resume_tokens:
            # Exact match
            matched_weighted += freq
            matched_keywords.append(keyword)
        elif _stem(keyword) in resume_stems:
            # Stem match — partial credit
            matched_weighted += freq * stem_weight
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = (matched_weighted / total_weighted * 100) if total_weighted > 0 else 0.0
    score = round(min(100.0, max(0.0, score)), 1)

    return {
        "score": score,
        "matched_count": len(matched_keywords),
        "total_count":   len(sorted_jd_keywords),
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
    }
