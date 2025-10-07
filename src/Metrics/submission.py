import ast
import HardMetrics
import fileParsing

class Submission:
    def __init__(self, path):
        self.path = path
        self.tree = self.make_tree()

    def make_tree(self):
        try:
            code = fileParsing.cleanParseFile(self.path)
            return ast.parse(code)
        except Exception as e:
            print(f"Error generating AST from '{self.path}': {e}")
            return None
        

    def get_path(self):
        return self.path
    
    def tree():
        # getter for tree
        return "tree"
    
    # may add functionality for prof. bang's AST for every language here

    def metrics():
        # getter for metrics, will call HardMetrics and tree
        return "metrics"
