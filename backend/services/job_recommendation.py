from schemas.resume import CandidateProfile
from tools.job_search import JobSearchTool
from services.matcher import JobMatcher


class JobRecommendationService:

    def __init__(self):
        self.job_search = JobSearchTool()
        self.matcher = JobMatcher()

    def recommend(
        self,
        candidate: CandidateProfile,
    ) -> list[dict]:

        location = ""

        if candidate.preferred_locations:
            location = candidate.preferred_locations[0]

        jobs = self.job_search.search(
            role=candidate.current_role,
            skills=candidate.skills,
            location=location,
        )

        matched_jobs = self.matcher.match(
            candidate_skills=candidate.skills,
            jobs=jobs,
        )

        return matched_jobs