from typing import TypedDict, Optional


class CodePilotState(TypedDict):

    # User's question
    user_request: str

    # Selected approved project
    project_id: str

    # Request category
    request_type: Optional[str]

    # Information collected from the selected project
    project_context: Optional[dict]

    # AI-generated response
    response: Optional[str]

    # Errors, if any
    error: Optional[str]