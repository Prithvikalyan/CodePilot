import logging
import tkinter as tk

from tkinter import filedialog

from fastapi import APIRouter, HTTPException, Query

from app.schemas.analysis import AnalysisRequest
from app.agent.graph import codepilot_graph

from app.services.project_registry import (
    get_available_projects,
    register_project,
    get_default_project,
)

from app.services.project_scanner import scan_project


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/projects")
def list_projects():
    """
    List all registered projects.
    """

    return {
        "projects": get_available_projects()
    }


@router.post("/projects/add")
def add_project():
    """
    Open the local computer's folder picker
    and register the selected project.
    """

    root = None

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_folder = filedialog.askdirectory(
            title="Select a project folder",
            mustexist=True,
        )

        if not selected_folder:
            return {
                "message": "Project selection cancelled.",
                "cancelled": True,
            }

        project = register_project(selected_folder)

        return {
            "message": "Project added successfully.",
            "cancelled": False,
            "project": project,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception("Could not add project.")

        raise HTTPException(
            status_code=500,
            detail="Could not add the selected project."
        )

    finally:
        if root is not None:
            root.destroy()


@router.get("/scan-project")
def scan_selected_project(
    project_id: str = Query(default=None)
):
    """
    Scan the selected registered project.
    """

    try:
        if not project_id:
            project_id = get_default_project()

        project_data = scan_project(project_id)

        return {
            "message": "Project scanned successfully",
            "project_id": project_data["project_id"],
            "project_name": project_data["project_name"],
            "project_path": project_data["project_path"],
            "total_files": len(project_data["files"]),
            "files": [
                file["file_path"]
                for file in project_data["files"]
            ],
            "skipped_files": project_data["skipped_files"],
            "skipped_file_details": (
                project_data["skipped_file_details"]
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except (FileNotFoundError, NotADirectoryError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception("Project scanning failed.")

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while scanning."
        )


@router.post("/analyze")
def analyze_project(request: AnalysisRequest):
    """
    Analyze the selected registered project.
    """

    try:
        initial_state = {
            "user_request": request.user_request,
            "project_id": request.project_id,
            "request_type": None,
            "project_context": None,
            "response": None,
            "error": None,
        }

        result = codepilot_graph.invoke(initial_state)

        if result.get("error"):
            raise HTTPException(
                status_code=500,
                detail="Project analysis failed."
            )

        context = result["project_context"]

        return {
            "user_request": result["user_request"],
            "project_id": result["project_id"],
            "request_type": result["request_type"],
            "project_summary": {
                "project_name": context["project_name"],
                "total_files": context["total_files"],
                "total_lines": context["total_lines"],
                "folder_structure": context["folder_structure"],
            },
            "response": result["response"],
        }

    except HTTPException:
        raise

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except (FileNotFoundError, NotADirectoryError) as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception:
        logger.exception(
            "Unexpected error during project analysis."
        )

        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred during project analysis."
        )