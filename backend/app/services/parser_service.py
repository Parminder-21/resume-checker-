import pdfplumber
import io
from typing import Tuple
from app.core.utils import extract_sections, clean_text

async def parse_pdf(file_content: bytes) -> Tuple[str, dict]:
    """
    Extract text and sections from PDF resume.
    
    Returns: (full_text, sections_dict)
    """
    try:
        pdf_file = io.BytesIO(file_content)
        text_content = ""
        
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text_content += page.extract_text() or ""
        
        if not text_content.strip():
            raise ValueError("No text extracted from PDF")
        
        # Extract sections
        sections = extract_sections(text_content)
        
        return text_content, sections
    
    except Exception as e:
        raise Exception(f"PDF parsing error: {str(e)}")
