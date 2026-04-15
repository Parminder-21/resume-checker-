import os
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.request_models import UploadResponse, ErrorResponse
from app.services.parser_service import process_uploaded_pdf
from app.core.config import settings

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume and extract clean text.
    Returns structured text ready for the optimize endpoint.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported. Please upload a .pdf file."
        )

    # Validate file size
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum allowed size is {settings.MAX_FILE_SIZE_MB}MB."
        )

    # Save to temp file and parse
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = process_uploaded_pdf(tmp_path)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse PDF: {str(e)}"
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return UploadResponse(
        status="success",
        resume_text=result["raw_text"],
        char_count=result["char_count"],
        sections_detected=result["sections_detected"]
    )