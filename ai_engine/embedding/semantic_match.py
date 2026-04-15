# AI Engine - Embedding module
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re


def compute_similarity(text_a: str, text_b: str, model) -> float:
    """
    Compute semantic similarity between two texts using SBERT.
    Returns score 0-100.
    """
    try:
        emb_a = model.encode([text_a])
        emb_b = model.encode([text_b])
        raw = cosine_similarity(emb_a, emb_b)[0][0]
        
        # Normalize from [0.2, 0.9] range to [0, 100]
        normalized = (raw - 0.2) / (0.9 - 0.2)
        score = max(10.0, min(100.0, normalized * 100))
        return round(score, 1)
    except Exception:
        return 50.0


def compute_keyword_overlap(resume_text: str, job_description: str) -> float:
    """
    Compute keyword overlap between resume and job description.
    Extracts keywords (words 4+ chars) and calculates overlap percentage.
    Returns score 0-100.
    """
    try:
        # Extract keywords (words of 4+ characters, case-insensitive)
        def extract_keywords(text: str) -> set:
            words = re.findall(r'\b\w+\b', text.lower())
            # Filter: 4+ chars, exclude common words
            common = {'the', 'this', 'that', 'with', 'from', 'have', 'which', 'your',
                     'their', 'been', 'were', 'also', 'more', 'used', 'such', 'them'}
            return {w for w in words if len(w) >= 4 and w not in common}
        
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)
        
        if not jd_keywords:
            return 10.0
        
        # Calculate overlap
        overlap = len(resume_keywords & jd_keywords)
        coverage = overlap / len(jd_keywords)
        
        # Normalize to 0-100 scale
        score = max(10.0, min(100.0, coverage * 100))
        return round(score, 1)
    
    except Exception:
        return 50.0
