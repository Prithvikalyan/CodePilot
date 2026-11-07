import json
import re
from pathlib import Path

from app.config import (
    BASE_DIR,
    DATA_DIR,
    PROJECTS_REGISTRY_FILE,
    DEFAULT_PROJECT_ID,
)


def create_default_registry():
    """
    Create the initial registry without changing project folders.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    default_projects = [
        {
            "project_id": "sample_project",
            "name": "Sample Project",
            "path": str((BASE_DIR / "sample_project").resolve()),
        },
        {
            "project_id": "another_project",
            "name": "Another Project",
            "path": str((BASE_DIR / "another_project").resolve()),
        },
    ]

    existing_projects = [
        project for project in default_projects
        if Path(project["path"]).is_dir()
    ]

    save_projects(existing_projects)


def load_projects():
    """
    Read registered projects from the JSON registry.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not PROJECTS_REGISTRY_FILE.exists():
        create_default_registry()

    try:
        with PROJECTS_REGISTRY_FILE.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        projects = data.get("projects", [])

        if not isinstance(projects, list):
            raise ValueError("Invalid project registry format.")

        return projects

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            "Could not read the project registry."
        ) from error


def save_projects(projects):
    """
    Save the registered projects.
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    temporary_file = PROJECTS_REGISTRY_FILE.with_suffix(".tmp")

    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(
            {"projects": projects},
            file,
            indent=4
        )

    temporary_file.replace(PROJECTS_REGISTRY_FILE)


def get_available_projects():
    """
    Return projects for the frontend.
    """

    projects = load_projects()

    result = []

    for project in projects:
        project_path = Path(project["path"])

        result.append({
            "project_id": project["project_id"],
            "name": project["name"],
            "available": project_path.is_dir(),
        })

    return result


def get_project(project_id: str):
    """
    Find a registered project using its ID.
    """

    projects = load_projects()

    for project in projects:
        if project["project_id"] == project_id:
            return project

    raise ValueError("Project is not registered.")


def register_project(folder_path: str):
    """
    Register a folder selected by the user.
    """

    selected_path = Path(folder_path).expanduser().resolve(strict=True)

    if not selected_path.is_dir():
        raise ValueError("The selected path is not a folder.")

    projects = load_projects()

    # Prevent registering the same folder twice.
    for project in projects:

        existing_path = Path(project["path"]).resolve()

        if existing_path == selected_path:
            raise ValueError("This project is already registered.")

    # Generate a unique project ID.
    base_id = re.sub(
        r"[^a-z0-9]+",
        "_",
        selected_path.name.lower()
    ).strip("_")

    if not base_id:
        base_id = "project"

    existing_ids = {
        project["project_id"]
        for project in projects
    }

    project_id = base_id
    counter = 2

    while project_id in existing_ids:
        project_id = f"{base_id}_{counter}"
        counter += 1

    new_project = {
        "project_id": project_id,
        "name": selected_path.name,
        "path": str(selected_path),
    }

    projects.append(new_project)

    save_projects(projects)

    return {
        "project_id": project_id,
        "name": selected_path.name,
        "path": str(selected_path),
    }


def get_default_project():
    """
    Return the default project ID.
    """

    try:
        get_project(DEFAULT_PROJECT_ID)
        return DEFAULT_PROJECT_ID

    except ValueError:
        projects = load_projects()

        if not projects:
            raise ValueError("No projects are registered.")

        return projects[0]["project_id"]