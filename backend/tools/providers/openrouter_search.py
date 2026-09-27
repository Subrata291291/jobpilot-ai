from openai import OpenAI, RateLimitError

from config import OPENROUTER_API_KEY
from tools.providers.web_search_provider import WebSearchProvider


class OpenRouterWebSearch(WebSearchProvider):

    def __init__(self):

        if not OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def search(self, query: str) -> str:

        if not query or not query.strip():
            raise ValueError(
                "Search query cannot be empty."
            )

        try:

            print("\n======================================")
            print(">>> OPENROUTER WEB SEARCH")
            print("======================================")

            print(f">>> Query:")
            print(query)

            response = self.client.chat.completions.create(
                model="openrouter/free",

                messages=[
                    {
                        "role": "user",
                        "content": f"""
Search the web for current and real job openings.

Search query:
{query}

Find actual job listings.

For every job listing, identify:
- Job title
- Company
- Location
- Skills
- Experience
- Salary if available
- Direct job posting URL

IMPORTANT:

Use actual job listings from the web search.

Do not invent jobs.

Do not invent URLs.

The source URL of each search result must be preserved.
"""
                    }
                ],

                tools=[
                    {
                        "type": "openrouter:web_search",
                        "parameters": {
                            "max_results": 10,
                            "max_total_results": 20,
                        },
                    }
                ],

                max_tokens=2500,
            )

        except RateLimitError as error:

            print(
                ">>> OpenRouter web search rate limit reached."
            )

            raise RuntimeError(
                "OpenRouter web search rate limit reached."
            ) from error

        except Exception as error:

            print(
                f">>> OpenRouter web search failed: {error}"
            )

            raise RuntimeError(
                f"Web search failed: {error}"
            ) from error

        # --------------------------------------------------
        # Validate response
        # --------------------------------------------------

        if not response.choices:

            raise RuntimeError(
                "OpenRouter web search returned no choices."
            )

        message = response.choices[0].message

        # --------------------------------------------------
        # Get normal model response
        # --------------------------------------------------

        content = message.content or ""

        print(
            f">>> Model response length: "
            f"{len(content)} characters"
        )

        # --------------------------------------------------
        # Extract URL citations
        # --------------------------------------------------

        annotations = getattr(
            message,
            "annotations",
            None,
        )

        if annotations is None:
            annotations = []

        print(
            f">>> URL annotations found: "
            f"{len(annotations)}"
        )

        search_sources = []

        for annotation in annotations:

            try:

                # Convert SDK object to dictionary
                if hasattr(annotation, "model_dump"):
                    annotation_data = annotation.model_dump()

                elif hasattr(annotation, "dict"):
                    annotation_data = annotation.dict()

                elif isinstance(annotation, dict):
                    annotation_data = annotation

                else:
                    continue

                # Only process URL citations
                if annotation_data.get("type") != "url_citation":
                    continue

                citation = annotation_data.get(
                    "url_citation",
                    {},
                )

                if not citation:
                    continue

                url = citation.get("url", "")
                title = citation.get("title", "")
                citation_content = citation.get(
                    "content",
                    "",
                )

                if not url:
                    continue

                source = {
                    "title": title,
                    "url": url,
                    "content": citation_content,
                }

                search_sources.append(source)

                print(
                    f">>> Source URL: {url}"
                )

            except Exception as error:

                print(
                    f">>> Could not parse annotation: "
                    f"{error}"
                )

                continue

        # --------------------------------------------------
        # Remove duplicate URLs
        # --------------------------------------------------

        unique_sources = []
        seen_urls = set()

        for source in search_sources:

            url = source["url"].strip()

            if not url:
                continue

            if url in seen_urls:
                continue

            seen_urls.add(url)

            unique_sources.append(source)

        print(
            f">>> Unique source URLs: "
            f"{len(unique_sources)}"
        )

        # --------------------------------------------------
        # Build source section
        # --------------------------------------------------

        source_text_parts = []

        for index, source in enumerate(
            unique_sources,
            start=1,
        ):

            title = source["title"]
            url = source["url"]
            source_content = source["content"]

            source_text_parts.append(
                f"""
SOURCE {index}
Title: {title}
URL: {url}
Content:
{source_content}
"""
            )

        source_text = "\n".join(
            source_text_parts
        )

        # --------------------------------------------------
        # Final result for JobExtractor
        # --------------------------------------------------

        if source_text:

            final_result = f"""
WEB SEARCH ANSWER
=================

{content}

WEB SEARCH SOURCES
==================

{source_text}
"""

        elif content.strip():

            print(
                ">>> No URL annotations found."
            )

            final_result = f"""
WEB SEARCH ANSWER
=================

{content}

NOTE:
No URL citation annotations were returned
by the search provider.
"""

        else:

            raise RuntimeError(
                "OpenRouter web search returned "
                "an empty response and no source URLs."
            )

        print(
            f">>> Final search result length: "
            f"{len(final_result)} characters"
        )

        print("======================================")
        print(">>> WEB SEARCH COMPLETED")
        print("======================================\n")

        return final_result.strip()