import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ai_engine.embedding.semantic_match import compute_similarity
from ai_engine.extraction.section_detector import detect_sections
from ai_engine.scoring.keyword_scorer import score_keyword_match
from app.models.request_models import ScoreBreakdown

logger = logging.getLogger(__name__)

# ── Scoring weights ───────────────────────────────────────────────────────────
# keyword_coverage gets the largest single weight because it is a direct,
# transparent measure of how many JD terms appear in the resume — meaning
# AI-added keywords are immediately visible in the score delta.
_W_SKILLS   = 0.35   # semantic match on skills section
_W_EXP      = 0.25   # semantic match on experience section
_W_KEYWORD  = 0.40   # mathematical keyword coverage (most sensitive to rewrites)


def compute_scores(resume_text: str, job_description: str, model) -> ScoreBreakdown:
    """
    Compute a 4-part ATS score breakdown.

    Weights:
        skills_match       → 35%  (SBERT semantic similarity on skills section)
        experience_match   → 25%  (SBERT semantic similarity on experience section)
        keyword_coverage   → 40%  (mathematical keyword overlap — most sensitive)

    This weighting ensures that AI-added keywords are clearly reflected in the
    overall score delta between the original and optimized resume.
    """
    sections = detect_sections(resume_text)

    skills_text     = sections.get("skills",     "") or resume_text
    experience_text = sections.get("experience", "") or resume_text

    logger.debug(f"Skills section length: {len(skills_text)} chars")
    logger.debug(f"Experience section length: {len(experience_text)} chars")

    # Semantic section-level similarities via SBERT
    skills_score     = compute_similarity(skills_text,     job_description, model)
    experience_score = compute_similarity(experience_text, job_description, model)

    # Mathematical keyword scoring (transparent, reproducible)
    kw_result = score_keyword_match(resume_text, job_description)
    keyword_score = kw_result["score"]

    # Weighted overall score
    overall = round(
        (skills_score     * _W_SKILLS) +
        (experience_score * _W_EXP)    +
        (keyword_score    * _W_KEYWORD),
        1
    )

    logger.info(
        f"Scores → skills={skills_score}% exp={experience_score}% "
        f"kw={keyword_score}% overall={overall}%"
    )

    return ScoreBreakdown(
        overall=overall,
        skills_match=skills_score,
        experience_match=experience_score,
        keyword_coverage=keyword_score,
        formatting="ATS Safe",
        matched_keywords=kw_result["matched_keywords"],
        missing_keywords=kw_result["missing_keywords"],
        keyword_matched_count=kw_result["matched_count"],
        keyword_total_count=kw_result["total_count"],
    )