import json
import re

from services.llm.service import LLMService


class JobExtractor:

    def __init__(self):
        self.llm_service = LLMService()

    def extract(self, search_results: str) -> list[dict]:

        if not search_results or not search_results.strip():
            raise ValueError(
                "Search results cannot be empty."
            )

        prompt = f"""
You are a professional job listing extraction system.

Your task is to extract ONLY real and distinct job listings
from the web search results provided below.

Return ONLY a valid JSON array.

Use EXACTLY this structure:

[
    {{
        "title": "",
        "company": "",
        "location": "",
        "skills": [],
        "experience": "",
        "salary": "",
        "url": ""
    }}
]

IMPORTANT URL RULES:

1. Extract the EXACT URL associated with each specific job listing.

2. The "url" field is extremely important.

3. If a specific job posting URL is available in the search results,
   ALWAYS put that URL into the "url" field.

4. Return the URL as a plain raw URL string.

5. Do NOT return markdown links.

6. Do NOT return:

   [Job Title](https://example.com/job/123)

7. Return:

   "url": "https://example.com/job/123"

8. Preserve the URL exactly as it appears in the search results.

9. Do NOT replace a specific job URL with the company's homepage.

10. Do NOT use a company homepage when a specific job posting URL exists.

11. Do NOT invent, guess, construct, modify, or hallucinate URLs.

12. If the search result contains a URL that clearly belongs to
    the specific job listing, use that URL.

13. If no specific job URL is available, return:

    "url": ""

14. Do not return search-engine URLs.

15. Do not return URLs that are unrelated to the job listing.

16. Do not return URLs from another job.

17. Prefer a direct job-detail URL over:

    - search-results page
    - category page
    - company homepage
    - company careers homepage

18. A URL from the WEB SEARCH SOURCES section must only be assigned
    to a job when the source clearly corresponds to that job.

19. Never assign the same source URL to unrelated jobs.

20. Never invent a URL just because a job title or company name is known.

JOB EXTRACTION RULES:

1. Extract as many distinct relevant job listings as are explicitly
   present in the search results, up to 20 jobs.

2. Do not invent or guess information.

3. Extract each job separately.

4. Do not use general search-summary skills as job-specific skills.

5. Only put skills explicitly associated with that particular job
   into "skills".

6. If skills are unavailable, use [].

7. If experience is unavailable, use "".

8. If salary is unavailable, use "".

9. If company is unavailable, use "".

10. If location is unavailable, use "".

11. Do not include expired/non-job pages unless the search result
    explicitly presents them as job listings.

12. Do not duplicate jobs.

13. Do not stop after 3 jobs.

14. Only include jobs with enough explicit information to identify
    the listing.

15. Return JSON only.

16. Do not use markdown.

17. Do not add explanations.

18. Do not wrap the JSON inside markdown code fences.

19. The first character of your response must be "[".

20. The last character of your response must be "]".

URL EXAMPLE:

If the search result contains:

Frontend Developer
ABC Technologies
Kolkata
https://example.com/jobs/frontend-developer-123

Return:

[
    {{
        "title": "Frontend Developer",
        "company": "ABC Technologies",
        "location": "Kolkata",
        "skills": [],
        "experience": "",
        "salary": "",
        "url": "https://example.com/jobs/frontend-developer-123"
    }}
]

If only this exists:

ABC Technologies
https://example.com/

and there is no specific job URL, return:

[
    {{
        "title": "Frontend Developer",
        "company": "ABC Technologies",
        "location": "Kolkata",
        "skills": [],
        "experience": "",
        "salary": "",
        "url": ""
    }}
]

Do NOT convert:

https://example.com/

into a job URL.

WEB SEARCH RESULTS
--------------------
{search_results}
--------------------
"""

        # --------------------------------------------------
        # Generate extraction response
        # --------------------------------------------------

        response = self.llm_service.generate(prompt)

        # --------------------------------------------------
        # Parse JSON safely
        # --------------------------------------------------

        jobs = self._parse_json_response(response)

        if not isinstance(jobs, list):
            raise ValueError(
                "Job extraction result must be a list."
            )

        # --------------------------------------------------
        # Clean and validate jobs
        # --------------------------------------------------

        cleaned_jobs = []

        seen_jobs = set()

        for job in jobs:

            if not isinstance(job, dict):
                continue

            title = self._clean_text(
                job.get("title", "")
            )

            company = self._clean_text(
                job.get("company", "")
            )

            location = self._clean_text(
                job.get("location", "")
            )

            experience = self._clean_text(
                job.get("experience", "")
            )

            salary = self._clean_text(
                job.get("salary", "")
            )

            # ----------------------------------------------
            # Skills
            # ----------------------------------------------

            skills = job.get("skills", [])

            if not isinstance(skills, list):
                skills = []

            cleaned_skills = []

            for skill in skills:

                if isinstance(skill, str):

                    skill = skill.strip()

                    if skill and skill not in cleaned_skills:
                        cleaned_skills.append(skill)

            # ----------------------------------------------
            # URL
            # ----------------------------------------------

            url = self._clean_url(
                job.get("url", "")
            )

            # ----------------------------------------------
            # Skip completely invalid objects
            # ----------------------------------------------

            if not title and not company:
                continue

            # ----------------------------------------------
            # Duplicate detection
            # ----------------------------------------------

            duplicate_key = (
                title.lower().strip(),
                company.lower().strip(),
                location.lower().strip(),
            )

            if duplicate_key in seen_jobs:
                continue

            seen_jobs.add(duplicate_key)

            # ----------------------------------------------
            # Final cleaned job
            # ----------------------------------------------

            cleaned_job = {
                "title": title,
                "company": company,
                "location": location,
                "skills": cleaned_skills,
                "experience": experience,
                "salary": salary,
                "url": url,
            }

            cleaned_jobs.append(cleaned_job)

        # --------------------------------------------------
        # Maximum 20 jobs
        # --------------------------------------------------

        return cleaned_jobs[:20]

    # ======================================================
    # JSON PARSER
    # ======================================================

    @staticmethod
    def _parse_json_response(response: str) -> list:

        if not response or not response.strip():

            raise ValueError(
                "LLM returned an empty job extraction response."
            )

        text = response.strip()

        # --------------------------------------------------
        # Debug output
        # --------------------------------------------------

        print(
            "\n========== JOB EXTRACTOR RESPONSE =========="
        )

        print(text)

        print(
            "=============================================\n"
        )

        # --------------------------------------------------
        # 1. Try direct JSON
        # --------------------------------------------------

        try:

            data = json.loads(text)

            if isinstance(data, list):
                return data

        except json.JSONDecodeError:
            pass

        # --------------------------------------------------
        # 2. Remove Markdown code fences
        # --------------------------------------------------

        cleaned = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\s*```$",
            "",
            cleaned,
        )

        cleaned = cleaned.strip()

        try:

            data = json.loads(cleaned)

            if isinstance(data, list):
                return data

        except json.JSONDecodeError:
            pass

        # --------------------------------------------------
        # 3. Extract JSON array from surrounding text
        # --------------------------------------------------

        start = cleaned.find("[")
        end = cleaned.rfind("]")

        if start != -1 and end != -1 and end > start:

            json_text = cleaned[
                start:end + 1
            ]

            try:

                data = json.loads(json_text)

                if isinstance(data, list):
                    return data

            except json.JSONDecodeError:
                pass

        # --------------------------------------------------
        # 4. Invalid JSON
        # --------------------------------------------------

        print(
            "\n========== INVALID JOB JSON =========="
        )

        print(response)

        print(
            "======================================\n"
        )

        raise ValueError(
            "LLM returned invalid job JSON."
        )

    # ======================================================
    # TEXT CLEANER
    # ======================================================

    @staticmethod
    def _clean_text(value) -> str:

        if value is None:
            return ""

        if not isinstance(value, str):
            value = str(value)

        return value.strip()

    # ======================================================
    # URL CLEANER
    # ======================================================

    @staticmethod
    def _clean_url(value) -> str:

        if not value:
            return ""

        if not isinstance(value, str):
            return ""

        url = value.strip()

        # --------------------------------------------------
        # Remove markdown link
        #
        # [Job Title](https://example.com/job)
        # --------------------------------------------------

        markdown_match = re.match(
            r"^\[.*?\]\((https?://[^\s)]+)\)$",
            url,
            re.IGNORECASE,
        )

        if markdown_match:

            url = markdown_match.group(1)

        # --------------------------------------------------
        # Sometimes LLM may return:
        #
        # <https://example.com/job>
        # --------------------------------------------------

        url = url.strip("<>")

        # --------------------------------------------------
        # Remove quotes
        # --------------------------------------------------

        url = url.strip("\"'")

        # --------------------------------------------------
        # Remove common trailing punctuation
        # --------------------------------------------------

        url = url.rstrip(
            ".,;:!?)]}"
        )

        # --------------------------------------------------
        # Validate HTTP / HTTPS
        # --------------------------------------------------

        if not re.match(
            r"^https?://[^\s]+$",
            url,
            re.IGNORECASE,
        ):

            return ""

        return url