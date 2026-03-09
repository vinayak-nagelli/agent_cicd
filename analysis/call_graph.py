import ast
import os


class AdvancedCallGraphBuilder:
    """
    Builds an advanced repository-level call graph.

    Features:
    - Detects function calls
    - Detects class methods
    - Handles object.method() calls
    - Handles imports across files
    - Allows deep tracing of function dependencies
    """

    def __init__(self):
        self.call_graph = {}
        self.imports = {}

    # ---------------------------------------------
    # Parse imports to track cross-file references
    # ---------------------------------------------
    def _extract_imports(self, tree, file_path):

        imported_modules = []

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_modules.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                module = node.module
                if module:
                    imported_modules.append(module)

        self.imports[file_path] = imported_modules

    # ---------------------------------------------
    # Extract function calls inside functions
    # ---------------------------------------------
    def _extract_function_calls(self, node):

        called_functions = []

        for child in ast.walk(node):

            if isinstance(child, ast.Call):

                # case: direct function call
                if isinstance(child.func, ast.Name):
                    called_functions.append(child.func.id)

                # case: object.method() call
                elif isinstance(child.func, ast.Attribute):
                    called_functions.append(child.func.attr)

        return called_functions

    # ---------------------------------------------
    # Analyze single file
    # ---------------------------------------------
    def analyze_file(self, file_path):

        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        # extract imports
        self._extract_imports(tree, file_path)

        for node in ast.walk(tree):

            # normal functions
            if isinstance(node, ast.FunctionDef):

                func_name = node.name
                calls = self._extract_function_calls(node)

                self.call_graph[func_name] = calls

            # class methods
            elif isinstance(node, ast.ClassDef):

                class_name = node.name

                for body_item in node.body:

                    if isinstance(body_item, ast.FunctionDef):

                        method_name = f"{class_name}.{body_item.name}"

                        calls = self._extract_function_calls(body_item)

                        self.call_graph[method_name] = calls

    # ---------------------------------------------
    # Analyze entire repository
    # ---------------------------------------------
    def analyze_repository(self, repo_path):

        for root, dirs, files in os.walk(repo_path):

            for file in files:

                if file.endswith(".py"):

                    file_path = os.path.join(root, file)

                    try:
                        self.analyze_file(file_path)
                    except Exception as e:
                        print(f"Skipping {file_path}: {e}")

        return self.call_graph

    # ---------------------------------------------
    # Find deep dependency chain
    # ---------------------------------------------
    def trace_dependencies(self, start_function, visited=None):

        if visited is None:
            visited = set()

        if start_function in visited:
            return []

        visited.add(start_function)

        calls = self.call_graph.get(start_function, [])

        dependency_chain = []

        for func in calls:

            dependency_chain.append(func)

            deeper = self.trace_dependencies(func, visited)

            dependency_chain.extend(deeper)

        return dependency_chain

    # ---------------------------------------------
    # Detect recursive cycles
    # ---------------------------------------------
    def detect_cycles(self):

        cycles = []

        for func in self.call_graph:

            visited = set()

            path = self.trace_dependencies(func, visited)

            if func in path:
                cycles.append(func)

        return cycles


# -------------------------------------------------
# Helper functions used by agent.py
# -------------------------------------------------

def build_call_graph(repo_path):

    builder = AdvancedCallGraphBuilder()

    graph = builder.analyze_repository(repo_path)

    return graph


def find_related_functions(call_graph, function_name):

    builder = AdvancedCallGraphBuilder()

    builder.call_graph = call_graph

    return builder.trace_dependencies(function_name)


def detect_recursive_functions(call_graph):

    builder = AdvancedCallGraphBuilder()

    builder.call_graph = call_graph

    return builder.detect_cycles()