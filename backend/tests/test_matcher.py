from services.matcher import JobMatcher


matcher = JobMatcher()

candidate_skills = [
    "React.js",
    "JavaScript",
    "WordPress",
    "WooCommerce",
]

jobs = [
    {
        "title": "Frontend Developer",
        "company": "Tech Solutions",
        "location": "Kolkata",
        "skills": [
            "React.js",
            "JavaScript",
            "HTML5",
            "CSS3",
        ],
    },
    {
        "title": "WordPress Developer",
        "company": "Web Agency",
        "location": "Remote",
        "skills": [
            "WordPress",
            "WooCommerce",
            "JavaScript",
            "PHP",
        ],
    },
]

results = matcher.match(
    candidate_skills,
    jobs,
)

print("\nJob Matches:")
print("================")

for job in results:
    print(f"Title: {job['title']}")
    print(f"Company: {job['company']}")
    print(f"Match Score: {job['match_score']}%")
    print("----------------")