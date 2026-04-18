import os
import re
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx2pdf import convert
import logging

logger = logging.getLogger(__name__)

def _clean_text(text: str) -> str:
    """Sanitize text for Word documents."""
    if not text:
        return ""
    # Standard cleanup for Word
    text = text.replace('\r', '')
    return text.strip()

def generate_pdf(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> str:
    """
    Generate a professional resume using python-docx and convert to PDF.
    
    Returns:
        The path to the generated file (might be .docx if conversion fails).
    """
    # 1. Create Word Document
    docx_path = output_path.replace('.pdf', '.docx')
    doc = Document()
    
    # Set Narrow Margins (Standard for resumes)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Styling Candidate Name (Header)
    header_name = doc.add_paragraph()
    header_name.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = header_name.add_run(candidate_name.upper())
    run.font.size = Pt(20)
    run.font.bold = True
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor(17, 34, 68) # Navy

    # Add a horizontal rule (border) after header
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(12)
    
    # Process text into sections and bullets
    headers = [
        'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'SUMMARY',
        'CERTIFICATIONS', 'LANGUAGES', 'TECHNICAL SKILLS', 'ACHIEVEMENTS',
        'PROFESSIONAL SUMMARY', 'WORK EXPERIENCE'
    ]
    
    lines = resume_text.split('\n')
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        # Detect Section Header
        if any(h in stripped.upper() for h in headers) and len(stripped) < 40:
            h_para = doc.add_paragraph()
            h_para.paragraph_format.space_before = Pt(12)
            h_para.paragraph_format.space_after = Pt(6)
            run = h_para.add_run(stripped.upper())
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.name = 'Calibri'
            run.font.color.rgb = RGBColor(17, 34, 68) # Navy
            
        # Detect Bullet Points
        elif stripped.startswith(('-', '*', '•')) or (
            len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.'
        ):
            # Remove bullet char
            content = re.sub(r'^[-•*●◦▪▸►✓✔◆■□▶→\d. ]+', '', stripped).strip()
            if content:
                p = doc.add_paragraph(content, style='List Bullet')
                p.paragraph_format.space_after = Pt(3)
        
        # Standard Body
        else:
            p = doc.add_paragraph(stripped)
            p.paragraph_format.space_after = Pt(6)
            run = p.runs[0] if p.runs else p.add_run()
            run.font.size = Pt(10)
            run.font.name = 'Calibri'

    # Footer
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer.add_run(f"\nOptimized for ATS · {datetime.now().year}")
    run.font.size = Pt(8)
    run.font.italic = True
    run.font.color.rgb = RGBColor(150, 150, 150)

    # Save Word Doc
    doc.save(docx_path)
    logger.info(f"✓ DOCX created at {docx_path}")

    # 2. Try PDF Conversion (Requires MS Word)
    try:
        logger.info(f"⌛ Attempting PDF conversion for {docx_path}...")
        convert(docx_path, output_path)
        logger.info(f"✅ PDF successfully created at {output_path}")
        return output_path # Success
    except Exception as e:
        logger.warning(f"⚠️ PDF conversion failed (Likely MS Word missing): {e}")
        # Return the docx path as the fallback
        return docx_path

def generate_docx(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> str:
    """Wrapper for legacy calls."""
    return generate_pdf(resume_text, output_path, candidate_name)
