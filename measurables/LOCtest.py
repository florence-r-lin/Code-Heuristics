import re  
import ast
from Cyclomatic import *
from NestedDepth import CallChain 


def commentCheck(comment): #fix becauyse it works now
    #hashtags = "\#[^\n\r]+?(?:[\n\r])"   # is the actual solution
    hashtags = "[\#]" # is the very temporary solution until I figure out how to get the actual solution to work
    if re.search(hashtags, comment):
        return comment
    else:
        return ""
    #print(commentCheck("#will this work"))
    #print(commentCheck("we will see"))

def removeComments(fullScript):
    multiLine = "\'\'\'[^']*\'\'\'|\"\"\"[^\"]*\"\"\"" # gets all docstrings
    fullScript = re.sub(multiLine, "", fullScript) # replaces all docstrings with an emptystring
    fullScript = re.sub("#.*","",fullScript) #replaces everything that has a comment with an emptystring
    return fullScript

def findFunctionsInScript(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

def getFunctionSource(scriptPath, func_node):
    with open(scriptPath, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])

def splitFunc(scriptPath):
    funcList = []
    functions = findFunctionsInScript(scriptPath)
    for func in functions:
        funcList.append(getFunctionSource(scriptPath, func))
    return funcList

def funcName(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    function_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return function_names
    # tempList = []
    # ansList = []
    # getNames = "(def +[a-zA-Z_]+( [^(]+)*)" #gets only the def (name)
    # for i in fullScript:
    #     if re.search(getNames, i):
    #         tempList.append(i)
    # for n, i in enumerate(tempList):
    #     parsedFuncName = i.split("(")[0]
    #     parsedFuncName = re.sub(" ","", parsedFuncName)
    #     ansList.append(parsedFuncName[3:]) #parses out the variable and the "def ", giving only the variable name
    # return ansList
    

def containsString(str, noCommentScriptStr):
    wordScript = noCommentScriptStr.split(" ")
    for i in wordScript:
        if re.search(str, i):
            return True
    return False

# def findIfOrVar(noCommentScriptStr):
#     return containsString("if|=", noCommentScriptStr)

# def findBoolAlg(noCommentScriptStr):
#     return containsString("and|or|not|", noCommentScriptStr)

# def findDictionaries(noCommentScriptStr):
#     return containsString("\{(?:[^{}]|)*\}", noCommentScriptStr)

# def findSlicing(noCommentScriptStr):
#     return containsString("\[.*:.*\]", noCommentScriptStr)

# def findNestedLoops(scriptPath):
#     with open(scriptPath, "r") as file:
#         tree = ast.parse(file.read(), filename=scriptPath)

#     for node in ast.walk(tree):
#         if isinstance(node, (ast.For, ast.While)):
#             for child in ast.iter_child_nodes(node):
#                 if isinstance(child, (ast.For, ast.While)):
#                     return True
#     return False


# def findLoops(scriptPath):
#     with open(scriptPath, "r") as file:
#         tree = ast.parse(file.read(), filename=scriptPath)

#     for node in ast.walk(tree):
#         if isinstance(node, (ast.For, ast.While)):
#             return True
#     return False
        
# def findRecursion(scriptPath):
#     #split into functions, then find function name within the functions
#     #def whitespace word (anything ) colon
#     totalScriptList = []
#     inputFile = open(scriptPath, "r")
#     for x in inputFile:
#         totalScriptList.append(x)
#     names = funcName(totalScriptList)
#     for n, i in enumerate(splitFunc(scriptPath)):
#         if i.count(names[n]) > 1:
#             return True
#     return False

# def findListComp(noCommentScriptStr):
#     # return containsString("\[.*for.*in.*\]", noCommentScriptStr)
#     tree = ast.parse(noCommentScriptStr)
#     for node in ast.walk(tree):
#         if isinstance(node, ast.ListComp):
#             return True
#     return False
    
# def findOop(scriptPath):
#     with open(scriptPath, "r") as file:
#         tree = ast.parse(file.read(), filename=scriptPath)
#     hasClass = False
#     hasMethod = False

#     for node in ast.walk(tree):
#         if isinstance(node, ast.ClassDef):
#             hasClass = True
#             for child in node.body:
#                 if isinstance(child, ast.FunctionDef):
#                     hasMethod = True

#     return hasClass and hasMethod

# def sumTests(boolList):
#     total = 0
#     for i in boolList:
#         if i:
#             total = total+1
#     return total


commentList = []
totalScriptList = []


# CHANGE THE SCRIPT HERE
# ---------------------------
scriptPath = "CodeMeasure/LOC.py"
# ---------------------------


inputfile = open(scriptPath, "r")
inputfiletest2 = open(scriptPath, "r")
noCommentsinputfile = removeComments(inputfiletest2.read())
for x in inputfile:
    totalScriptList.append(x)
    commentList.append(commentCheck(x))

# for i in splitFunc(scriptPath):
#     print(i)
commentList = [z for z in commentList if z != ""]

def bold_colored_text(text, color_code):
    return f"\033[1;{color_code}m{text}\033[0m"

# Color codes
COLOR_BLUE = 34
COLOR_GREEN = 32
COLOR_RED = 31

alignment_width = 43  # Adjusted width for alignment

def color_boolean(value):
    return bold_colored_text(value, COLOR_GREEN if value else COLOR_RED)

# print(f"{'The total LOC is:':<{alignment_width}}" + bold_colored_text(len(totalScriptList), COLOR_BLUE))
# print(f"{'The Cyclomatic Complexity is:':<{alignment_width}}" + bold_colored_text(CyclomaticChicanery(noCommentsinputfile), COLOR_GREEN))
#
# comment_percentage = (1 - (len(noCommentsinputfile) / len(open(scriptPath, "r").read()))) * 100
# print(f"{'The percentage comments is:':<{alignment_width}}" + bold_colored_text(f"{comment_percentage:.3f} %", COLOR_BLUE))
#
# print(f"{'There are functions present:':<{alignment_width}}" + bold_colored_text(len(funcName(totalScriptList)), COLOR_BLUE))
# print(f"{'These functions are:':<{alignment_width}}" + bold_colored_text(funcName(totalScriptList), COLOR_GREEN))
# print(f"{'The total Cyclomatic Complexity is:':<{alignment_width}}" + bold_colored_text(calculate_cyclomatic_complexity(open(scriptPath, "r").read()), COLOR_BLUE))

depthChain = CallChain()#splitFunc(scriptPath), funcName(scriptPath))
depthChain = CallChain(splitFunc(scriptPath), funcName(scriptPath))
ambitionScore = depthChain.depth
print(f"{'The highest level of function nesting is:':<{alignment_width}}" + bold_colored_text(ambitionScore, COLOR_BLUE))
print(f"{'The longest chain of function calls is:':<{alignment_width}}" + bold_colored_text(depthChain.longestChain, COLOR_BLUE))

#print(f"{'The most function calls within a function:':<{alignment_width}}" + bold_colored_text(depthChain.maxFunctionCalls, COLOR_BLUE))
# print(depthChain.findMaxDepth(['hostGame', ['addMove'], ['allowsMove'], ['isFull'], ['winsFor'], ['aiMove', ['allowsMove'], ['colsToWin', ['addMove'], ['allowsMove'], ['delMove'], ['winsFor'], ['addMove'], ['allowsMove'], ['delMove'], ['winsFor']], ['allowsMove'], ['colsToWin', ['addMove'], ['allowsMove'], ['delMove'], ['winsFor'], ['addMove'], ['allowsMove'], ['delMove'], ['winsFor']]], ['addMove'], ['allowsMove'], ['isFull'], ['winsFor'], ['aiMove', ['allowsMove'], ['colsToWin', ['addMove'], ['allowsMove'], ['delMove'], ['winsFor'], ['addMove'], ['allowsMove'], ['delMove'], ['winsFor']], ['allowsMove'], ['colsToWin', ['addMove'], ['allowsMove'], ['delMove'], ['winsFor'], ['addMove'], ['allowsMove'], ['delMove'], ['winsFor']]]]))           
#print(f"{'The function with the most calls is:':<{alignment_width}}" + bold_colored_text(depthChain.functionMostCalls, COLOR_BLUE))
#print(f"{'The calls in '+ bold_colored_text(depthChain.functionMostCalls, COLOR_BLUE):}" +" include " + bold_colored_text(depthChain.maxFunctionCallsList, COLOR_BLUE))

#print(f"{'The average depth is :':<{alignment_width}}" + bold_colored_text(depthChain.averageDepth, COLOR_BLUE))
#print(f"{'The average calls is: ':<{alignment_width}}" + bold_colored_text(depthChain.averageCalls, COLOR_BLUE))



# weeksTesting = []
# weeksTesting.append(findIfOrVar(noCommentsinputfile))
# weeksTesting.append(findRecursion(scriptPath))
# weeksTesting.append(findListComp(noCommentsinputfile))
# weeksTesting.append(findSlicing(noCommentsinputfile))
# weeksTesting.append(findBoolAlg(noCommentsinputfile))
# weeksTesting.append(findLoops(scriptPath))
# weeksTesting.append(findNestedLoops(scriptPath))
# weeksTesting.append(findDictionaries(noCommentsinputfile))
# weeksTesting.append(findOop(scriptPath))

# print(f"{'Week 1: Has ifs or variables?':<{alignment_width}}" + color_boolean(findIfOrVar(noCommentsinputfile)))
# print(f"{'Week 2: Has Recursion?':<{alignment_width}}" + color_boolean(findRecursion(scriptPath)))
# print(f"{'Week 3: Has List Comprehension?':<{alignment_width}}" + color_boolean(findListComp(noCommentsinputfile)))
# print(f"{'Week 4: Has Slicing?':<{alignment_width}}" + color_boolean(findSlicing(noCommentsinputfile)))
# print(f"{'Week 5: Has Boolean Algebra?':<{alignment_width}}" + color_boolean(findBoolAlg(noCommentsinputfile)))
# print(f"{'Week 7: Has Loops?':<{alignment_width}}" + color_boolean(findLoops(scriptPath)))
# print(f"{'Week 8: Has Nested loops?':<{alignment_width}}" + color_boolean(findNestedLoops(scriptPath)))
# print(f"{'Week 9: Has Dictionaries?':<{alignment_width}}" + color_boolean(findDictionaries(noCommentsinputfile)))
# print(f"{'Week 10: Has OOP?':<{alignment_width}}" + color_boolean(findOop(scriptPath)))
# print(f"{'This project encompasses':<{alignment_width}}" + bold_colored_text(sumTests(weeksTesting), COLOR_BLUE) + " out of " + bold_colored_text(len(weeksTesting), COLOR_BLUE) + " weeks tested in this course")


'''DEBUGGING STATEMENTS'''



