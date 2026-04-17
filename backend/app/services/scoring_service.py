import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ai_engine.embedding.semantic_match import compute_similarity
from ai_engine.extraction.section_detector import detect_sections
from ai_engine.scoring.keyword_scorer import score_keyword_match
from app.models.request_models import ScoreBreakdown


def compute_scores(resume_text: str, job_description: str, model) -> ScoreBreakdown:
    """
    Compute a 4-part ATS score breakdown.

    Weights:
        skills_match       → 50%
        experience_match   → 30%
        keyword_coverage   → 20%

    keyword_coverage is computed by the dedicated mathematical keyword scorer,
    which returns the weighted percentage of JD keywords present in the resume
    along with the matched/missing keyword lists for transparent reporting.
    """
    sections = detect_sections(resume_text)

    skills_text     = sections.get("skills", "") or resume_text
    experience_text = sections.get("experience", "") or resume_text

    # Semantic section-level similarities
    skills_score     = compute_similarity(skills_text, job_description, model)
    experience_score = compute_similarity(experience_text, job_description, model)

    # Dedicated mathematical keyword scoring
    kw_result = score_keyword_match(resume_text, job_description)
    keyword_score = kw_result["score"]

    # Weighted overall
    overall = round(
        (skills_score * 0.50) +
        (experience_score * 0.30) +
        (keyword_score * 0.20),
        1
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