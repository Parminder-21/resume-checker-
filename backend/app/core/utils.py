import re
from typing import List

def normalize_score(raw_value: float, min_val: float = 0.2, max_val: float = 0.9) -> float:
    """Normalize cosine similarity to 0-100 scale with floor at 10."""
    normalized = (raw_value - min_val) / (max_val - min_val)
    score = max(10.0, min(100.0, normalized * 100))
    return round(score, 1)

def extract_sections(text: str) -> dict:
    """Extract sections from resume text."""
    sections = {
        "skills": "",
        "experience": "",
        "education": "",
        "summary": ""
    }
    
    lines = text.split('\n')
    current_section = None
    
    section_keywords = {
        "skills": ["skills", "technical skills", "core competencies"],
        "experience": ["experience", "work experience", "professional experience"],
        "education": ["education", "degrees", "certifications"],
        "summary": ["summary", "objective", "professional summary"]
    }
    
    for line in lines:
        lower_line = line.lower().strip()
        for section, keywords in section_keywords.items():
            if any(kw in lower_line for kw in keywords):
                current_section = section
                break
        
        if current_section and line.strip():
            sections[current_section] += line + "\n"
    
    return sections

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\-,;:()\']', ' ', text)
    return text.strip()
