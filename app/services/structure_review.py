def build_structure_review_prompt(user_request: str, project_context: dict):

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
You are CodePilot, a Software Project Structure Analyst.

USER REQUEST:
{user_request}

CURRENT PROJECT STRUCTURE:
{project_context['folder_structure']}

TOTAL FILES:
{project_context['total_files']}

SOURCE CODE:
{files_content}

ANALYSIS INSTRUCTIONS:

1. Evaluate the current structure based on project size and complexity.
2. Identify files whose responsibilities appear misplaced or mixed.
3. Identify duplicated functionality only when supported by the code.
4. Explain dependencies between files.
5. Recommend a better structure only when it provides a meaningful benefit.
6. Do not impose enterprise architecture on small projects.
7. Preserve existing functionality.
8. Explain where existing files should move, if restructuring is needed.
9. Do not invent modules, features, or dependencies.
10. Clearly distinguish actual problems from optional recommendations.
11. If the current structure is suitable, say so.
12. Do not modify or execute project files.
13. Do not assume that a file is unnecessary just because
    it is not imported by another scanned file.

14. Distinguish between:
    - Not imported within the scanned project
    - Potentially unused code
    - Confirmed unnecessary code

15. Do not rename a file when its current name accurately
    describes its main responsibility.

16. Do not move functions into database.py simply because
    they work with user data. Consider whether the function
    belongs to business logic or data access.

17. Prefer keeping the existing structure when the benefits
    of restructuring are unclear.

18. Never recommend deleting a file without strong evidence
    and an explanation of the consequences.
    
REPORT FORMAT:

# Structure Review Summary

# Current Structure Assessment

# Findings

# Recommended Structure

# File Movement Explanation

# Migration Considerations

# Final Recommendation

Use clear, beginner-friendly explanations.
"""

    return prompt