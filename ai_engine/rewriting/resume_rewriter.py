"""Module for rewriting resume content using LLM (Groq API)."""

import os
import re
import sys
import json
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from groq import Groq
from app.core.config import settings
from app.core.utils import extract_bullets


def load_rewrite_prompt() -> str:
    """Load the rewrite prompt template."""
    prompt_path = os.path.join(
        os.path.dirname(__file__),
        '..', 'prompts', 'rewrite_prompt.txt'
    )
    
    if os.path.exists(prompt_path):
        with open(prompt_path, 'r') as f:
            return f.read()
    
    # Fallback prompt if file doesn't exist
    return """You are an expert resume writer specializing in ATS optimization.

Your task: Rewrite resume bullet points to better match the job description while maintaining accuracy.

Requirements:
1. Use keywords from the job description naturally
2. Emphasize relevant accomplishments and metrics
3. Keep bullets concise (max 1-2 lines)
4. Focus on impact and results
5. Maintain professional tone
6. Do NOT fabricate experience or skills not in the original resume
7. Return ONLY valid JSON with no markdown formatting

Input format: JSON with "bullets" array and "job_description"
Output format: JSON with "rewritten_bullets" array where each has "original" and "rewritten" fields"""


def rewrite_resume(resume_text: str, job_description: str, model) -> tuple[str, list[dict]]:
    """
    Rewrite resume bullets using Groq API to match job description.
    
    Args:
        resume_text: Original resume text
        job_description: Target job description
        model: SBERT model (unused but kept for interface compatibility)
        
    Returns:
        Tuple of (optimized_full_text, list_of_diffs)
        where each diff is {"original": str, "rewritten": str}
    """
    
    # Initialize Groq client
    client = Groq(api_key=settings.GROQ_API_KEY)
    
    # Extract bullets from resume
    bullets = extract_bullets(resume_text)
    
    if not bullets:
        # No bullets found, return as-is
        return resume_text, []
    
    # Load rewrite prompt
    system_prompt = load_rewrite_prompt()
    
    # Build user message
    user_message = f"""Job Description:
{job_description}

Resume Bullets to Rewrite (up to 15):
{json.dumps(bullets[:15], indent=2)}

Please rewrite these bullets to better align with the job description. Return ONLY valid JSON."""
    
    try:
        # Call Groq API (mixtral is free and very powerful)
        response = client.chat.completions.create(
            model=settings.MODEL_NAME,
            max_tokens=settings.MAX_TOKENS,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )
        
        # Parse response
        response_text = response.choices[0].message.content
        
        # Extract JSON from response (handle both array and object formats)
        json_match = re.search(r'[\[\{].*[\]\}]', response_text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            # Handle both array and object responses
            if isinstance(result, list):
                rewritten = result
            else:
                rewritten = result.get("rewritten_bullets", [])
        else:
            raise ValueError("Could not parse JSON response from Claude")
        
        # Build diff list
        diff_list = []
        for i, original_bullet in enumerate(bullets[:len(rewritten)]):
            rewritten_item = rewritten[i] if i < len(rewritten) else {}
            if isinstance(rewritten_item, dict):
                diff_list.append({
                    "original": original_bullet,
                    "rewritten": rewritten_item.get("rewritten", original_bullet)
                })
            else:
                diff_list.append({
                    "original": original_bullet,
                    "rewritten": str(rewritten_item)
                })
        
        # Reconstruct optimized resume text by replacing bullets
        optimized_text = resume_text
        for diff in diff_list:
            if diff["original"] in optimized_text:
                # Replace bullet points in original text
                optimized_text = optimized_text.replace(
                    diff["original"],
                    diff["rewritten"],
                    1  # Replace only first occurrence
                )
        
        return optimized_text, diff_list
        
    except Exception as e:
        # On error, return original with empty diff
        print(f"Warning: Rewrite failed: {e}")
        return resume_text, [
            {"original": bullet, "rewritten": bullet} for bullet in bullets
        ]


def _build_rewrite_prompt_with_context(resume_text: str, job_description: str) -> str:
    """
    Build a detailed prompt for resume rewriting.
    
    Args:
        resume_text: Original resume
        job_description: Job description
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an ATS-optimized resume writer.

Job Description:
---
{job_description}
---

Original Resume Excerpt:
---
{resume_text[:2000]}
---

Please rewrite the resume bullets to incorporate keywords from the job description while maintaining accuracy."""
    
    return prompt
