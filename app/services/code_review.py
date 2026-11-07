def build_code_review_prompt(
    user_request: str,
    project_context: dict
):
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
You are CodePilot, an experienced Python Code Reviewer.

Your task is to review the supplied software project.

USER REQUEST:
{user_request}

PROJECT STRUCTURE:
{project_context['folder_structure']}

SOURCE CODE:
{files_content}

REVIEW INSTRUCTIONS:

1. Identify genuine bugs and potential runtime errors.
2. Identify security and performance problems when supported by evidence.
3. Identify maintainability and code-quality improvements separately.
4. Explain why each issue matters.
5. Provide a suggested fix for every finding.
6. Refer to the exact file containing the issue.
7. Include the relevant code as evidence.
8. Give a line number when it can be determined reliably.
9. Assign severity: Critical, High, Medium, or Low.
10. Do not invent bugs or unsupported problems.
11. Do not report normal coding choices as bugs.
12. If no issues are found, clearly state that.
13. Do not modify or execute any project files.

REPORT FORMAT:

# Code Review Summary

Briefly summarize the review.

# Findings

For each finding, provide:

- File:
- Line:
- Severity:
- Category:
- Problem:
- Evidence:
- Why it matters:
- Suggested fix:

# Code Quality Improvements

List optional improvements separately from bugs.

# Final Assessment

Summarize the overall code quality and important risks.

Use clear, beginner-friendly explanations.
"""

    return prompt