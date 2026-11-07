from pathlib import Path

from app.config import (
    MAX_FILE_SIZE,
    SUPPORTED_EXTENSIONS,
    IGNORED_DIRECTORIES,
)

from app.services.project_registry import get_project


def scan_project(project_id: str):
    """
    Scan a registered project folder.
    """

    project = get_project(project_id)

    project_root = Path(project["path"]).resolve()

    if not project_root.exists():
        raise FileNotFoundError(
            f"Project folder not found: {project_root}"
        )

    if not project_root.is_dir():
        raise NotADirectoryError(
            f"Not a directory: {project_root}"
        )

    project_data = {
        "project_id": project["project_id"],
        "project_name": project["name"],
        "project_path": str(project_root),
        "files": [],
        "skipped_files": [],
        "skipped_file_details": [],
    }

    def record_skipped_file(file_path, reason):

        relative_path = str(
            file_path.relative_to(project_root)
        )

        project_data["skipped_files"].append(relative_path)

        project_data["skipped_file_details"].append({
            "file_path": relative_path,
            "reason": reason,
        })

    for file_path in project_root.rglob("*"):

        if file_path.is_symlink():
            record_skipped_file(
                file_path,
                "Symbolic links are not scanned"
            )
            continue

        relative_path = file_path.relative_to(project_root)

        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        try:
            resolved_path = file_path.resolve(strict=True)
            resolved_path.relative_to(project_root)

        except (OSError, RuntimeError, ValueError):
            record_skipped_file(
                file_path,
                "Path is outside the approved project folder "
                "or cannot be resolved"
            )
            continue

        if not resolved_path.is_file():
            continue

        if resolved_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            record_skipped_file(
                file_path,
                "Unsupported file extension"
            )
            continue

        try:
            if resolved_path.stat().st_size > MAX_FILE_SIZE:
                record_skipped_file(
                    file_path,
                    "File exceeds maximum allowed size"
                )
                continue

            with resolved_path.open("rb") as file:
                content_bytes = file.read(MAX_FILE_SIZE + 1)

            if len(content_bytes) > MAX_FILE_SIZE:
                record_skipped_file(
                    file_path,
                    "File exceeds maximum allowed size during reading"
                )
                continue

            if b"\x00" in content_bytes[:1024]:
                record_skipped_file(
                    file_path,
                    "Binary file detected"
                )
                continue

            content = content_bytes.decode("utf-8")

            project_data["files"].append({
                "file_path": str(relative_path),
                "content": content,
            })

        except UnicodeDecodeError:
            record_skipped_file(
                file_path,
                "File could not be decoded as UTF-8"
            )

        except OSError:
            record_skipped_file(
                file_path,
                "File could not be accessed or read"
            )

    return project_data