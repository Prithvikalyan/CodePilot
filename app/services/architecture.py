
def build_architecture_prompt(user_request: str, project_context: dict):

    project_files = []

    for file in project_context["source_code"]:

        project_files.append(
            f"""
FILE: {file['file_path']}

CODE:
{file['content']}
"""
        )

    files_content = "\n".join(project_files)

    prompt = f"""
You are CodePilot, an AI Software Architecture Analyst.

Analyze the architecture of the supplied software project.

USER QUESTION:
{user_request}

PROJECT STRUCTURE:
{project_context['folder_structure']}

TOTAL FILES:
{project_context['total_files']}

SOURCE CODE:
{files_content}

ANALYSIS INSTRUCTIONS:

1. Identify the purpose of each relevant file.
2. Identify imports and dependencies between files.
3. Explain how the modules communicate.
4. Identify the main entry point, if visible.
5. Explain the execution flow step by step.
6. Distinguish actual dependencies from assumptions.
7. Do not invent modules or functionality.
8. Mention when the available source code is insufficient.

Provide a clear architecture explanation with headings,
file references and a simple execution flow.
"""

    return prompt
