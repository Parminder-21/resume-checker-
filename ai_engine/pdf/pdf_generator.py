import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER

def _clean_text(text: str) -> str:
    """Sanitize text for ReportLab to prevent Unicode crashes."""
    if not text: return ""
    replacements = {
        '\u2022': '-', '\u2023': '-', '\u2043': '-',
        '\u2013': '-', '\u2014': '--',
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u00a0': ' ', '\ufb01': 'fi', '\ufb02': 'fl'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode('ascii', 'ignore').decode('ascii')

def generate_pdf(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> None:
    """Generate a premium, ATS-safe PDF with Aggressive Layout Rescue."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.4 * inch, bottomMargin=0.4 * inch,
        leftMargin=0.6 * inch, rightMargin=0.6 * inch
    )
    
    styles = getSampleStyleSheet()
    
    # --- Premium Design ---
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor='#112244', spaceAfter=14, alignment=TA_CENTER, fontName='Helvetica-Bold')
    section_title_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=13, textColor='#112244', spaceAfter=6, spaceBefore=10, fontName='Helvetica-Bold')
    subheading_style = ParagraphStyle('SubHeading', parent=styles['BodyText'], fontSize=11, leading=13, textColor='#000000', spaceAfter=4, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('Body', parent=styles['BodyText'], fontSize=10, leading=13, textColor='#333333', spaceAfter=8, fontName='Helvetica')
    bullet_style = ParagraphStyle('Bullet', parent=styles['BodyText'], fontSize=10, leading=13, leftIndent=15, firstLineIndent=0, spaceAfter=4, textColor='#333333', fontName='Helvetica')

    elements = []
    
    # Header
    elements.append(Paragraph(_clean_text(candidate_name).upper(), title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color='#112244', spaceAfter=10))
    
    # --- Aggressive Layout Rescue ---
    # Injects structure into smushed text chunks
    text = resume_text
    headers = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'SUMMARY', 'CERTIFICATIONS', 'LANGUAGES', 'TECHNICAL SKILLS', 'ACHIEVEMENTS']
    for h in headers:
        text = re.sub(f"(?<!\n\n)(?P<head>{h})", r"\n\n\g<head>", text, flags=re.IGNORECASE)
    
    date_pattern = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2})\s?[\-\–\—\s]\s?(?:Present|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2})"
    text = re.sub(f"(?<!\n\n)(?P<date>{date_pattern})", r"\n\n\g<date>", text)
    text = re.sub(r"(?<!\n)(?P<bull>[•\-\*])", r"\n\g<bull>", text)

    chunks = text.split('\n')
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped: continue
        
        clean = _clean_text(stripped)
        
        # Section Header
        if any(h in clean.upper() for h in headers) and len(clean) < 40:
            if len(elements) > 2: elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(clean.upper(), section_title_style))
            elements.append(HRFlowable(width="30%", thickness=0.5, color='#eeeeee', spaceAfter=4, align=TA_LEFT))
            
        # Date / Subheader
        elif re.search(date_pattern, clean) and len(clean) < 120:
            elements.append(Paragraph(clean, subheading_style))
            
        # Bullets
        elif stripped.startswith(('-', '*', '•')) or (len(stripped) > 0 and stripped[0].isdigit() and stripped[1] == '.'):
            content = clean.lstrip('-*•0123456789. ').strip()
            elements.append(Paragraph(f"&bull; {content}", bullet_style))
            
        # Standard Body (with sentence-splitting for long blocks)
        else:
            if len(clean) > 400:
                sentences = re.split(r'(?<=[.!?])\s+', clean)
                sub_groups = [" ".join(sentences[i:i+3]) for i in range(0, len(sentences), 3)]
                for group in sub_groups:
                    elements.append(Paragraph(group, body_style))
            else:
                elements.append(Paragraph(clean, body_style))
    
    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = f"Optimized for ATS &bull; {datetime.now().strftime('%Y')}"
    elements.append(Paragraph(_clean_text(footer_text), ParagraphStyle('Footer', fontSize=8, textColor='#bbbbbb', alignment=TA_CENTER)))
    
    doc.build(elements)

def generate_docx(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> None:
    # Basic DOCX fallback for production
    with open(output_path, 'w') as f:
        f.write(f"{candidate_name}\n\n{resume_text}")
