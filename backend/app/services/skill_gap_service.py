import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ai_engine.extraction.skill_extractor import extract_skills
from app.models.request_models import SkillGap


def detect_gaps(resume_text: str, job_description: str) -> list[SkillGap]:
    """
    Compare skills in JD vs resume and return missing skills with priority.

    Priority logic:
        High   → skill appears 3+ times in JD OR in 'required' section
        Medium → skill appears 2 times
        Low    → skill appears once
    """
    jd_skills     = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)

    # Extract skill names from the dicts returned by extract_skills
    resume_skills_names = {skill_dict["skill"] for skill_dict in resume_skills if isinstance(skill_dict, dict)}
    resume_skills_lower = {s.lower() for s in resume_skills_names}

    gaps: list[SkillGap] = []
    seen = set()

    for skill_info in jd_skills:
        if not isinstance(skill_info, dict):
            continue
        skill_name = skill_info.get("skill", "")
        if not skill_name:
            continue
        if skill_name.lower() in resume_skills_lower:
            continue
        if skill_name.lower() in seen:
            continue
        seen.add(skill_name.lower())

        count = skill_info.get("count", 1)
        in_required = skill_info.get("in_required", False)

        if count >= 3 or in_required:
            priority = "High"
        elif count == 2:
            priority = "Medium"
        else:
            priority = "Low"

        gaps.append(SkillGap(skill=skill_name, priority=priority))

    # Sort: High → Medium → Low
    order = {"High": 0, "Medium": 1, "Low": 2}
    gaps.sort(key=lambda x: order[x.priority])

    return gaps[:15]  # cap at 15 for UI clarity