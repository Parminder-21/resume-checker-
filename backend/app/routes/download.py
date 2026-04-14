from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.models.request_models import PDFDownloadRequest
from app.services import pdf_service
import io
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/download")
async def download_resume(data: PDFDownloadRequest):
    """Generate and download optimized resume as PDF."""
    
    try:
        if not data.optimized_resume.strip():
            raise HTTPException(status_code=400, detail="Resume text is empty")
        
        logger.info("Generating PDF...")
        pdf_bytes = pdf_service.generate_pdf(data.optimized_resume)
        
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=optimized_resume.pdf"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF download error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating PDF: {str(e)}"
        )
