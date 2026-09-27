from fastapi import APIRouter, UploadFile, File, HTTPException

from services.cv_parser import extract_cv_text
from schemas.resume import (
    ResumeUploadResponse,
    ResumeAnalyzeResponse,
)

from services.cv_parser import extract_cv_text
from services.cv_analyzer import CVAnalyzer

router = APIRouter(
    prefix="/resume",
    tags=["Resume"],
)


MAX_FILE_SIZE = 5 * 1024 * 1024

ALLOWED_EXTENSIONS = (
    ".pdf",
    ".docx",
)


@router.post(
    "/upload",
    response_model=ResumeUploadResponse,
)
async def upload_resume(
    file: UploadFile = File(...),
):
    filename = file.filename or ""

    if not filename.lower().endswith(
        ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    content = await file.read(
        MAX_FILE_SIZE + 1
    )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB.",
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    try:
        extracted_text = extract_cv_text(
            filename,
            content,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="Could not extract text from the CV.",
        )

    return {
        "filename": filename,
        "size": len(content),
        "status": "success",
        "message": (
            f"CV uploaded and parsed successfully. "
            f"Extracted {len(extracted_text)} characters."
        ),
    }

@router.post(
    "/analyze",
    response_model=ResumeAnalyzeResponse,
)
async def analyze_resume(
    file: UploadFile = File(...),
):
    filename = file.filename or ""

    if not filename.lower().endswith(
        ALLOWED_EXTENSIONS
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed.",
        )

    content = await file.read(
        MAX_FILE_SIZE + 1
    )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB.",
        )

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    try:
        extracted_text = extract_cv_text(
            filename,
            content,
        )

        if not extracted_text:
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from the CV.",
            )

        analyzer = CVAnalyzer()

        profile = analyzer.analyze(
            extracted_text
        )

        return ResumeAnalyzeResponse(
            filename=filename,
            profile=profile,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )