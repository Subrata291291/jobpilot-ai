import os
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


# Application settings
APP_NAME = os.getenv("APP_NAME", "JobPilot AI")
APP_ENV = os.getenv("APP_ENV", "development")


# API keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


# LLM models
GROQ_MODEL = os.getenv("GROQ_MODEL")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")