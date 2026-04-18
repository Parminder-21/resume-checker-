import sys
import os
import tempfile

# Allow importing ai_engine from project root
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
project_root = os.path.dirname(backend_root)
sys.path.insert(0, project_root)

from ai_engine.pdf.pdf_generator import (
    generate_pdf,
    generate_docx,
    is_pdf_conversion_available
)


def create_optimized_pdf(optimized_resume: str, candidate_name: str = "Candidate") -> tuple[bytes, str]:
    """
    Generate the optimized resume as a downloadable file.

    Returns:
        (file_bytes, content_type)

        If PDF conversion is available:
            → (pdf_bytes,  "application/pdf")
            → filename: optimized_resume.pdf

        If PDF conversion is NOT available (fallback):
            → (docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            → filename: optimized_resume.docx

    The caller (download.py route) checks content_type to set the
    correct Content-Disposition filename extension.
    """
    with tempfile.TemporaryDirectory() as tmpdir:

        if is_pdf_conversion_available():
            # In a FastAPI async context, COM objects require thread initialization
            import pythoncom
            pythoncom.CoInitialize()
            
            # ── PDF path (preferred) ─────────────────────────────────────
            output_path = os.path.join(tmpdir, "resume.pdf")
            try:
                generate_pdf(
                    resume_text=optimized_resume,
                    output_path=output_path,
                    candidate_name=candidate_name
                )
                with open(output_path, "rb") as f:
                    file_data = f.read()
                    
                pythoncom.CoUninitialize()
                return file_data, "application/pdf"
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Docx2pdf failed: {e}", exc_info=True)
                # PDF failed even though Word is present — fall through
                pass

        # ── DOCX fallback ────────────────────────────────────────────────
        output_path = os.path.join(tmpdir, "resume.docx")
        generate_docx(
            resume_text=optimized_resume,
            output_path=output_path,
            candidate_name=candidate_name
        )
        with open(output_path, "rb") as f:
            return f.read(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document"