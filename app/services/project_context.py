from app.services.project_scanner import scan_project


def build_project_context(project_id: str):

    project_data = scan_project(project_id)

    files = project_data["files"]

    folder_structure = [
        file["file_path"]
        for file in files
    ]

    source_code = [
        {
            "file_path": file["file_path"],
            "content": file["content"],
        }
        for file in files
    ]

    total_files = len(files)

    total_lines = sum(
        len(file["content"].splitlines())
        for file in files
    )

    return {
        "project_id": project_data["project_id"],
        "project_name": project_data["project_name"],
        "project_path": project_data["project_path"],
        "folder_structure": folder_structure,
        "total_files": total_files,
        "total_lines": total_lines,
        "source_code": source_code,
        "skipped_files": project_data["skipped_files"],
        "skipped_file_details": project_data["skipped_file_details"],
    }