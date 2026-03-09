import os
import ast

CLONE_DIR = "cloned_repo"


def read_file(file_path):

    try:
        with open(file_path, "r") as f:
            return f.read()

    except Exception as e:
        print("Error reading file:", e)
        return None


def find_function_in_repo(function_name):

    for root, dirs, files in os.walk(CLONE_DIR):

        for file in files:

            if file.endswith(".py"):

                file_path = os.path.join(root, file)

                content = read_file(file_path)

                if content and f"def {function_name}(" in content:

                    return file_path

    return None


def extract_function_ast(file_path, function_name):

    try:

        with open(file_path, "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef) and node.name == function_name:

                start_line = node.lineno
                end_line = node.end_lineno

                with open(file_path, "r") as f:
                    lines = f.readlines()

                function_code = "".join(lines[start_line-1:end_line])

                return function_code

    except Exception as e:
        print("AST extraction error:", e)

    return None