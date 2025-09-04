import ast

def countLoops(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))

print(countLoops('/Users/summer-2024/Desktop/code metrics 25/All-Data/CS35-Data/assignments postllm/submissions_cs35_sp2025/Jerry Qiao/final|hw1pr1 JQ.py'))