import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.models.request_models import SkillGap
from typing import List
import re

# Master skill list (curated top skills)
MASTER_SKILLS = {
    "languages": ["Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R", "MATLAB", "SQL"],
    "frameworks": ["React", "Vue", "Angular", "FastAPI", "Django", "Flask", "Spring Boot", "ASP.NET", "Express", "Next.js", "NestJS"],
    "cloud": ["AWS", "Google Cloud", "Azure", "Docker", "Kubernetes", "Terraform", "CloudFormation", "Lambda", "EC2", "S3"],
    "data": ["SQL", "MongoDB", "PostgreSQL", "MySQL", "Redis", "Cassandra", "Elasticsearch", "Firebase", "DynamoDB"],
    "ml": ["TensorFlow", "PyTorch", "scikit-learn", "Keras", "NLP", "Computer Vision", "Deep Learning", "Machine Learning"],
    "tools": ["Git", "GitHub", "GitLab", "CI/CD", "Jenkins", "Docker", "Linux", "Nginx", "Apache", "Jira"],
    "other": ["REST API", "GraphQL", "Microservices", "Agile", "Scrum", "DevOps", "Testing", "AWS", "GCP"]
}

def flatten_skills(skills_dict: dict) -> List[str]:
    """Flatten skill dictionary to list."""
    return [skill for category in skills_dict.values() for skill in category]

ALL_SKILLS = flatten_skills(MASTER_SKILLS)

async def detect_gaps(resume_text: str, job_description: str) -> List[SkillGap]:
    """
    Detect missing skills from JD vs resume.
    Returns prioritized list of missing skills.
    """
    try:
        # Extract skills from both texts
        jd_skills = extract_skills(job_description)
        resume_skills = extract_skills(resume_text)
        
        # Find missing
        missing = list(set(jd_skills) - set(resume_skills))
        
        # Prioritize by frequency in JD
        skill_gaps = []
        for skill in missing:
            frequency = job_description.lower().count(skill.lower())
            required = "required" in job_description.lower() or "must have" in job_description.lower()
            
            if frequency >= 3 or required:
                priority = "High"
            elif frequency == 2:
                priority = "Medium"
            else:
                priority = "Low"
            
            skill_gaps.append(SkillGap(skill=skill, priority=priority))
        
        # Sort by priority
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        skill_gaps.sort(key=lambda x: priority_order[x.priority])
        
        return skill_gaps[:10]  # Top 10 missing skills
    
    except Exception as e:
        return []

def extract_skills(text: str) -> List[str]:
    """Extract known skills from text."""
    text_lower = text.lower()
    found_skills = []
    
    for skill in ALL_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills
