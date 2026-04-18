import os
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors

# ─── Color Palette ─────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#112244')
DARK_GREY = colors.HexColor('#333333')
MID_GREY  = colors.HexColor('#666666')
LIGHT_GREY= colors.HexColor('#bbbbbb')

def _clean_text(text: str) -> str:
    """Sanitize text for ReportLab — handles XML escaping and non-ASCII characters."""
    if not text:
        return ""
    
    # 1. Unicode to ASCII replacements for standard fonts
    replacements = {
        '\u2022': '-', '\u2023': '-', '\u2043': '-',
        '\u2013': '-', '\u2014': '--',
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u00a0': ' ', '\ufb01': 'fi', '\ufb02': 'fl'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    # 2. XML escaping (Crucial: Paragraphs crash on raw &, <, >)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
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

    title_style = ParagraphStyle(
        'Title', parent=styles['Heading1'],
        fontSize=20, textColor=NAVY,
        spaceAfter=14, alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    section_title_style = ParagraphStyle(
        'Section', parent=styles['Heading2'],
        fontSize=13, textColor=NAVY,
        spaceAfter=6, spaceBefore=10,
        fontName='Helvetica-Bold'
    )
    subheading_style = ParagraphStyle(
        'SubHeading', parent=styles['BodyText'],
        fontSize=11, leading=13, textColor=DARK_GREY,
        spaceAfter=4, fontName='Helvetica-Bold'
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['BodyText'],
        fontSize=10, leading=13, textColor=DARK_GREY,
        spaceAfter=8, fontName='Helvetica'
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['BodyText'],
        fontSize=10, leading=13, leftIndent=15,
        firstLineIndent=0, spaceAfter=4,
        textColor=DARK_GREY, fontName='Helvetica'
    )
    footer_style = ParagraphStyle(
        'Footer', fontSize=8, textColor=LIGHT_GREY, alignment=TA_CENTER
    )

    elements = []

    # Header
    elements.append(Paragraph(_clean_text(candidate_name).upper(), title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=10))

    # Aggressive Layout Rescue
    text = resume_text
    headers = [
        'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'SUMMARY',
        'CERTIFICATIONS', 'LANGUAGES', 'TECHNICAL SKILLS', 'ACHIEVEMENTS'
    ]
    for h in headers:
        text = re.sub(f"(?<!\n\n)(?P<head>{h})", r"\n\n\g<head>", text, flags=re.IGNORECASE)

    date_pattern = (
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2})"
        r"\s?[\-\u2013\u2014\s]\s?"
        r"(?:Present|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d{2})"
    )
    text = re.sub(f"(?<!\n\n)(?P<date>{date_pattern})", r"\n\n\g<date>", text)
    text = re.sub(r"(?<!\n)(?P<bull>[•\-\*])", r"\n\g<bull>", text)

    chunks = text.split('\n')
    for chunk in chunks:
        stripped = chunk.strip()
        if not stripped:
            continue
        clean = _clean_text(stripped)
        if not clean:
            continue

        # Section Header
        if any(h in clean.upper() for h in headers) and len(clean) < 40:
            if len(elements) > 2:
                elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(clean.upper(), section_title_style))
            elements.append(HRFlowable(width="30%", thickness=0.5, color=LIGHT_GREY, spaceAfter=4, align=TA_LEFT))

        # Date / Subheader
        elif re.search(date_pattern, clean) and len(clean) < 120:
            elements.append(Paragraph(clean, subheading_style))

        # Bullets
        elif stripped.startswith(('-', '*', '\u2022')) or (
            len(stripped) > 1 and stripped[0].isdigit() and stripped[1] == '.'
        ):
            content = clean.lstrip('-*\u2022 0123456789. ').strip()
            if content:
                elements.append(Paragraph(f"&bull; {content}", bullet_style))

        # Standard Body
        else:
            if len(clean) > 400:
                sentences = re.split(r'(?<=[.!?])\s+', clean)
                for i in range(0, len(sentences), 3):
                    group = " ".join(sentences[i:i+3])
                    elements.append(Paragraph(group, body_style))
            else:
                elements.append(Paragraph(clean, body_style))

    # Footer
    elements.append(Spacer(1, 0.5 * inch))
    footer_text = f"Optimized for ATS &bull; {datetime.now().strftime('%Y')}"
    elements.append(Paragraph(_clean_text(footer_text), footer_style))

    doc.build(elements)


def generate_docx(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> None:
    """Basic DOCX fallback (writes plain text)."""
    with open(output_path, 'w', encoding='utf-8', errors='ignore') as f:
        f.write(f"{candidate_name}\n\n{resume_text}")
