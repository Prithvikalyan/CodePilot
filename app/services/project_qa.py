
def build_project_qa_prompt(user_request: str, project_context: dict):

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
You are CodePilot, an AI Project Analyst.

Your task is to answer questions about the user's software project.

USER QUESTION:
{user_request}

PROJECT INFORMATION:

Project path:
{project_context['project_path']}

Total files:
{project_context['total_files']}

Total lines:
{project_context['total_lines']}

PROJECT SOURCE CODE:
{files_content}

INSTRUCTIONS:

1. Answer using the supplied project information.
2. Explain technical concepts in simple language.
3. Refer to relevant filenames when explaining.
4. Do not invent features or functionality.
5. If the supplied code does not contain enough
   information, clearly mention that.
6. Explain how the relevant files work together
   when appropriate.

Provide a clear and structured answer.
"""

    return prompt
