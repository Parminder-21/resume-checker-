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
    Generate the optimized resume.
    Pipeline: docx -> pdf (via docx2pdf).
    Fallback: serves .docx if PDF conversion is not possible (e.g. on Linux/Render).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # We start with .pdf suggestion, but generate_pdf might return .docx
        ideal_path = os.path.join(tmpdir, "resume.pdf") 
        try:
            actual_path = generate_pdf(
                resume_text=optimized_resume,
                output_path=ideal_path,
                candidate_name=candidate_name
            )
            
            with open(actual_path, "rb") as f:
                file_data = f.read()
            
            # Determine content type based on what was actually returned
            if actual_path.endswith('.docx'):
                mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            else:
                mime_type = "application/pdf"
                
            return file_data, mime_type
            
        except Exception as e:
            logger.error(f"Resume generation failed: {e}", exc_info=True)
            # Fallback to simple text file if something goes wrong
            return optimized_resume.encode('utf-8'), "text/plain"