from langgraph.graph import StateGraph, START, END

from app.agent.state import CodePilotState

from app.agent.nodes import (
    classify_request,
    load_project_context,
    answer_project_question,
    analyze_architecture,
    review_code,
    validate_code_review,
    analyze_structure,
    generate_project_report,
    validate_project_report,
    )


def route_request(state: CodePilotState):

    if state["request_type"] == "project_qa":
        return "project_qa"

    elif state["request_type"] == "architecture":
        return "architecture"

    elif state["request_type"] == "code_review":
        return "code_review"

    elif state["request_type"] == "structure_review":
        return "structure_review"

    elif state["request_type"] == "project_report":
        return "project_report"

    return "not_implemented"


def pending_workflow(state: CodePilotState):

    return {
        "response": (
            f"The {state['request_type']} workflow "
            "has not been implemented yet."
        )
    }


def build_graph():

    workflow = StateGraph(CodePilotState)

    # Register nodes
    workflow.add_node("classify_request", classify_request)
    workflow.add_node("load_project_context", load_project_context)

    workflow.add_node(
        "answer_project_question",
        answer_project_question
    )

    workflow.add_node("analyze_architecture", analyze_architecture)
    workflow.add_node("review_code", review_code)

    workflow.add_node(
        "validate_code_review",
        validate_code_review
    )

    workflow.add_node("analyze_structure", analyze_structure)

    workflow.add_node(
        "generate_project_report",
        generate_project_report
    )
    workflow.add_node(
    "validate_project_report",
    validate_project_report
        )

    workflow.add_node("pending_workflow", pending_workflow)

    # Starting point
    workflow.add_edge(START, "classify_request")

    workflow.add_edge(
        "classify_request",
        "load_project_context"
    )

    # Route to the correct workflow
    workflow.add_conditional_edges(
        "load_project_context",
        route_request,
        {
            "project_qa": "answer_project_question",
            "architecture": "analyze_architecture",
            "code_review": "review_code",
            "structure_review": "analyze_structure",
            "project_report": "generate_project_report",
            "not_implemented": "pending_workflow",
        }
    )

    # Connect workflows to END
    workflow.add_edge("answer_project_question", END)
    workflow.add_edge("analyze_architecture", END)

    workflow.add_edge(
        "review_code",
        "validate_code_review"
    )

    workflow.add_edge("validate_code_review", END)
    workflow.add_edge("analyze_structure", END)
    workflow.add_edge(
    "generate_project_report",
    "validate_project_report"
)

    workflow.add_edge(
    "validate_project_report",
    END
)
    workflow.add_edge("pending_workflow", END)

    return workflow.compile()


codepilot_graph = build_graph()
