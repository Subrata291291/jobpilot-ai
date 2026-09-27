import json

from schemas.resume import CandidateProfile
from services.llm.service import LLMService


class CVAnalyzer:
    """
    Analyze extracted CV text and create
    a structured candidate profile.
    """

    def __init__(self):
        self.llm_service = LLMService()

    def analyze(self, cv_text: str) -> CandidateProfile:
        if not cv_text or not cv_text.strip():
            raise ValueError("CV text cannot be empty.")

        prompt = f"""
You are a CV analysis assistant.

Analyze the CV text below and extract only information
that is supported by the CV.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "name": "",
    "current_role": "",
    "experience_years": 0,
    "skills": [],
    "education": [],
    "preferred_roles": [],
    "preferred_locations": []
}}

Rules:

1. Do not invent information.
2. If information is not available, use an empty string,
   0, or an empty list.
3. experience_years must be a number.
4. skills must be an array of strings.
5. education must be an array of strings.
6. preferred_roles must be an array of strings.
7. preferred_locations must be an array of strings.
8. Return JSON only. Do not use markdown.
9. Keep the extracted information concise.

CV TEXT:
--------------------
{cv_text}
--------------------
"""

        response = self.llm_service.generate(prompt)

        try:
            data = json.loads(response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "LLM returned invalid JSON."
            ) from error

        return CandidateProfile(**data)