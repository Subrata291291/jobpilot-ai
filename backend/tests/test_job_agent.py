from schemas.resume import CandidateProfile
from agents.job_agent import JobAgent


candidate = CandidateProfile(
    name="Subrata Haldar",
    current_role="Frontend Developer",
    experience_years=5,
    skills=[
        "React.js",
        "JavaScript",
        "TypeScript",
        "WordPress",
        "WooCommerce",
        "HTML5",
        "CSS3",
        "Tailwind CSS",
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


agent = JobAgent()

results = agent.run(candidate)


print("\nRecommended Jobs:")
print("================")

for job in results:

    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Location: {job['location']}")
    print(f"Skill Match: {job['skill_score']}%")
    print(f"Role Match: {job['role_score']}%")
    print(f"Location Match: {job['location_score']}%")
    print(f"Experience Match: {job['experience_score']}%")
    print(f"Overall Match: {job['match_score']}%")
    print(f"URL: {job['url']}")
    print("----------------")