from schemas.resume import CandidateProfile
from tools.web_search import WebSearchTool
from services.job_extractor import JobExtractor
from services.matcher import JobMatcher


class JobAgent:
    """
    Job search agent.

    Takes a candidate profile, searches the web for
    relevant jobs, extracts structured job data, and
    ranks the jobs based on skill matching.
    """

    def __init__(self):
        self.web_search = WebSearchTool()
        self.job_extractor = JobExtractor()
        self.matcher = JobMatcher()

    def build_search_query(self, candidate: CandidateProfile) -> str:

        role = (
            candidate.preferred_roles[0].strip()
            if candidate.preferred_roles
            and candidate.preferred_roles[0].strip()
            else candidate.current_role
        )

        skills = ", ".join(candidate.skills[:8])
        location = ", ".join(candidate.preferred_locations[:3])

        query_parts = [
            "current job openings",
            role,
        ]

        if skills:
            query_parts.append(f"skills: {skills}")

        if location:
            query_parts.append(f"location: {location}")

        return " ".join(query_parts)

    def run(
        self,
        candidate: CandidateProfile,
    ) -> list[dict]:

        if not candidate.current_role:
            raise ValueError(
                "Candidate role is required."
            )

        search_query = self.build_search_query(
            candidate
        )

        print("\n=== JOB AGENT ===")
        print("Search Query:")
        print(search_query)

        search_results = self.web_search.search(
            search_query
        )

        jobs = self.job_extractor.extract(
            search_results
        )

        if not jobs:
            return []

        search_role = (
            candidate.preferred_roles[0].strip()
            if candidate.preferred_roles
            and candidate.preferred_roles[0].strip()
            else candidate.current_role
        )

        matched_jobs = self.matcher.match(
            candidate_role=search_role,
            candidate_skills=candidate.skills,
            candidate_locations=candidate.preferred_locations,
            candidate_experience=candidate.experience_years,
            jobs=jobs,
        )

        return matched_jobs