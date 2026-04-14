import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import anthropic
import json
import logging
from app.models.request_models import DiffItem
from typing import Tuple, List
from app.core.config import settings
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def build_rewrite_prompt(resume_text: str, job_description: str) -> str:
    """Build the Claude prompt for resume rewriting."""
    return f"""You are an expert resume optimizer specializing in ATS optimization.

TASK: Rewrite the resume bullets to align better with the job description while preserving all factual accuracy.

CRITICAL RULES:
1. NEVER invent skills, tools, or experience the candidate doesn't have
2. ONLY rephrase existing content using stronger language
3. Use action verbs (Developed, Engineered, Optimized, Architected, Designed, Built)
4. Match keywords and terminology from the job description
5. Include metrics and quantifiable impact where available
6. Keep each bullet concise (1-2 lines max)
7. Preserve all dates, company names, and role titles exactly

JOB DESCRIPTION:
{job_description}

ORIGINAL RESUME:
{resume_text}

OUTPUT FORMAT:
Return a JSON array with this exact structure (NO additional text):
[
  {{"original": "original bullet text", "rewritten": "improved bullet text"}},
  ...
]

IMPORTANT: Return ONLY the JSON array. No markdown, no explanations."""

async def rewrite_resume(resume_text: str, job_description: str, model=None) -> Tuple[str, List[DiffItem]]:
    """
    Rewrite resume using Claude API.
    Returns (optimized_resume_text, diff_list)
    """
    try:
        if not settings.ANTHROPIC_API_KEY:
            logger.error("ANTHROPIC_API_KEY not set")
            return resume_text, []
        
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        
        # Build prompt
        prompt = build_rewrite_prompt(resume_text, job_description)
        
        # Call Claude
        logger.info("Calling Claude API for resume rewriting...")
        response = client.messages.create(
            model=settings.MODEL_NAME,
            max_tokens=settings.MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        response_text = response.content[0].text
        logger.info(f"Raw response: {response_text[:200]}")
        
        # Parse JSON response
        try:
            # Clean the response (remove markdown code blocks if present)
            cleaned = response_text.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            
            diff_data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Response was: {response_text}")
            return resume_text, []
        
        # Build diff and optimized text
        optimized = resume_text
        diff_list = []
        
        for item in diff_data:
            original = item.get("original", "")
            rewritten = item.get("rewritten", "")
            
            if original and rewritten and original in optimized:
                diff_list.append(DiffItem(
                    original=original,
                    optimized=rewritten,
                    changed=original != rewritten
                ))
                optimized = optimized.replace(original, rewritten, 1)
        
        return optimized, diff_list
    
    except anthropic.APIError as e:
        logger.error(f"Claude API error: {e}")
        return resume_text, []
    except Exception as e:
        logger.error(f"Unexpected error in rewrite_resume: {e}")
        return resume_text, []
