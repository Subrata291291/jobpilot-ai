from services.llm.groq import GroqLLM
from services.llm.openrouter import OpenRouterLLM
from services.llm.openai import OpenAILLM
from services.llm.gemini import GeminiLLM


class LLMService:

    def __init__(self):

        self.providers = [
            ("groq", GroqLLM),
            ("openrouter", OpenRouterLLM),
            ("openai", OpenAILLM),
            ("gemini", GeminiLLM),
        ]

    def generate(self, prompt: str) -> str:

        if not prompt or not prompt.strip():
            raise ValueError(
                "Prompt cannot be empty."
            )

        errors = []

        for provider_name, provider_class in self.providers:

            try:

                print(
                    f"\n>>> Trying LLM provider: "
                    f"{provider_name}"
                )

                provider = provider_class()

                response = provider.generate(prompt)

                if response and response.strip():

                    print(
                        f">>> LLM provider succeeded: "
                        f"{provider_name}"
                    )

                    return response.strip()

                errors.append(
                    f"{provider_name}: empty response"
                )

            except Exception as error:

                print(
                    f">>> LLM provider failed: "
                    f"{provider_name} -> {error}"
                )

                errors.append(
                    f"{provider_name}: {error}"
                )

        raise RuntimeError(
            "All LLM providers failed. "
            + " | ".join(errors)
        )