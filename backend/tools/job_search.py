from typing import Any


class JobSearchTool:
    """
    Job search tool.

    This version uses sample jobs so we can test
    the JobPilot architecture before connecting
    a real job-search API.
    """

    def search(
        self,
        role: str = "",
        skills: list[str] | None = None,
        location: str = "",
    ) -> list[dict[str, Any]]:

        skills = skills or []

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
                "experience": "3-5 years",
                "url": "https://example.com/job/1",
            },
            {
                "title": "React Developer",
                "company": "Digital Labs",
                "location": "Kolkata",
                "skills": [
                    "React.js",
                    "JavaScript",
                    "TypeScript",
                    "REST API",
                ],
                "experience": "2-4 years",
                "url": "https://example.com/job/2",
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
                "experience": "3-5 years",
                "url": "https://example.com/job/3",
            },
        ]

        results = []

        role_lower = role.lower()
        location_lower = location.lower()

        for job in jobs:

            job_title = job["title"].lower()
            job_location = job["location"].lower()

            role_match = (
                not role
                or role_lower in job_title
                or job_title in role_lower
            )

            location_match = (
                not location
                or location_lower in job_location
                or job_location == "remote"
            )

            skill_match = (
                not skills
                or any(
                    skill.lower() in [
                        job_skill.lower()
                        for job_skill in job["skills"]
                    ]
                    for skill in skills
                )
            )

            if role_match and location_match and skill_match:
                results.append(job)

        return results