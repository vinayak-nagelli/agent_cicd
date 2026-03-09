import ast


def analyze_function_structure(function_code):

    tree = ast.parse(function_code)

    analysis = {
        "function": None,
        "arguments": [],
        "variables": set(),
        "operators": [],
        "calls": [],
        "returns": [],
        "conditions": 0,
        "loops": 0
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            analysis["function"] = node.name

            for arg in node.args.args:
                analysis["arguments"].append(arg.arg)

        elif isinstance(node, ast.Name):

            analysis["variables"].add(node.id)

        elif isinstance(node, ast.BinOp):

            analysis["operators"].append(type(node.op).__name__)

        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):
                analysis["calls"].append(node.func.id)

        elif isinstance(node, ast.Return):

            analysis["returns"].append(node.lineno)

        elif isinstance(node, ast.If):

            analysis["conditions"] += 1

        elif isinstance(node, (ast.For, ast.While)):

            analysis["loops"] += 1

    analysis["variables"] = list(analysis["variables"])

    return analysis