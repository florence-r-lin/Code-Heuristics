import re  
import ast
# import pygame
from Cyclomatic import *
import fileParsing
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
    
def containsString(str, noCommentScriptStr):
    wordScript = noCommentScriptStr.split(" ")
    for i in wordScript:
        if re.search(str, i):
            return True
    return False

def findIfOrVar(noCommentScriptStr):
    return containsString("if|=", noCommentScriptStr)

def findBoolAlg(noCommentScriptStr):
    return containsString("and|or|not|", noCommentScriptStr)

def findDictionaries(noCommentScriptStr):
    return containsString(r"\{(?:[^{}]|)*\}", noCommentScriptStr)

def findSlicing(noCommentScriptStr):
    return containsString(r"\[.*:.*\]", noCommentScriptStr)

def findNestedLoops(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.For, ast.While)):
                    return True
    return False


def findLoops(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            return True
    return False
        
def findRecursion(scriptPath):
    #split into functions, then find function name within the functions
    #def whitespace word (anything ) colon
    totalScriptList = []
    inputFile = open(scriptPath, "r")
    for x in inputFile:
        totalScriptList.append(x)
    names = funcName(scriptPath)
    for n, i in enumerate(splitFunc(scriptPath)):
        if i.count(names[n]) > 1:
            return True
    return False

def findListComp(noCommentScriptStr):
    return containsString("\[.*for.*in.*\]", noCommentScriptStr)
    # tree = ast.parse(noCommentScriptStr)
    # for node in ast.walk(tree):
    #     if isinstance(node, ast.ListComp):
    #         return True
    # return False
    
def findOop(scriptPath):
    with open(scriptPath, "r") as file:
        tree = ast.parse(file.read(), filename=scriptPath)
    hasClass = False
    hasMethod = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            hasClass = True
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    hasMethod = True

    return hasClass and hasMethod

def sumTests(boolList):
    total = 0
    for i in boolList:
        if i:
            total = total+1
    return total

def noCommentsFromFile(scriptPath):
    file = open(scriptPath, "r")
    return(removeComments(file.read()))


def replaceInFile(scriptPath, toBeReplaced, replacer):
    f = open(scriptPath,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace(toBeReplaced, replacer)

    f = open(scriptPath,'w')
    f.write(newdata)
    f.close()


def allMetrics(scriptPath):
    parseable = fileParsing.doesItParse(scriptPath)
    '''
    if (not parseable):
        print(scriptPath, "is not parseable")
        return
    '''
    commentList = []
    totalScriptList = []
    # opening file
    inputfile = open(scriptPath, "r")
    inputfiletest2 = open(scriptPath, "r")
    noCommentsinputfile = removeComments(inputfiletest2.read())
    # making two line by line lists of the file, both full and only comments
    for x in inputfile:
        totalScriptList.append(x)
        commentList.append(commentCheck(x))
    commentList = [z for z in commentList if z != ""]
    # setting up all portions of list
    totalLOC = len(totalScriptList)
    commentPercentage = (1 - (len(noCommentsinputfile) / len(open(scriptPath, "r").read()))) * 100
    functions = funcName(scriptPath)
    totalCC = calculate_cyclomatic_complexity(open(scriptPath, "r").read())
    lenFuncs = len(functions)
    depthChain = CallChain()
    depthChain = CallChain(splitFunc(scriptPath), funcName(scriptPath))
    ambitionScore = depthChain.depth
    # print(depthChain.longestChain)
    # getting into weekstested
    weeksTesting = []
    weeksTesting.append(findIfOrVar(noCommentsinputfile))
    weeksTesting.append(findRecursion(scriptPath))
    weeksTesting.append(findListComp(noCommentsinputfile))
    weeksTesting.append(findSlicing(noCommentsinputfile))
    weeksTesting.append(findBoolAlg(noCommentsinputfile))
    weeksTesting.append(findLoops(scriptPath))
    weeksTesting.append(findNestedLoops(scriptPath))
    weeksTesting.append(findDictionaries(noCommentsinputfile))
    weeksTesting.append(findOop(scriptPath))
    weeksUsed = sumTests(weeksTesting)
    totalWeekstested = len(weeksTesting)

    outputList = [scriptPath, totalLOC, commentPercentage, lenFuncs, totalCC,ambitionScore, weeksUsed]#ambitionScore, weeksUsed]
    #fullList = [totalLOC, commentPercentage, functions, totalCC, ambitionScore, depthChain.longestChain, depthChain.functionMostCalls, depthChain.maxFunctionCallsList, weeksUsed, totalWeekstested]
    return outputList#fullList,outputList
    # return fieldDict