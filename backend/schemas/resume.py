from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    filename: str
    size: int
    status: str
    message: str


class CandidateProfile(BaseModel):
    name: str = ""
    current_role: str = ""
    experience_years: float = 0

    skills: list[str] = Field(default_factory=list)

    education: list[str] = Field(default_factory=list)

    preferred_roles: list[str] = Field(default_factory=list)

    preferred_locations: list[str] = Field(default_factory=list)


class ResumeAnalyzeResponse(BaseModel):
    filename: str
    profile: CandidateProfile