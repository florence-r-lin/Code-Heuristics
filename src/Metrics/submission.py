import ast
import HardMetrics
import fileParsing

class Submission:
    def __init__(self, path):
        self.path = path
        self.tree = self.make_tree()
        self.metrics_data = None  # to cache metrics dataclass if desired

    def make_tree(self):
        try:
            code = fileParsing.cleanParseFile(self.path)
            return ast.parse(code)
        except Exception as e:
            print(f"Error generating AST from '{self.path}': {e}")
            return None

    def get_path(self):
        return self.path
    
    def get_tree(self):
        return self.tree
    
    def get_metrics(self):
        if self.metrics_data is None:
            # Let's say allMetrics accepts path + tree and returns dataclass
            self.metrics_data = HardMetrics.allMetrics(self.path, tree=self.tree)
        return self.metrics_data
