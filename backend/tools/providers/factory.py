from tools.providers.openrouter_search import OpenRouterWebSearch
from tools.providers.gemini_search import GeminiWebSearch


class FallbackWebSearchProvider:

    def __init__(self):
        self.providers = [
            ("openrouter", OpenRouterWebSearch),
            ("gemini", GeminiWebSearch),
        ]

    def search(self, query: str) -> str:

        errors = []

        for provider_name, provider_class in self.providers:

            try:
                print(
                    f"\n>>> Trying web search provider: "
                    f"{provider_name}"
                )

                provider = provider_class()

                result = provider.search(query)

                if result and result.strip():

                    print(
                        f">>> Web search provider succeeded: "
                        f"{provider_name}"
                    )

                    return result.strip()

                errors.append(
                    f"{provider_name}: empty response"
                )

            except Exception as error:

                print(
                    f">>> Web search provider failed: "
                    f"{provider_name} -> {error}"
                )

                errors.append(
                    f"{provider_name}: {error}"
                )

        raise RuntimeError(
            "All web search providers failed. "
            + " | ".join(errors)
        )


def get_search_provider():

    return FallbackWebSearchProvider()