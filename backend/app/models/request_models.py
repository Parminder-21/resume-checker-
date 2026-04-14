from pydantic import BaseModel
from typing import List, Literal

class ScoreBreakdown(BaseModel):
    overall: float
    skills_match: float
    experience_match: float
    keyword_coverage: float
    formatting: str = "ATS Safe"

class SkillGap(BaseModel):
    skill: str
    priority: Literal["High", "Medium", "Low"]

class DiffItem(BaseModel):
    original: str
    optimized: str
    changed: bool = True

class ResumeInput(BaseModel):
    resume_text: str
    job_description: str

class OptimizeResponse(BaseModel):
    status: str = "success"
    scores: dict
    skill_gaps: List[SkillGap]
    optimized_resume: str
    diff: List[DiffItem]

class PDFDownloadRequest(BaseModel):
    optimized_resume: str

class UploadResponse(BaseModel):
    status: str = "success"
    resume_text: str
    sections: dict
