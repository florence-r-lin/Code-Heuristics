import re  
import ast
# import pygame
from Cyclomatic import *
import fileParsing
from NestedDepth import CallChain 
import time
import multiprocessing


def removeComment(code):
    # remove # comments
    return re.sub(r'#.*', '', code)

def removeDocstring(code):
    # remove triple-quoted docstrings
    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    return re.sub(docstring_regex, '', code, flags=re.DOTALL)

def removeblank(code):
    nonblankLine = [line for line in code.splitlines() if line.strip() != ""]
    return '\n'.join(nonblankLine)

def countComment(code):
    return sum(1 for line in code.splitlines() if '#' in line and not line.strip().startswith('#!'))

def countDocstring(code):
    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    matches = re.findall(docstring_regex, code, flags=re.DOTALL)
    total_lines = 0
    for match in matches:
        docstring_text = match[0] if match[0] else match[1]
        total_lines += docstring_text.count('\n') + 2
    return total_lines

def countblank(code):
    return sum(1 for line in code.splitlines() if line.strip() == "")

def calculatePercentage(scriptPath):
    with open(scriptPath, 'r') as file:
        code = file.read()

    total_lines = len(code.splitlines())
    if total_lines == 0:
        return 0.0, 0.0, 0.0

    # docstring percentage
    docstringPercentage = (countDocstring(code) / total_lines) * 100

    # comment percentage
    commentPercentage = (countComment(code) / total_lines) * 100

    # blank line percentage
    blankPercentage = (countblank(code) / total_lines) * 100

    return commentPercentage, docstringPercentage, blankPercentage

def findFunc(cleanFile):
    try:
        tree = ast.parse(cleanFile)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return functions
    except:
        return []

def getFunctionSource(scriptPath, func_node):
    with open(scriptPath, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])

def splitFunc(cleanFile):
    funcList = []
    try:
        tree = ast.parse(cleanFile)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        lines = cleanFile.splitlines(keepends=True)
        for func in functions:
            start_line = func.lineno - 1
            end_line = func.end_lineno
            func_source = "".join(lines[start_line:end_line])
            funcList.append(func_source)
        return funcList
    except Exception as e:
        return []
 
def funcName(cleanFile):
    try:
        tree = ast.parse(cleanFile)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        return [func.name for func in functions]
    except:
        return []

def avgFunc(cleanFile):
    try:
        tree = ast.parse(cleanFile)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        if len(functions) == 0:
            return 0
        total_lines = 0
        for func in functions:
            if hasattr(func, 'end_lineno'):
                total_lines += func.end_lineno - func.lineno + 1
            else:
                total_lines += 1  # fallback
        return total_lines / len(functions)
    except:
        return 0

def countLoops(cleanFile):
    try:
        tree = ast.parse(cleanFile)
        return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
    except:
        return 0

def avgLoop(cleanFile):
    try:
        tree = ast.parse(cleanFile)
        loop_lengths = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                if hasattr(node, 'end_lineno'):
                    loop_lengths.append(node.end_lineno - node.lineno + 1)
                else:
                    loop_lengths.append(1)
        if loop_lengths:
            return sum(loop_lengths) / len(loop_lengths)
        else:
            return 0
    except:
        return 0

def findIfOrVar(cleanFile):
    try:
        tree = ast.parse(cleanFile)

        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.Assign)):
                return True
        return False
    except: 
        return False

def findBoolAlg(cleanFile):
    try: 
        tree = ast.parse(cleanFile)

        for node in ast.walk(tree):
            if isinstance(node, ast.BoolOp):
                return True
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
                return True
        return False
    except:
        return False

def findDictionaries(cleanFile):
    try: 
        tree = ast.parse(cleanFile)

        for node in ast.walk(tree):
            if isinstance(node, ast.Dict):
                return True
        return False
    except: 
        return False

def findSlicing(cleanFile):
    try: 
        tree = ast.parse(cleanFile)
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
                return True
        return False
    except: 
        return False

def findNestedLoops(scriptPath):
    try: 
        with open(scriptPath, "r") as file:
            tree = ast.parse(file.read(), filename=scriptPath)

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.For, ast.While)):
                        return True
        return False
    except: 
        return False

def findLoops(scriptPath):
    try: 
        with open(scriptPath, "r") as file:
            tree = ast.parse(file.read(), filename=scriptPath)

        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                return True
        return False
    except:
        return False
        
def findRecursion(scriptPath):
    try:
        with open(scriptPath, "r") as file:
            ast.parse(file.read(), filename=scriptPath)
        
        functions = findFunc(scriptPath)
        for func in functions: 
            func_name = func.name
            for node in ast.walk(func):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == func_name:
                        return True
                    if isinstance(node.func, ast.Attribute) and node.func.attr == func_name:
                        return True
        return False
    except: 
        return False

def findListComp(cleanFile):
    try:
        tree = ast.parse(cleanFile)

        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                return True
        return False
    except:
        return False
    
def findOop(scriptPath):
    try:
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
    except: 
        return False

def identify_project(script_path):
    project_keywords = {
        'textID': ["cleanstring", "makewordlength", "textmodel", "makewords", "makestems", "makepunctuation", "myparameter", "rawtext", "tmintro", "dictionary", "smallestvalue", "comparedictionaries", "twomodels", "comapretext", "encode", "punctuation"],
        'picoBot': ["randomize", "surrounding", "crossover", "xxxx", "nxxx", "nxwx", "xxxS", "bot", "pico", "program", "world", "unsortedkeys", "possible", "mutate", "getmove", "visitedcells", "evaluatefitness", "trials", "GA", "savetofile", "average"],
        'gameOfLife': ["lifeboard", "life", "gen", "generation", "longevity", "cell", "neighbors", "corner", "population", "glider", "dance", "demo"],
        'vPython': ["vpython", "velocity", "make_", "box", "sphere", "cylinder", "pos", "vel", "autoscale", "glowscript", "axis", "cone", "compound", "vec", "origin", "event"],
        'textGame_keywords': ["board", "win", "host", "card", "play", "ai", "hand", "game", "opponent", "hangman", "jotto", "chomp", "tic", "tac", "toe", "mancala", "battleship", "mastermind", "dice"]
    }

    text_path = script_path[:-3] + '_metrics.txt'
    
    with open(script_path, 'r', encoding='utf-8') as file:
        script_text = file.read().lower()
    
    with open(text_path, 'w', encoding='utf-8') as text_file:
        text_file.write(script_text)
    
    project_scores = {project: sum(script_text.count(keyword) for keyword in keywords) for project, keywords in project_keywords.items()}
    
    best_match = max(project_scores, key=project_scores.get)
    return best_match

def sumTests(boolList):
    total = 0
    for i in boolList:
        if i:
            total += 1
    return total

def executeFile(path, return_dict):
    try:
        with open(path, 'r') as f:
            filedata = f.read()
        exec(filedata, {})
        return_dict['result'] = 'completed'
    except Exception as e:
        return_dict['result'] = str(e)

def testTimeout(scriptPath, timeout):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    process = multiprocessing.Process(target=executeFile, args=(scriptPath, return_dict))
    process.start()
    process.join(timeout)

    if process.is_alive():
        process.terminate()
        process.join()
        return "Execution Timed Out"

    return return_dict.get('result', 'Execution Completed')

def findExecutionTime(scriptPath, timeout=5):
    try:
        startTime = time.time()
        result = testTimeout(scriptPath, timeout)
        
        if result == "Execution Timed Out":
            return 'timeout'

        endTime = time.time()
        return endTime - startTime
    
    except Exception as e:
        return 'error'


def allMetrics(scriptPath):
    parseable = fileParsing.doesItParse(scriptPath)
    if not parseable:
        print(scriptPath, 'is not parseable')
        return
    
    with open(scriptPath, 'r', encoding='utf-8-sig', errors='ignore') as f:
        originalCode = f.read()

    cleanFile = fileParsing.cleanParseFile(scriptPath)
    codeOnlyFile = removeblank(removeDocstring(removeComment(originalCode)))

    totalLOC = len(originalCode.splitlines())
    commentPercentage, docstringPercentage, blankPercentage = calculatePercentage(scriptPath)

    # setting up all portions of list
    totalLOC = len(originalCode.splitlines())
    commentPercentage, docstringPercentage, blankPercentage = calculatePercentage(scriptPath)

    functions = findFunc(cleanFile)
    lenFuncs = len(functions)
    avgFuncLen = avgFunc(cleanFile)
    numLoops = countLoops(cleanFile)
    avgLoopLen = avgLoop(cleanFile)

    totalCC = calculate_cyclomatic_complexity(cleanFile)

    depthChain = CallChain(splitFunc(cleanFile), funcName(cleanFile))
    ambitionScore = depthChain.depth

    executionTime = findExecutionTime(scriptPath)

    """
    weeksTesting = [
            findIfOrVar(codeOnlyFile),
            findRecursion(scriptPath),
            findListComp(codeOnlyFile),
            findSlicing(codeOnlyFile),
            findBoolAlg(codeOnlyFile),
            findLoops(scriptPath),
            findNestedLoops(scriptPath),
            findDictionaries(codeOnlyFile),
            findOop(scriptPath)
        ]
    weeksUsed = sumTests(weeksTesting)
    totalWeekstested = len(weeksTesting)
    """

    # project = identify_project(scriptPath)
    Class = fileParsing.getClassFromFilepath(scriptPath)
    Semester = fileParsing.getSemesterFromFilepath(scriptPath)
    Year = fileParsing.getYearFromFilepath(scriptPath)

    outputList = [scriptPath, totalLOC, commentPercentage, docstringPercentage, blankPercentage, lenFuncs, avgFuncLen, numLoops, avgLoopLen, totalCC, ambitionScore, executionTime, Class, Semester, Year]
    return outputList

print(allMetrics('/Users/summer-2024/Desktop/code metrics 25/All-Data/CS35-Data/assignments postllm/submissions_cs35_sp2025/submission_351/final|hw4pr1 .py'))
# ['filepath', 800, 24.75, 4.125, 37.25, 7, 12.857142857142858, 3, 3.0, 11, 1, 1.3178491592407227, 'CS35', 'sp2025', 2025]