from fastapi import APIRouter, Depends, HTTPException, Request
from app.models.request_models import ResumeInput, OptimizeResponse
from app.services import (
    scoring_service, skill_gap_service,
    rewriter_service
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_resume(data: ResumeInput, request: Request):
    """
    Core endpoint: Optimize resume for job description.
    Returns scores, skill gaps, optimized resume, and diffs.
    """
    
    try:
        # Validate input
        if not data.resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text is empty")
        if not data.job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is empty")
        
        logger.info("Starting resume optimization...")
        model = request.app.state.sbert_model
        
        # Step 1: Score original resume
        logger.info("Computing initial scores...")
        initial_scores = await scoring_service.compute_scores(
            data.resume_text,
            data.job_description,
            model
        )
        
        # Step 2: Detect skill gaps
        logger.info("Detecting skill gaps...")
        skill_gaps = await skill_gap_service.detect_gaps(
            data.resume_text,
            data.job_description
        )
        
        # Step 3: Rewrite resume with Claude
        logger.info("Rewriting resume with AI...")
        optimized_resume, diff = await rewriter_service.rewrite_resume(
            data.resume_text,
            data.job_description,
            model
        )
        
        # Step 4: Re-score optimized resume
        logger.info("Computing optimized scores...")
        optimized_scores = await scoring_service.compute_scores(
            optimized_resume,
            data.job_description,
            model
        )
        
        logger.info(f"Optimization complete. Initial: {initial_scores['overall']:.1f}% → Optimized: {optimized_scores['overall']:.1f}%")
        
        return OptimizeResponse(
            status="success",
            scores={
                "initial": initial_scores,
                "optimized": optimized_scores
            },
            skill_gaps=skill_gaps,
            optimized_resume=optimized_resume,
            diff=diff
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Optimization error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during optimization: {str(e)}"
        )
