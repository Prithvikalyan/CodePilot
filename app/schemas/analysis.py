from pydantic import BaseModel, Field, field_validator

from app.config import DEFAULT_PROJECT_ID


class AnalysisRequest(BaseModel):

    user_request: str = Field(min_length=1)

    project_id: str = Field(
        default=DEFAULT_PROJECT_ID,
        min_length=1
    )

    @field_validator("user_request", mode="before")
    @classmethod
    def strip_user_request(cls, value):

        if isinstance(value, str):
            return value.strip()

        return value

    @field_validator("project_id", mode="before")
    @classmethod
    def strip_project_id(cls, value):

        if isinstance(value, str):
            return value.strip()

        return value