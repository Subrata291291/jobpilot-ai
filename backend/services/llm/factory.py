from config import LLM_PROVIDER
from services.llm.base import BaseLLM
from services.llm.openrouter import OpenRouterLLM
from services.llm.groq import GroqLLM


def get_llm() -> BaseLLM:
    """
    Return the configured LLM provider.
    """

    if LLM_PROVIDER == "openrouter":
        return OpenRouterLLM()

    if LLM_PROVIDER == "groq":
        return GroqLLM()

    raise ValueError(
        f"Unsupported LLM provider: {LLM_PROVIDER}"
    )