from fastapi import APIRouter, HTTPException, UploadFile, File, Form

from schemas.resume import CandidateProfile
from agents.job_agent import JobAgent
from services.cv_parser import extract_cv_text
from services.cv_analyzer import CVAnalyzer


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/recommend")
def recommend_jobs(candidate: CandidateProfile):

    try:
        agent = JobAgent()
        jobs = agent.run(candidate)

        return {
            "status": "success",
            "total_jobs": len(jobs),
            "jobs": jobs,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        print("\n========== JOB RECOMMENDATION ERROR ==========")
        print(error)
        print("==============================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/recommend-from-cv")
async def recommend_jobs_from_cv(
    file: UploadFile = File(...),
    preferred_role: str = Form(""),
    preferred_location: str = Form(""),
):

    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CV is empty.",
        )

    try:
        # -------------------------
        # 1. Extract CV text
        # -------------------------

        cv_text = extract_cv_text(
            filename,
            content,
        )

        if not cv_text:
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from the CV.",
            )

        # -------------------------
        # 2. Analyze CV
        # -------------------------

        analyzer = CVAnalyzer()

        candidate = analyzer.analyze(
            cv_text
        )

        # -------------------------
        # 3. Add user preferences
        # -------------------------

        if preferred_role.strip():
            candidate.preferred_roles = [
                preferred_role.strip()
            ]

        if preferred_location.strip():
            candidate.preferred_locations = [
                preferred_location.strip()
            ]

        # -------------------------
        # 4. Search and match jobs
        # -------------------------

        agent = JobAgent()

        jobs = agent.run(
            candidate
        )

        # -------------------------
        # 5. Return response
        # -------------------------

        return {
            "status": "success",
            "candidate": candidate.model_dump(),
            "total_jobs": len(jobs),
            "jobs": jobs,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except RuntimeError as error:
        print("\n========== JOB RECOMMENDATION ERROR ==========")
        print(error)
        print("==============================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )