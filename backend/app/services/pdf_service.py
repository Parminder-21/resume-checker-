import sys
import os
import tempfile
import logging

# Allow importing ai_engine from project root
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
project_root = os.path.dirname(backend_root)
sys.path.insert(0, project_root)

from ai_engine.pdf.pdf_generator import generate_pdf

logger = logging.getLogger(__name__)

def create_optimized_pdf(optimized_resume: str, candidate_name: str = "Candidate") -> tuple[bytes, str]:
    """
    Generate the optimized resume as a downloadable PDF.
    Uses ReportLab for production stability and cross-platform compatibility.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "resume.pdf")
        try:
            generate_pdf(
                resume_text=optimized_resume,
                output_path=output_path,
                candidate_name=candidate_name
            )
            with open(output_path, "rb") as f:
                file_data = f.read()
                
            return file_data, "application/pdf"
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}", exc_info=True)
            # Fallback to simple text file if something goes wrong
            return optimized_resume.encode('utf-8'), "text/plain"