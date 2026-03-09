import ast


class DataFlowAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.assignments = {}
        self.returns = []
        self.operations = []
        self.variables_used = set()

    # -----------------------------
    # Track assignments
    # -----------------------------
    def visit_Assign(self, node):

        if isinstance(node.targets[0], ast.Name):

            var = node.targets[0].id

            value = ast.dump(node.value)

            self.assignments[var] = value

        self.generic_visit(node)

    # -----------------------------
    # Track variable usage
    # -----------------------------
    def visit_Name(self, node):

        self.variables_used.add(node.id)

    # -----------------------------
    # Track return values
    # -----------------------------
    def visit_Return(self, node):

        if node.value is not None:

            self.returns.append(ast.dump(node.value))

        self.generic_visit(node)

    # -----------------------------
    # Track arithmetic operations
    # -----------------------------
    def visit_BinOp(self, node):

        op_type = type(node.op).__name__

        left = ast.dump(node.left)
        right = ast.dump(node.right)

        self.operations.append({
            "operator": op_type,
            "left": left,
            "right": right
        })

        self.generic_visit(node)


def analyze_data_flow(function_code):

    tree = ast.parse(function_code)

    analyzer = DataFlowAnalyzer()

    analyzer.visit(tree)

    return {
        "assignments": analyzer.assignments,
        "operations": analyzer.operations,
        "returns": analyzer.returns,
        "variables_used": list(analyzer.variables_used)
    }