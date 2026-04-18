from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from app.models.request_models import DownloadRequest
from app.services.pdf_service import create_optimized_pdf
from app.routes.auth import get_current_user
from app.models.user import User as UserModel
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

EXTENSIONS = {
    "application/pdf": "pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
}


@router.post("/download")
async def download_resume(
    data: DownloadRequest,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Generate and return the optimized resume as a downloadable file.

    Returns PDF if LibreOffice is installed, DOCX otherwise.
    Both are ATS-safe and accepted by all major ATS platforms.
    """
    if not data.optimized_resume or len(data.optimized_resume.strip()) < 50:
        raise HTTPException(status_code=400, detail="Optimized resume text is empty.")

    try:
        file_bytes, content_type = create_optimized_pdf(
            optimized_resume=data.optimized_resume,
            candidate_name=data.candidate_name or "Candidate"
        )

        ext      = EXTENSIONS.get(content_type, "pdf")
        filename = f"optimized_resume.{ext}"

        return Response(
            content=file_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(file_bytes)),
                "X-File-Type": ext   # lets frontend show correct icon
            }
        )

    except Exception as e:
        logger.error(f"Download failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"File generation failed: {str(e)}")