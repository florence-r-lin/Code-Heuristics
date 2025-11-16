import ast

def countLoops(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))