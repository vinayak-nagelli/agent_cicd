import re
import os
from debugging.source_locator import (
    read_file,
    find_function_in_repo,
    extract_function_ast
)
from analysis.ast_analyzer import analyze_function_structure
from analysis.call_graph import build_call_graph, find_related_functions
from analysis.data_flow import analyze_data_flow
from analysis.bug_ranker import rank_buggy_lines

from patch.patch_generator import extract_buggy_line, build_patch_prompt


CLONE_DIR = "cloned_repo"

CALL_GRAPH = build_call_graph(CLONE_DIR)

def extract_test_function(file_content, test_name):

    pattern = rf"def {test_name}\(.*?\):(.*?)(?=\ndef|\Z)"

    match = re.search(pattern, file_content, re.S)

    if match:
        return match.group(0)

    return None


def extract_function_name(test_code):

    match = re.search(r"assert\s+(\w+)\(", test_code)

    if match:
        return match.group(1)

    return None


def parse_test_failures(output):

    print("\nAnalyzing test failures\n")

    failures = re.findall(r"FAILED\s+([^\s]+)::([^\s]+)", output)

    results = []

    for failure in failures:

        file_name = failure[0]
        test_name = failure[1]

        print("Test:", test_name)
        print("File:", file_name)
        print("-" * 30)

        results.append({
            "file": file_name,
            "test": test_name
        })

    for failure in results:

        path = os.path.join(CLONE_DIR, failure["file"])

        content = read_file(path)

        test_code = extract_test_function(content, failure["test"])

        print("\nTest Function Code:\n")
        print(test_code)

        function_name = extract_function_name(test_code)

        print("\nFunction Under Test:", function_name)

        source_file = find_function_in_repo(function_name)

        print("Source File:", source_file)

        source_function = extract_function_ast(source_file, function_name)

        print("\nSource Function Code:\n")
        print(source_function)

        analysis = analyze_function_structure(source_function)

        print("\nAST Analysis:\n")
        print(analysis)

        # CALL GRAPH STEP
        print("\nCall Graph Analysis:\n")
        related_functions = find_related_functions(CALL_GRAPH, function_name)
        print("Functions called inside", function_name, ":")
        print(related_functions)

        # DATA FLOW
        data_flow = analyze_data_flow(source_function)

        print("\nData Flow Analysis:\n")
        print(data_flow)


        # BUG RANKING
        ranked_lines = rank_buggy_lines(source_function)

        print("\nSuspicious Lines Ranking:\n")
        print(ranked_lines)
        line_number, buggy_line = extract_buggy_line(source_function, ranked_lines)

        print("\nMost Suspicious Line:")
        print("Line:", line_number)
        print("Code:", buggy_line)

        prompt = build_patch_prompt(
        function_name,
        source_function,
        buggy_line,
        line_number,
        test_code,
        analysis,
        data_flow
            )
        print("\nGenerated LLM Prompt:\n")
        print(prompt)





    return results