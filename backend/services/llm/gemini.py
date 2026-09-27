from google import genai

from config import GOOGLE_API_KEY, GEMINI_MODEL
from services.llm.base import BaseLLM


class GeminiLLM(BaseLLM):

    def __init__(self):

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        if not GEMINI_MODEL:
            raise ValueError(
                "GEMINI_MODEL is not configured."
            )

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    def generate(self, prompt: str) -> str:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        try:

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

        except Exception as error:

            raise RuntimeError(
                f"Gemini generation failed: {error}"
            ) from error

        if not response.text:

            raise RuntimeError(
                "Gemini returned empty content."
            )

        return response.text.strip()