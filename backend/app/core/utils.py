import re
import hashlib


def clean_text(text: str) -> str:
    """Remove excessive horizontal whitespace but PRESERVE newlines."""
    # Only collapse horizontal whitespace (spaces, tabs, etc. NOT newlines)
    text = re.sub(r'[ \t\r\f\v]+', ' ', text)
    # Remove non-printable characters except space and newline
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    return text.strip()


def truncate_text(text: str, max_chars: int = 8000) -> str:
    """Truncate text to max_chars, keeping complete sentences."""
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.8:
        return truncated[:last_period + 1]
    return truncated


def hash_text(text: str) -> str:
    """SHA256 hash for caching keys."""
    return hashlib.sha256(text.encode()).hexdigest()


def normalize_score(raw: float, min_val: float = 0.2, max_val: float = 0.9, floor: float = 10.0) -> float:
    """
    Normalize cosine similarity [min_val, max_val] → [0, 100].
    Cosine scores between unrelated texts rarely go below 0.2.
    """
    normalized = (raw - min_val) / (max_val - min_val)
    score = max(floor, min(100.0, normalized * 100))
    return round(score, 1)


def extract_bullets(text: str) -> list[str]:
    """
    Extract bullet-point lines from resume text.
    Looks for lines starting with -, •, *, or numbered lists.
    Also extracts short lines under sections like "Skills" or "Experience".
    """
    import logging
    logger = logging.getLogger(__name__)
    
    lines = text.split('\n')
    bullets = []
    in_section = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines and short lines
        if not stripped or len(stripped) < 10:
            in_section = False
            continue
        
        # Check if this is a section header
        if any(keyword in stripped.lower() for keyword in ['experience', 'skills', 'project', 'achievement', 'responsibility', 'education']):
            in_section = True
            logger.debug(f"Found section: {stripped[:30]}")
            continue
        
        # Extract formatted bullets (-, •, *, etc. added comprehensive set)
        if re.match(r'^[-•*●◦▪▸►✓✔◆■□▶→]\s+', stripped):
            bullet = re.sub(r'^[-•*●◦▪▸►✓✔◆■□▶→]\s+', '', stripped)
            if len(bullet) > 15:  # Lowered from 20 to catch more content
                bullets.append(bullet)
                logger.debug(f"✓ Found bullet ({len(bullet)} chars): {bullet[:60]}")
        elif re.match(r'^\d+[.):]\s+', stripped) and len(stripped) > 20:
            bullet = re.sub(r'^\d+[.):]\s+', '', stripped)
            bullets.append(bullet)
            logger.debug(f"✓ Found numbered bullet ({len(bullet)} chars): {bullet[:60]}")
        # Extract content lines that look like bullet points (indented or in sections)
        elif in_section and len(stripped) > 25 and not re.match(r'^[A-Z]{2,}', stripped):
            # This line is likely content in an experience/skills section
            if not any(stripped.endswith(x) for x in [':', ',', ';']):
                bullets.append(stripped)
                logger.debug(f"✓ Found section content ({len(stripped)} chars): {stripped[:60]}")
    
    # If no bullets found, try to extract meaningful lines as fallback
    if not bullets:
        logger.warning("⚠️ No bullets found with standard patterns, trying fallback")
        for line in lines:
            stripped = line.strip()
            if 30 < len(stripped) < 200 and not re.match(r'^[A-Z\s]{10,}$', stripped):
                bullets.append(stripped)
                logger.debug(f"✓ Fallback bullet ({len(stripped)} chars): {stripped[:60]}")
    
    logger.info(f"📊 Extracted {len(bullets)} bullets total")
    return bullets


def split_into_sentences(text: str) -> list[str]:
    """Simple sentence splitter for resume text."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 15]