from schemas.resume import CandidateProfile
from services.job_recommendation import JobRecommendationService


candidate = CandidateProfile(
    name="Subrata Haldar",
    current_role="Frontend Developer",
    experience_years=5,
    skills=[
        "React.js",
        "JavaScript",
        "WordPress",
        "WooCommerce",
    ],
    education=[],
    preferred_roles=[
        "Frontend Developer",
        "React Developer",
    ],
    preferred_locations=[
        "Kolkata",
    ],
)


service = JobRecommendationService()

results = service.recommend(candidate)


print("\nRecommended Jobs:")
print("================")

for job in results:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Match Score: {job['match_score']}%")
    print(f"URL: {job['url']}")
    print("----------------")