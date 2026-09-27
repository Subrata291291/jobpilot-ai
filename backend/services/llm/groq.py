from groq import Groq

from config import GROQ_API_KEY, GROQ_MODEL
from services.llm.base import BaseLLM


class GroqLLM(BaseLLM):
    """
    Groq LLM implementation.
    """

    def __init__(self):
        self.client = Groq(
            api_key=GROQ_API_KEY,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_completion_tokens=2000,
            reasoning_effort="low",
            include_reasoning=False,
        )

        if not response.choices:
            raise RuntimeError(
                "Groq returned no choices."
            )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "Groq returned empty content."
            )

        return content.strip()