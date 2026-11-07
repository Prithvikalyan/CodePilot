
def build_project_report_validation_prompt(
    project_context: dict,
    initial_report: str
):
    """
    Build a validation prompt for the overall project report.
    """

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
You are CodePilot's Senior Project Report Validator.

Your job is to verify and improve an initial AI-generated
Project Summary and Recommendations report.

ACTUAL PROJECT INFORMATION:

Project Path:
{project_context.get("project_path", "Not available")}

Total Files:
{project_context.get("total_files", 0)}

Total Lines:
{project_context.get("total_lines", 0)}

ACTUAL PROJECT SOURCE CODE:
{files_content}

INITIAL PROJECT REPORT:
{initial_report}


VALIDATION INSTRUCTIONS:

1. Verify project descriptions against the actual source code.

2. Verify that identified strengths are supported by evidence.

3. Remove weaknesses that are unsupported or incorrect.

4. Check whether technical risks are realistic and relevant.

5. Distinguish confirmed issues from potential risks.

6. Verify that recommendations address actual project
   limitations.

7. Remove unnecessary recommendations that would make
   the project unnecessarily complicated.

8. Ensure priorities (High, Medium, Low) are reasonable.

9. Do not invent files, functions, technologies,
   dependencies or project functionality.

10. Do not claim that a file or function is unused unless
    the available project evidence supports that conclusion.

11. Do not recommend deleting or modifying functionality
    without sufficient evidence.

12. Keep explanations beginner-friendly and practical.

13. Preserve useful findings from the initial report.

14. Correct inaccurate or misleading statements.

15. If information is unavailable, explicitly mention
    that limitation.


REQUIRED REPORT SECTIONS:

# CodePilot Project Report

## 1. Project Overview

## 2. Project Strengths

## 3. Project Weaknesses

## 4. Technical Risks

## 5. Recommended Improvements

## 6. Overall Project Assessment


FINAL INSTRUCTIONS:

- Include all six required sections.
- Ensure recommendations are actionable.
- Clearly distinguish confirmed findings from potential risks.
- Do not invent information.
- Return the complete corrected report.

"""

    return prompt
