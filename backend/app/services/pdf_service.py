import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_pdf(resume_text: str) -> bytes:
    """
    Generate ATS-safe PDF from resume text.
    Returns PDF as bytes.
    """
    try:
        # Create buffer
        pdf_buffer = BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch
        )
        
        # Build content
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles for ATS-safe formatting
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=14,
            textColor=(0, 0, 0),
            spaceAfter=6,
            alignment=0,  # Left align
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=11,
            textColor=(0, 0, 0),
            spaceAfter=4,
            spaceBefore=6,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            textColor=(0, 0, 0),
            spaceAfter=4,
            fontName='Helvetica',
            alignment=0
        )
        
        # Parse resume text into sections and add to story
        lines = resume_text.split('\n')
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                story.append(Spacer(1, 0.1*inch))
            elif stripped.isupper() and len(stripped) < 50:
                # Assume uppercase lines are section headers
                story.append(Paragraph(stripped, heading_style))
            else:
                # Regular content
                story.append(Paragraph(stripped, body_style))
        
        # Build PDF
        doc.build(story)
        
        # Return bytes
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    
    except Exception as e:
        logger.error(f"PDF generation error: {e}")
        raise
