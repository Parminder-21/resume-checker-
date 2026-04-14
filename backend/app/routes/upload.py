from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import parser_service
from app.models.request_models import UploadResponse
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a PDF resume."""
    
    try:
        # Validate file type
        if file.content_type not in ["application/pdf"]:
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )
        
        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size exceeds 5MB limit"
            )
        
        # Parse PDF
        resume_text, sections = await parser_service.parse_pdf(content)
        
        if not resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF. Try copy-pasting your resume instead."
            )
        
        logger.info(f"Resume parsed successfully. Length: {len(resume_text)}")
        
        return UploadResponse(
            status="success",
            resume_text=resume_text,
            sections=sections
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
