from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from services.llm.base import BaseLLM


class OpenAILLM(BaseLLM):

    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            max_completion_tokens=2000,
        )

        if not response.choices:
            raise RuntimeError(
                "OpenAI returned no choices."
            )

        content = response.choices[0].message.content

        if not content:
            raise RuntimeError(
                "OpenAI returned empty content."
            )

        return content.strip()