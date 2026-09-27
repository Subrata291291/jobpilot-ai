from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME, APP_ENV

from api.chat import router as chat_router
from api.resume import router as resume_router
from api.jobs import router as jobs_router


app = FastAPI(
    title=APP_NAME,
    description="AI-powered job search and matching platform",
    version="1.0.0",
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(chat_router)
app.include_router(resume_router)
app.include_router(jobs_router)


@app.get("/")
def root():
    return {
        "message": f"{APP_NAME} API is running",
        "environment": APP_ENV,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/config-test")
def config_test():
    return {
        "app_name": APP_NAME,
        "environment": APP_ENV,
    }


@app.get("/llm-test")
def llm_test():
    from services.llm.service import LLMService

    service = LLMService()

    response = service.generate(
        "Reply with one short sentence: What is RAG?"
    )

    return {"response": response}