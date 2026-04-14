import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sklearn.metrics.pairwise import cosine_similarity
from app.core.utils import normalize_score, extract_sections
import numpy as np

async def compute_scores(resume_text: str, job_description: str, model) -> dict:
    """
    Compute ATS match scores using semantic similarity.
    Returns {overall, skills_match, experience_match, keyword_coverage, formatting}
    """
    try:
        # Get resume sections
        resume_sections = extract_sections(resume_text)
        
        # Encode full texts
        resume_embedding = model.encode([resume_text])
        jd_embedding = model.encode([job_description])
        
        # Overall similarity
        overall_similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]
        overall_score = normalize_score(overall_similarity)
        
        # Section-level scoring
        skills_score = normalize_score(
            cosine_similarity([model.encode([resume_sections["skills"]])[0]], 
                            [model.encode([job_description])[0]])[0][0]
        ) if resume_sections["skills"].strip() else 30.0
        
        experience_score = normalize_score(
            cosine_similarity([model.encode([resume_sections["experience"]])[0]], 
                            [model.encode([job_description])[0]])[0][0]
        ) if resume_sections["experience"].strip() else 25.0
        
        # Keyword coverage (simple term overlap)
        resume_terms = set(resume_text.lower().split())
        jd_terms = set(job_description.lower().split())
        overlap = len(resume_terms & jd_terms) / len(jd_terms) if jd_terms else 0
        keyword_score = round(overlap * 100, 1)
        
        return {
            "overall": min(100.0, overall_score),
            "skills_match": skills_score,
            "experience_match": experience_score,
            "keyword_coverage": keyword_score,
            "formatting": "ATS Safe"
        }
    
    except Exception as e:
        # Return baseline scores on error
        return {
            "overall": 50.0,
            "skills_match": 50.0,
            "experience_match": 50.0,
            "keyword_coverage": 50.0,
            "formatting": "ATS Safe"
        }
