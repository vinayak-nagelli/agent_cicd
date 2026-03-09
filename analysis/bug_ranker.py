import ast


class SuspiciousLineDetector(ast.NodeVisitor):

    def __init__(self):
        self.scores = []

    def visit_BinOp(self, node):

        score = 0

        op_type = type(node.op).__name__

        # suspicious arithmetic
        if op_type in ["Sub", "Div"]:
            score += 3

        # redundant arithmetic
        if op_type in ["Add", "Mult"]:
            if isinstance(node.right, ast.Constant):

                if node.right.value in [0, 1]:
                    score += 2

        line = node.lineno

        self.scores.append({
            "line": line,
            "operator": op_type,
            "score": score
        })

        self.generic_visit(node)


def rank_buggy_lines(function_code):

    tree = ast.parse(function_code)

    detector = SuspiciousLineDetector()

    detector.visit(tree)

    ranked = sorted(detector.scores, key=lambda x: x["score"], reverse=True)

    return ranked