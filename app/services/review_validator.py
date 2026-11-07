def build_review_validation_prompt(
    user_request: str,
    project_context: dict,
    initial_review: str
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
You are CodePilot's Senior Code Review Validator.

Your job is to verify the findings produced by an initial
AI code reviewer.

USER REQUEST:
{user_request}

ACTUAL PROJECT SOURCE CODE:
{files_content}

INITIAL CODE REVIEW:
{initial_review}

VALIDATION INSTRUCTIONS:

1. Verify every finding against the actual source code.
2. Remove findings that are unsupported or incorrect.
3. Distinguish confirmed bugs, potential bugs,
   context-dependent behavior, and optional improvements.

4. Do not classify implicit None returns as bugs
   automatically. Python functions legitimately return None
   when no explicit return statement is executed.

5. Only classify a missing return as a confirmed bug when
   the available code demonstrates that the caller requires
   a different return value or incorrectly uses None.

6. If caller behavior is unavailable, classify the issue
   as context-dependent rather than a confirmed bug.
7. Check whether the suggested fixes are correct.
8. Correct inaccurate line numbers when possible.
9. Review whether severity is appropriate.
10. Do not invent new issues without code evidence.
11. Do not assume intended behavior without evidence.
12. Clearly explain any uncertain findings.

OUTPUT:

# Validated Code Review

# Confirmed Findings

# Rejected or Modified Findings

# Additional Notes

# Final Assessment

Return a clear, accurate and beginner-friendly report.
"""

    return prompt


