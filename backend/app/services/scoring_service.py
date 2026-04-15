import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ai_engine.embedding.semantic_match import compute_similarity, compute_keyword_overlap
from ai_engine.extraction.section_detector import detect_sections
from app.models.request_models import ScoreBreakdown


def compute_scores(resume_text: str, job_description: str, model) -> ScoreBreakdown:
    """
    Compute a 4-part ATS score breakdown.

    Weights:
        skills_match       → 50%
        experience_match   → 30%
        keyword_coverage   → 20%
    """
    sections = detect_sections(resume_text)

    skills_text     = sections.get("skills", "") or resume_text
    experience_text = sections.get("experience", "") or resume_text

    # Compute section-level similarities
    skills_score     = compute_similarity(skills_text, job_description, model)
    experience_score = compute_similarity(experience_text, job_description, model)
    keyword_score    = compute_keyword_overlap(resume_text, job_description)

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
        formatting="ATS Safe"
    )