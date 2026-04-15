import sys
import os
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from ai_engine.pdf.pdf_generator import generate_pdf


def create_optimized_pdf(optimized_resume: str, candidate_name: str = "Candidate") -> bytes:
    """
    Generate an ATS-safe PDF from optimized resume text.
    Returns PDF as raw bytes.
    """
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        generate_pdf(
            resume_text=optimized_resume,
            output_path=tmp_path,
            candidate_name=candidate_name
        )
        with open(tmp_path, "rb") as f:
            pdf_bytes = f.read()
        return pdf_bytes
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)