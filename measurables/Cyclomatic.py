import ast

class CyclomaticComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.edges = 0
        self.nodes = 0
        self.decision_points = 0

    def generic_visit(self, node):
        self.nodes += 1
        super().generic_visit(node)

    def visit_If(self, node):
        self.decision_points += 1
        self.edges += 2  # Two edges: true and false branches
        self.generic_visit(node)

    def visit_For(self, node):
        self.decision_points += 1
        self.edges += 2  # Loop entry and exit
        self.generic_visit(node)

    def visit_While(self, node):
        self.decision_points += 1
        self.edges += 2  # Loop entry and exit
        self.generic_visit(node)

    def visit_And(self, node):
        self.decision_points += 1
        self.edges += 1
        self.generic_visit(node)

    def visit_Or(self, node):
        self.decision_points += 1
        self.edges += 1
        self.generic_visit(node)
    

def calculate_cyclomatic_complexity(source_code):
    tree = ast.parse(source_code)
    visitor = CyclomaticComplexityVisitor()
    visitor.visit(tree)

    # Each node implicitly has one entry edge
    visitor.edges += visitor.nodes
    complexity = visitor.edges - visitor.nodes + 2
    return complexity

#print(open("LOC.py", "r").read())
#print(calculate_cyclomatic_complexity(open("LOC.py", "r").read()))