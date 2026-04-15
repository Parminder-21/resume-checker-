"""PDF generation module for creating ATS-safe resume PDFs."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from datetime import datetime


def generate_pdf(resume_text: str, output_path: str, candidate_name: str = "Candidate") -> None:
    """
    Generate an ATS-safe PDF from resume text.
    
    Args:
        resume_text: The resume content as plain text
        output_path: Path where to save the PDF file
        candidate_name: Name of the candidate for header
    """
    # Create PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch
    )
    
    # Create styles
    styles = getSampleStyleSheet()
    
    # Custom styles for resume
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor='#000000',
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        textColor='#000000',
        spaceAfter=6,
        spaceBefore=6,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        textColor='#000000',
        spaceAfter=4,
        leading=12,
        fontName='Helvetica'
    )
    
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['BodyText'],
        fontSize=10,
        textColor='#000000',
        spaceAfter=3,
        leftIndent=20,
        leading=11,
        fontName='Helvetica'
    )
    
    # Build document elements
    elements = []
    
    # Add candidate name as title
    elements.append(Paragraph(candidate_name, title_style))
    elements.append(Spacer(1, 0.1 * inch))
    
    # Process resume text into sections
    lines = resume_text.split('\n')
    current_section = None
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            elements.append(Spacer(1, 0.05 * inch))
            continue
        
        # Detect section headers (typically all caps or end with ":")
        if (stripped.isupper() or stripped.endswith(':')) and len(stripped) > 3:
            if current_section is not None:
                elements.append(Spacer(1, 0.05 * inch))
            elements.append(Paragraph(stripped, heading_style))
            current_section = stripped
            elements.append(Spacer(1, 0.05 * inch))
        # Detect bullet points
        elif line.startswith((' -', ' •', ' *', '  -', '  •', '  *')):
            # Remove bullet markers and add as formatted bullet
            clean_text = line.lstrip()
            if clean_text[0] in '-•*':
                clean_text = clean_text[1:].lstrip()
            elements.append(Paragraph(f"• {clean_text}", bullet_style))
        else:
            # Regular paragraph text
            elements.append(Paragraph(stripped, body_style))
    
    # Add footer with generation time
    elements.append(Spacer(1, 0.2 * inch))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor='#666666',
        alignment=TA_LEFT
    )))
    
    # Build PDF
    doc.build(elements)
