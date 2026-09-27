from fastapi import APIRouter, HTTPException

from schemas.chat import ChatRequest, ChatResponse
from services.llm.service import LLMService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        llm_service = LLMService()

        response = llm_service.generate(
            request.message
        )

        return ChatResponse(
            response=response
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