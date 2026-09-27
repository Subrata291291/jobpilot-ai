from openai import OpenAI

from config import OPENROUTER_API_KEY


class WebFetchTool:
    """
    Fetch and read a web page using OpenRouter.
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def fetch(self, url: str) -> str:

        if not url or not url.strip():
            raise ValueError("URL cannot be empty.")

        try:
            response = self.client.chat.completions.create(
                model="openrouter/free",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            "Read this job page and extract the "
                            "available job information.\n\n"
                            f"URL: {url}"
                        ),
                    }
                ],
                tools=[
                    {
                        "type": "openrouter:web_fetch",
                        "parameters": {
                            "engine": "openrouter",
                            "max_content_tokens": 4000,
                        },
                    }
                ],
                max_tokens=1000,
            )

            if not response.choices:
                return ""

            content = response.choices[0].message.content

            if not content:
                return ""

            return content.strip()

        except Exception as error:
            print(
                f"Web fetch failed for {url}: {error}"
            )
            return ""