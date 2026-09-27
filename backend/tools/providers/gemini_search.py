from google import genai
from google.genai import types

from config import GOOGLE_API_KEY, GEMINI_MODEL
from tools.providers.web_search_provider import WebSearchProvider


class GeminiWebSearch(WebSearchProvider):

    def __init__(self):

        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

    def search(self, query: str) -> str:

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        try:

            print("\n======================================")
            print(">>> GEMINI GOOGLE SEARCH")
            print("======================================")

            print(">>> Query:")
            print(query)

            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=f"""
Search Google for current and real job openings.

Search query:
{query}

Find actual job listings.

For every job include, when available:
- Job title
- Company
- Location
- Skills
- Experience
- Salary
- Direct job posting URL

Do not invent jobs.
Do not invent URLs.
Only use information found through Google Search.
""",
                config=types.GenerateContentConfig(
                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ]
                ),
            )

        except Exception as error:

            raise RuntimeError(
                f"Gemini web search failed: {error}"
            ) from error

        if not response.text:

            raise RuntimeError(
                "Gemini web search returned empty content."
            )

        print(">>> Gemini Google Search succeeded")
        print("======================================\n")

        return response.text.strip()