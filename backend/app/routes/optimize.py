from fastapi import APIRouter, HTTPException, Request
from app.models.request_models import OptimizeRequest, OptimizeResponse, ScorePair
from app.services import scoring_service, skill_gap_service, rewriter_service
from app.core.utils import hash_text
import logging

router  = APIRouter()
logger  = logging.getLogger(__name__)

# Simple in-memory cache: hash(resume+jd) → OptimizeResponse
_cache: dict = {}


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize_resume(data: OptimizeRequest, request: Request):
    """
    Core pipeline endpoint.

    Steps:
        1. Score original resume vs JD
        2. Detect skill gaps
        3. Rewrite bullets with LLM (Claude)
        4. Re-score optimized resume
        5. Build diff
        6. Return full response
    """
    model = request.app.state.sbert_model

    # Cache check (useful for repeated demo runs)
    cache_key = hash_text(data.resume_text + data.job_description)
    if cache_key in _cache:
        logger.info("Cache hit — returning cached result")
        return _cache[cache_key]

    try:
        # ── Step 1: Score original ────────────────────────────────────────────
        logger.info("Computing initial ATS score...")
        initial_scores = scoring_service.compute_scores(
            data.resume_text,
            data.job_description,
            model
        )

        # ── Step 2: Detect skill gaps ─────────────────────────────────────────
        logger.info("Detecting skill gaps...")
        skill_gaps = skill_gap_service.detect_gaps(
            data.resume_text,
            data.job_description
        )

        # ── Step 3: Rewrite resume with LLM ───────────────────────────────────
        logger.info("Rewriting resume with AI...")
        optimized_text, diff_items = rewriter_service.rewrite_and_diff(
            data.resume_text,
            data.job_description,
            model
        )

        # ── Step 4: Re-score optimized resume ─────────────────────────────────
        logger.info("Computing optimized ATS score...")
        optimized_scores = scoring_service.compute_scores(
            optimized_text,
            data.job_description,
            model
        )

        # ── Step 5: Build response ─────────────────────────────────────────────
        response = OptimizeResponse(
            status="success",
            scores=ScorePair(
                initial=initial_scores,
                optimized=optimized_scores
            ),
            skill_gaps=skill_gaps,
            optimized_resume=optimized_text,
            diff=diff_items
        )

        # Cache and return
        _cache[cache_key] = response
        logger.info(
            f"Optimization complete. Score: {initial_scores.overall}% → {optimized_scores.overall}%"
        )
        return response

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Optimization failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Optimization failed: {str(e)}. Please try again."
        )