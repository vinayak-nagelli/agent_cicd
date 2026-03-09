# patch_generator.py
import ast

def get_line_from_code(function_code, line_number):
    """
    Extract a specific line from the function.
    """
    lines = function_code.split("\n")
    if line_number <= len(lines):
        return lines[line_number - 1].rstrip()
    return None


def get_buggy_context(function_code, line_number, context=2):
    """
    Returns lines around the buggy line for LLM context.
    Default context is 2 lines above and below.
    """
    lines = function_code.split("\n")
    start = max(0, line_number - context - 1)
    end = min(len(lines), line_number + context)
    return "\n".join(lines[start:end])


def extract_buggy_line(function_code, ranked_lines):
    """
    Get the most suspicious line from bug_ranker.
    Returns line number and line text.
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
    multi_line=True,
    context_lines=2
):
    """
    Build LLM prompt with context for debugging.

    If multi_line=True, provide a few lines around the buggy line
    instead of only a single line.
    """

    if multi_line:
        buggy_context = get_buggy_context(function_code, line_number, context=context_lines)
        buggy_desc = f"Buggy code context (around line {line_number}):\n{buggy_context}"
    else:
        buggy_desc = f"Buggy line (line {line_number}): {buggy_line}"

    prompt = f"""
You are an automated debugging assistant.

A unit test failed.

Test code:
{test_code}

Function under test:
{function_name}

Full function code:
{function_code}

{buggy_desc}

AST analysis:
{ast_analysis}

Data flow analysis:
{data_flow}

Your task:
Fix ONLY the buggy code. 
You may update 1–5 lines if needed. 
Do NOT rewrite the entire function.
Do NOT change existing variable names, except if absolutely required for the fix.

Output format:
Provide modified lines in the format:
<line_number>: <new code>
For example:
6: result = x + y
7: temp = result * 1
"""

    return prompt