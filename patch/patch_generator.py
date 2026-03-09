import ast


def get_line_from_code(function_code, line_number):
    """
    Extract a specific line from the function.
    """

    lines = function_code.split("\n")

    if line_number <= len(lines):
        return lines[line_number - 1].strip()

    return None


def extract_buggy_line(function_code, ranked_lines):
    """
    Get the most suspicious line from bug_ranker.
    """

    if not ranked_lines:
        return None, None

    top_bug = ranked_lines[0]

    line_number = top_bug["line"]

    buggy_line = get_line_from_code(function_code, line_number)

    return line_number, buggy_line


def build_patch_prompt(
    function_name,
    function_code,
    buggy_line,
    line_number,
    test_code,
    ast_analysis,
    data_flow,
):
    """
    Build LLM prompt with minimal context.
    """

    prompt = f"""
You are an automated debugging assistant.

A unit test failed.

Test code:
{test_code}

Function under test:
{function_name}

Full function code:
{function_code}

Buggy line suspected (line {line_number}):
{buggy_line}

AST analysis:
{ast_analysis}

Data flow analysis:
{data_flow}

Your task:
Fix ONLY the buggy line.

Rules:
- Do NOT rewrite the whole function.
- Do NOT change variable names.
- Only return the corrected line of code.

Output format:
corrected_line = <fixed line>
"""

    return prompt