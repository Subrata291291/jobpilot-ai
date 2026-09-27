class JobMatcher:
    """
    Matches a candidate with jobs using:
    - Skill match
    - Role match
    - Location match
    - Experience match
    """

    def normalize(self, value: str) -> str:
        return value.lower().strip()

    def calculate_skill_match(
        self,
        candidate_skills: list[str],
        job_skills: list[str],
    ) -> float:

        if not candidate_skills or not job_skills:
            return 0.0

        candidate = {
            self.normalize(skill)
            for skill in candidate_skills
        }

        job = {
            self.normalize(skill)
            for skill in job_skills
        }

        matched = candidate.intersection(job)

        return round(
            (len(matched) / len(job)) * 100,
            2,
        )

    def calculate_role_match(
        self,
        candidate_role: str,
        job_title: str,
    ) -> float:

        if not candidate_role or not job_title:
            return 0.0

        candidate_role = self.normalize(candidate_role)
        job_title = self.normalize(job_title)

        if candidate_role in job_title:
            return 100.0

        candidate_words = set(candidate_role.split())
        job_words = set(job_title.split())

        matched_words = candidate_words.intersection(
            job_words
        )

        if not candidate_words:
            return 0.0

        return round(
            (len(matched_words) / len(candidate_words)) * 100,
            2,
        )

    def calculate_location_match(
        self,
        preferred_locations: list[str],
        job_location: str,
    ) -> float:

        if not preferred_locations or not job_location:
            return 0.0

        job_location = self.normalize(job_location)

        for location in preferred_locations:

            location = self.normalize(location)

            if (
                location in job_location
                or job_location in location
                or "remote" in job_location
            ):
                return 100.0

        return 0.0

    def calculate_experience_match(
        self,
        candidate_experience: float,
        job_experience: str,
    ) -> float:

        if not job_experience:
            return 50.0

        import re

        text = job_experience.lower().strip()

        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            text,
        )

        if not numbers:
            return 50.0

        values = [
            float(number)
            for number in numbers
        ]

        # Example: "3+ years"
        if "+" in text and len(values) == 1:

            minimum = values[0]

            if candidate_experience >= minimum:
                return 100.0

            difference = minimum - candidate_experience

            if difference <= 1:
                return 75.0

            if difference <= 2:
                return 50.0

            return 25.0

        # Example: "3-5 years"
        if len(values) >= 2:

            minimum = values[0]
            maximum = values[1]

            if minimum <= candidate_experience <= maximum:
                return 100.0

            if candidate_experience < minimum:
                difference = minimum - candidate_experience
            else:
                difference = candidate_experience - maximum

        # Example: "5 years"
        else:

            minimum = values[0]

            if candidate_experience >= minimum:
                return 100.0

            difference = minimum - candidate_experience

        if difference <= 1:
            return 75.0

        if difference <= 2:
            return 50.0

        return 25.0

    def match(
        self,
        candidate_role: str,
        candidate_skills: list[str],
        candidate_locations: list[str],
        candidate_experience: float,
        jobs: list[dict],
    ) -> list[dict]:

        matched_jobs = []

        for job in jobs:

            skill_score = self.calculate_skill_match(
                candidate_skills,
                job.get("skills", []),
            )

            role_score = self.calculate_role_match(
                candidate_role,
                job.get("title", ""),
            )

            location_score = self.calculate_location_match(
                candidate_locations,
                job.get("location", ""),
            )

            experience_score = self.calculate_experience_match(
                candidate_experience,
                job.get("experience", ""),
            )

            overall_score = round(
                (
                    skill_score * 0.40
                    + role_score * 0.30
                    + location_score * 0.20
                    + experience_score * 0.10
                ),
                2,
            )

            matched_job = {
                **job,
                "skill_score": skill_score,
                "role_score": role_score,
                "location_score": location_score,
                "experience_score": experience_score,
                "match_score": overall_score,
            }

            matched_jobs.append(matched_job)

        matched_jobs.sort(
            key=lambda job: job["match_score"],
            reverse=True,
        )

        return matched_jobs