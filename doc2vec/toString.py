import re
import ast

class StringFormat:
    
    def __init__(self, path):
        self.path = path
        self.funcList = self.splitFunc(self.path) # is a list of functions with comments
        self.noComments = self.removeComments(self.funcList) #still a list no comments
        self.finalString = self.removeTabNewLn(self.noComments)  

    def removeComments(self, scriptLst):
        noComments = []
        for i in scriptLst:
            multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\"" # gets all docstrings
            i = re.sub(multiLine, "", i) # replaces all docstrings with an emptystring
            i = re.sub("#.*","",i) #replaces everything that has a comment with an emptystring
            noComments.append(i)
        return noComments
    
    def removeTabNewLn(self, noCommentLst):
        noTabLn = []
        for i in noCommentLst:
            i = re.sub("[\t+\n]", "", i)
            noTabLn.append(i)
        return noTabLn
    
    
    def getFunctionSource(self, scriptPath, func_node):
        with open(scriptPath, "r") as file:
            lines = file.readlines()

        start_line = func_node.lineno - 1
        end_line = func_node.end_lineno

        return "".join(lines[start_line:end_line])

    def splitFunc(self, scriptPath):
        funcList = []
        functions = self.findFunctionsInScript(scriptPath)
        for func in functions:
            funcList.append(self.getFunctionSource(scriptPath, func))
        return funcList
    
    def findFunctionsInScript(self, scriptPath):
        with open(scriptPath, "r") as file:
            tree = ast.parse(file.read(), filename=scriptPath)

        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return functions
    
# noStringScript = StringFormat("CodeMeasure/LOC.py")
# print(noStringScript.finalString)
