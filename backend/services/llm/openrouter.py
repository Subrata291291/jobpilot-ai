from openai import OpenAI

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL
from services.llm.base import BaseLLM


class OpenRouterLLM(BaseLLM):

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def generate(self, prompt: str) -> str:

        print("\n>>> OPENROUTER GENERATE CALLED")
        print(">>> MODEL:", OPENROUTER_MODEL)

        response = self.client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1500,
        )

        print(">>> OPENROUTER RESPONSE RECEIVED")
        print(">>> RESPONSE:", response)

        if not response.choices:
            raise RuntimeError(
                "OpenRouter returned no choices."
            )

        message = response.choices[0].message

        print(">>> MESSAGE:", message)
        print(">>> CONTENT:", repr(message.content))
        print(
            ">>> REASONING:",
            repr(getattr(message, "reasoning", None))
        )
        print(
            ">>> FINISH REASON:",
            response.choices[0].finish_reason
        )

        content = message.content

        if not content:
            raise RuntimeError(
                "OpenRouter returned empty content."
            )

        return content.strip()