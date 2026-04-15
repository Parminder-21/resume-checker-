from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.models.request_models import DownloadRequest
from app.services.pdf_service import create_optimized_pdf
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/download")
async def download_pdf(data: DownloadRequest):
    """
    Generate and return an ATS-safe PDF of the optimized resume.
    Returns PDF as binary download.
    """
    if not data.optimized_resume or len(data.optimized_resume.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail="Optimized resume text is empty or too short."
        )

    try:
        pdf_bytes = create_optimized_pdf(
            optimized_resume=data.optimized_resume,
            candidate_name=data.candidate_name or "Candidate"
        )

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": "attachment; filename=optimized_resume.pdf",
                "Content-Length": str(len(pdf_bytes))
            }
        )

    except Exception as e:
        logger.error(f"PDF generation failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"PDF generation failed: {str(e)}"
        )