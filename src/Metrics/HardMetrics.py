import re  
import ast
# import pygame
from Cyclomatic import *
import fileParsing
from NestedDepth import CallChain 
import time
import multiprocessing

# for new version of comment counting
import tokenize
from io import StringIO

# this should overcount
def oldRemoveComment(code):
    # remove single-line comments (starting with #)
    return re.sub(r'#.*', '', code)

# this should be slower on a large scale
def removeComment(code):
    result = []
    tokens = tokenize.generate_tokens(StringIO(code).readline)

    for tok_type, tok_string, start, end, line in tokens:
        if tok_type == tokenize.COMMENT:
            continue  # skip comments
        elif tok_type == tokenize.NL or tok_type == tokenize.NEWLINE:
            result.append('\n')
        else:
            result.append(tok_string)

    return ''.join(result)

# a little too simple, but will keep it for now
def removeDocstring(code):
    # remove triple-quoted docstrings
    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    return re.sub(docstring_regex, '', code, flags=re.DOTALL)


# fully AI-generated, need to test
# we can simplify this using the AST we've already generated, ideally
def newRemoveDocstring(code):
    class DocstringRemover(ast.NodeTransformer):
        def visit_FunctionDef(self, node):
            self.generic_visit(node)
            if (len(node.body) > 0 and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

        def visit_ClassDef(self, node):
            self.generic_visit(node)
            if (len(node.body) > 0 and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

        def visit_Module(self, node):
            self.generic_visit(node)
            if (len(node.body) > 0 and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
            return node

    tree = ast.parse(code)
    tree = DocstringRemover().visit(tree)
    ast.fix_missing_locations(tree)
    
    try:
        return ast.unparse(tree)  # Python 3.9+
    except AttributeError:
        import astor
        return astor.to_source(tree)  # Use astor as fallback for <3.9


def removeblank(code):
    # remove empty lines
    nonblankLine = [line for line in code.splitlines() if line.strip() != ""]
    return '\n'.join(nonblankLine)

# the old version of this function didn't catch all single-line comments
# idk if inline comments are supposed to be included here, but I am including them now
def oldCountComment(code):

    # count number of single-line comments (starting with #)
    return sum(1 for line in code.splitlines() if '#' in line and not line.strip().startswith('#!'))

def countComment(code):
    count = 0
    try:
        tokens = tokenize.generate_tokens(StringIO(code).readline)
        for tok_type, tok_string, *_ in tokens:
            if tok_type == tokenize.COMMENT:
                count += 1
    except tokenize.TokenError as e:
        raise ValueError(f"Token error in comment counting: {e}")
    return count



def countDocstring(code):
    # counts the number of docstrings in a file using regex
    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    matches = re.findall(docstring_regex, code, flags=re.DOTALL)
    total_lines = 0
    for match in matches:
        docstring_text = match[0] if match[0] else match[1]
        total_lines += docstring_text.count('\n') + 2
    return total_lines

def countblank(code):
    # counts the number of blank lines in a script
    return sum(1 for line in code.splitlines() if line.strip() == "")

def calculatePercentage(scriptPath):
    # calculates percentage of lines which are docstrings, comments, blank lines
    with open(scriptPath, 'r') as file:
        code = file.read()

    total_lines = len(code.splitlines())
    if total_lines == 0:
        return 0.0, 0.0, 0.0

    # docstring percentage
    docstringPercentage = (countDocstring(code) / total_lines) * 100

    # comment percentage
    try:
        commentPercentage = (countComment(code) / total_lines) * 100
    except ValueError as e:
        print(f"Skipping file {scriptPath} due to comment count failure: {e}")
        return None, None, None  # Or return a special object indicating skip

    # blank line percentage
    blankPercentage = (countblank(code) / total_lines) * 100

    return commentPercentage, docstringPercentage, blankPercentage


# this basically works OK but could miss async functions
def findFunc(tree):
    # returns all functions in a script using ASTs
    if not tree:
        return []
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

# fully vibecoded, not implementing it yet, looks reasonable though
def newFindFunc(tree):
    # returns all functions in a script using ASTs
    if not tree:
        return []
    functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
    return functions

def getFunctionSource(scriptPath, func_node):
    # returns the text of a particular function
    with open(scriptPath, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])

# currently missing async functions
def splitFunc(cleanFile):
    # Returns list of function source code strings from source and its AST
    tree = ast.parse(cleanFile)
    funcList = []
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    lines = cleanFile.splitlines(keepends=True)
    for func in functions:
        start_line = func.lineno - 1
        end_line = func.end_lineno
        func_source = "".join(lines[start_line:end_line])
        funcList.append(func_source)
    return funcList


def funcName(tree):
    # returns a list of the names of all functions in cleanFile
    if not tree:
        return []
    
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return [func.name for func in functions]

def avgFunc(tree):
    # returns the average number of lines per function in cleanFile
    if not tree:
        return 0
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


# it looks like currently this counts all loops in the entire file! 
# that seems fine to me but clashes with the comment, so idk
def countLoops(tree):
    # counts the total number of for or while loops of all functions in cleanFile
    if not tree:
        return 0
    
    return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))

# did not originally return anything if there were no loops, so added fallback
def avgLoop(tree):
    # returns average number of lines in a loop in cleanFile
    if not tree:
        return 0

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
  

def findIfOrVar(tree):
    # returns whether a file contains an if statement or a variable assignment
    if not tree:
        return False
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.Assign)):
            return True
    return False
  

def findBoolAlg(tree):
    # returns whether a file contains a boolean operator (if, and, not)
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.BoolOp):
            return True
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return True
    return False

def findDictionaries(tree):
    # returns whether any dictionaries are made in tree
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            return True
    return False

# (do we also want to check for index accessing? currently we don't)
def findSlicing(tree):
    # returns whether any objects in cleanFile are sliced
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            return True
    return False

# this only catches nested loops in consecutive lines
def oldFindNestedLoops(tree):
    # returns whether tree contains any nested loops
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.For, ast.While)):
                    return True
    return False

# slightly vibecoded but looks good
def findNestedLoops(tree):
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            # Check if there's any loop node nested *anywhere* inside this loop's body
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.For, ast.While)):
                    return True
    return False



def findLoops(tree):
    # returns whether tree contains any loops

    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            return True
    return False

        
def findRecursion(tree):
    # returns whether tree contains any recursive calls
    if not tree:
        return False
        
    functions = findFunc(tree)
    for func in functions: 
        func_name = func.name
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True
                if isinstance(node.func, ast.Attribute) and node.func.attr == func_name:
                    return True
    return False


def findListComp(tree):
    # returns whether any list comprehension is used in cleanFile

    if not tree:
        return False
  
    for node in ast.walk(tree):
        if isinstance(node, ast.ListComp):
            return True
    return False

# I can optimize this slightly
def oldFindOop(tree):
    # returns whether a class and a method are found in tree
    if not tree:
        return False
    
  
    hasClass = False
    hasMethod = False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            hasClass = True
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    hasMethod = True

    return hasClass and hasMethod

def findOop(tree):
    # returns whether a class and a method are found in tree
    if not tree:
        return False

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    return True

    return False

# we need to figure out what to do with this when we open-source it
# not gonna touch it for now though
def identify_project(script_path):
    # returns which project the file likely corresponds to
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

# this works but can be optimized
def oldSumTests(boolList):
    # returns number of true values in boolList
    total = 0
    for i in boolList:
        if i:
            total += 1
    return total

def sumTests(boolList):
    return sum(boolList)

# we need to think more about this;
# breaks if it relies on global vars
# (but maybe that's fine if we're only looking at an individual file)
# also it can be risky to run an unknown file!
def executeFile(path, return_dict):
    # adds whether path was successfully executed to return_dict
    try:
        with open(path, 'r') as f:
            filedata = f.read()
        exec(filedata, {})
        return_dict['result'] = 'completed'
    except Exception as e:
        return_dict['result'] = str(e)

# def testTimeout(scriptPath, timeout):
#     # returns whether scriptPath was executed in < timeout
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()

#     process = multiprocessing.Process(target=executeFile, args=(scriptPath, return_dict))
#     process.start()
#     process.join(timeout)

#     if process.is_alive():
#         process.terminate()
#         process.join()
#         return "Execution Timed Out"

#     return return_dict.get('result', 'Execution Completed')

def _execute_file_worker(scriptPath, conn):
    """Child process: run the file and send back a status string."""
    try:
        with open(scriptPath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        exec(code, {})
        conn.send("Execution Completed")
    except Exception as e:
        conn.send(str(e))
    finally:
        conn.close()

def testTimeout(scriptPath, timeout):
    """
    Run scriptPath in a separate process with a time limit.
    Returns one of:
      - "Execution Completed"
      - an exception string from the child
      - "Execution Timed Out"
    """
    parent_conn, child_conn = multiprocessing.Pipe(duplex=False)
    p = multiprocessing.Process(target=_execute_file_worker, args=(scriptPath, child_conn))
    p.start()
    child_conn.close()  # close child end in parent process

    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        parent_conn.close()
        return "Execution Timed Out"

    # Child finished; try to receive its message (if any)
    status = "Execution Completed"
    if parent_conn.poll():          # message waiting?
        status = parent_conn.recv() # str sent by worker
    parent_conn.close()
    return status

# for now we're just going to ignore execution time. maybe we can add it back in later?
# def findExecutionTime(scriptPath, timeout=5):
#     # return the amount of time it takes ot execute scriptPath
#     # (or the amount of time before "timing out")
#     try:
#         startTime = time.time()
#         result = testTimeout(scriptPath, timeout)
#         if result == "Execution Timed Out":
#             return 'timeout'

#         endTime = time.time()
#         return endTime - startTime
    
#     except Exception as e:
#         # TODO: RAISE ERRORS AND HANDLE
#         return 'error'

def allMetrics(scriptPath, tree=None):
    parseable = fileParsing.doesItParse(scriptPath)
    if not parseable:
        print(scriptPath, 'is not parseable')
        return

    if tree is None:
        clean_code = fileParsing.cleanParseFile(scriptPath)
        tree = ast.parse(clean_code)
    else:
        clean_code = None  # already have tree, assume clean_code not needed here

    with open(scriptPath, 'r', encoding='utf-8-sig', errors='ignore') as f:
        originalCode = f.read()

    if clean_code is None:
        clean_code = fileParsing.cleanParseFile(scriptPath)

    commentPercentage, docstringPercentage, blankPercentage = calculatePercentage(scriptPath)

    functions = findFunc(tree)
    numFunctions = len(functions)
    avgFuncLen = avgFunc(tree)
    numLoops = countLoops(tree)
    avgLoopLen = avgLoop(tree)
    totalCC = calculate_cyclomatic_complexity(tree)

    depthChain = CallChain(splitFunc(clean_code), funcName(tree))
    ambitionScore = depthChain.depth

    executionTime = -3.0  # placeholder

    weeksTesting = [
        findIfOrVar(tree),
        findRecursion(tree),
        findListComp(tree),
        findSlicing(tree),
        findBoolAlg(tree),
        findLoops(tree),
        findNestedLoops(tree),
        findDictionaries(tree),
        findOop(tree)
    ]
    weeksUsed = sumTests(weeksTesting)
    totalWeekstested = len(weeksTesting)

    Class = fileParsing.getClassFromFilepath(scriptPath)
    Semester = fileParsing.getSemesterFromFilepath(scriptPath)
    Year = fileParsing.getYearFromFilepath(scriptPath)

    return {
    'file': scriptPath,
    'loc': len(originalCode.splitlines()),
    'comment_pct': commentPercentage,
    'doc_pct': docstringPercentage,
    'blank_pct': blankPercentage,
    'num_funcs': numFunctions,
    'avg_func_len': avgFuncLen,
    'num_loops': numLoops,
    'avg_loop_len': avgLoopLen,
    'cyclo': totalCC,
    'max_depth': ambitionScore,
    'exec_time': executionTime,
    'weeks_used': weeksUsed,
    'total_weeks_tested': totalWeekstested,
    'class_name': Class,
    'semester': Semester,
    'year': Year
}





# print(allMetrics('/Users/summer-2024/Desktop/code metrics 25/All-Data/CS35-Data/assignments postllm/submissions_cs35_sp2025/submission_351/final|hw4pr1 .py'))
# ['filepath', 800, 24.75, 4.125, 37.25, 7, 12.857142857142858, 3, 3.0, 11, 1, 1.3178491592407227, 'CS35', 'sp2025', 2025]