
from app.services.project_context import build_project_context

from app.services.architecture import build_architecture_prompt
from app.services.code_review import build_code_review_prompt

from app.services.project_qa import build_project_qa_prompt
from app.services.llm import ask_llm
from app.services.review_validator import build_review_validation_prompt
from app.services.structure_review import build_structure_review_prompt

from app.services.project_report import build_project_report_prompt

from app.services.project_report_validator import (
    build_project_report_validation_prompt
)



def classify_request(state: dict):
    user_request = state["user_request"].lower()

    if any(word in user_request for word in [
        "project report",
        "overall report",
        "project summary",
        "recommendations",
    ]):
        request_type = "project_report"

    elif any(word in user_request for word in [
        "architecture",
        "modules",
        "connect",
    ]):
        request_type = "architecture"

    elif any(word in user_request for word in [
        "structure",
        "organize",
        "folder layout",
    ]):
        request_type = "structure_review"

    elif any(word in user_request for word in [
        "bug",
        "error",
        "code review",
        "review code",
        "issue",
    ]):
        request_type = "code_review"

    else:
        request_type = "project_qa"

    return {"request_type": request_type}


def load_project_context(state: dict):

    project_id = state["project_id"]

    project_context = build_project_context(project_id)

    return {
        "project_context": project_context
    }



def answer_project_question(state: dict):

    # Get the user's question
    user_request = state["user_request"]

    # Get the scanned project information
    project_context = state["project_context"]

    # Prepare the prompt
    prompt = build_project_qa_prompt(
        user_request,
        project_context
    )

    # Send prompt to NVIDIA
    response = ask_llm(prompt)

    # Return AI-generated answer
    return {
        "response": response
    }


def analyze_architecture(state: dict):
    user_request = state["user_request"]
    project_context = state["project_context"]

    prompt = build_architecture_prompt(
        user_request,
        project_context
    )

    response = ask_llm(prompt)

    return {
        "response": response
    }


def review_code(state: dict):
    user_request = state["user_request"]
    project_context = state["project_context"]

    prompt = build_code_review_prompt(
        user_request,
        project_context
    )

    response = ask_llm(prompt)

    return {
        "response": response
    }


def validate_code_review(state: dict):
    user_request = state["user_request"]
    project_context = state["project_context"]
    initial_review = state["response"]

    prompt = build_review_validation_prompt(
        user_request,
        project_context,
        initial_review
    )

    validated_response = ask_llm(prompt)

    return {
        "response": validated_response
    }


def analyze_structure(state: dict):
    user_request = state["user_request"]
    project_context = state["project_context"]

    prompt = build_structure_review_prompt(
        user_request,
        project_context
    )

    response = ask_llm(prompt)

    return {"response": response}


def generate_project_report(state: dict):
    """
    Generate an overall project report with recommendations.
    """

    project_context = state["project_context"]

    prompt = build_project_report_prompt(project_context)

    response = ask_llm(prompt)

    return {
        "response": response
    }


def validate_project_report(state: dict):
    """
    Validate the generated project report against actual source code.
    """

    project_context = state["project_context"]
    initial_report = state["response"]

    prompt = build_project_report_validation_prompt(
        project_context,
        initial_report
    )

    validated_report = ask_llm(prompt)

    return {
        "response": validated_report
    }