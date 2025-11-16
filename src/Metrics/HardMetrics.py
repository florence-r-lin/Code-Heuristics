import re  
import ast
from dataclasses import dataclass
from typing import Optional

from Cyclomatic import *
import fileParsing
from NestedDepth import CallChain


@dataclass
class MetricRecord:
    """Flat, typed record that represents metrics for a single file."""
    file: str
    loc: int
    comment_pct: float
    doc_pct: float
    blank_pct: float
    num_funcs: int
    avg_func_len: float
    num_loops: int
    avg_loop_len: float
    cyclo: float
    max_depth: Optional[int]
    exec_time: float
    class_name: Optional[str]
    semester: Optional[str]
    year: Optional[int]

def removeComment(code):
    """Removes single-line comments from a script.
    This is a more lightweight version of the function which is slightly
    less accurate than tokenizeRemoveComment, but much faster.

    :param code: Inputted script
    :type code: str
    :return: The same script, excepting single-line comments
    :rtype: str
    """
    return re.sub(r'#.*', '', code)

def tokenizeRemoveComment(code):
    """Removes single-line comments from a script.
    This is a slightly more precise version of the function,
    but much slower, so by default it is not used.

    :param code: Inputted script
    :type code: str
    :return: The same script, excepting single-line comments
    :rtype: str
    """
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

def removeDocstring(code):
    """Removes docstrings from a script.
    This is a more lightweight version of the function which is slightly
    less accurate than tokenizeRemoveDocstring, but much faster.

    :param code: Inputted script
    :type code: str
    :return: The same script, excepting triple-quoted docstrings
    :rtype: str
    """

    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    return re.sub(docstring_regex, '', code, flags=re.DOTALL)

def tokenizeRemoveDocstring(code):
    """Removes single-line comments from a script.
    This is a slightly more precise version of the function,
    but much slower, so by default it is not used.

    :param code: Inputted script
    :type code: str
    :return: The same script, excepting triple-quoted docstrings
    :rtype: str
    """
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
    """Removes blank lines from a script.

    :param code: Inputted script
    :type code: str
    :return: The same script, excepting blank lines
    :rtype: str
    """
    nonblankLine = [line for line in code.splitlines() if line.strip() != ""]
    return '\n'.join(nonblankLine)


def countComment(code):
    """Counts the number of single-line comments in a script.
    This is a more lightweight version of tokenizedCountComment.

    :param code: Inputted script
    :type code: str
    :return: Number of single-line comments in the script
    :rtype: int
    """

    # count number of single-line comments (starting with #)
    return sum(1 for line in code.splitlines() if '#' in line and not line.strip().startswith('#!'))

def tokenizedCountComment(code):
    """Counts the number of single-line comments in a script with tokenization.

    :param code: Inputted script
    :type code: str
    :return: Number of single-line comments in the script
    :rtype: int
    """

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
    """Counts the number of docstrings in a script.

    :param code: Inputted script
    :type code: str
    :return: Number of single-line comments in the script
    :rtype: int
    """
    docstring_regex = r"'''(.*?)'''|\"\"\"(.*?)\"\"\""
    matches = re.findall(docstring_regex, code, flags=re.DOTALL)
    total_lines = 0
    for match in matches:
        docstring_text = match[0] if match[0] else match[1]
        total_lines += docstring_text.count('\n') + 2
    return total_lines

def countblank(code):
    """Counts the number of blank lines in a script.

    :param code: Inputted script
    :type code: str
    :return: Number of blank lines in the script
    :rtype: int
    """
    return sum(1 for line in code.splitlines() if line.strip() == "")

def calculatePercentage(scriptPath):
    """Calculates the percentages of lines which are
    docstrings, comments, and blank lengths

    :param scriptPath: file path to script of choice
    :type scriptPath: str
    :return: percentage of lines which are docstrings, comments, blanks
    :rtype: tuple of three floats
    """
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



def findFunc(tree):
    """Returns a list of all functions in an AST

    :param tree: abstract syntax tree associated with a particular script
    :type code: abstract syntax tree
    :return: percentage of lines which are docstrings, comments, blanks
    :rtype: list of ast.FunctionDef
    """
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

def getFunctionSource(scriptPath, func_node):
    """
    Returns the source code of a specific function from a Python script
    based on its node in an abstract syntax tree.

    :param scriptPath: path to the script containing the function code
    :type scriptPath: str
    :param func_node: the AST node representing the function to find.
    :type func_node: ast.FunctionDef
    :return: the function's source code
    :rtype: str
    """

    with open(scriptPath, "r") as file:
        lines = file.readlines()

    start_line = func_node.lineno - 1
    end_line = func_node.end_lineno

    return "".join(lines[start_line:end_line])


def splitFunc(cleanFile):
    """
    Extracts all function definitions from a file and returns their code

    :param cleanFile: file path of the code to analyze
    :type cleanFile: str
    :return: list of each function's source code
    :rtype: list[str]
    """

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
    """
    Retrieves the names of all function definitions from an AST 

    :param tree: an abstract syntax tree to retrieve names from
    :type tree: ast.AST
    :return: list of function names found within tree
    :rtype: list[str]
    """
    # returns a list of the names of all functions in cleanFile
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return [func.name for func in functions]

def avgFunc(tree):
    """
    Calculates the average number of lines per function in a given AST

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: average number of lines across all functions in tree
    :rtype: float
    """

    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    # if no functions are found, return 0
    if len(functions) == 0:
        return 0
    total_lines = 0
    for func in functions:
        if hasattr(func, 'end_lineno'):
            total_lines += func.end_lineno - func.lineno + 1
        else:
            total_lines += 1  # fallback
    return total_lines / len(functions)


def countLoops(tree):
    """Counts the total number of for and while loops in a given AST

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: total count of for and while loops within tree
    :rtype: int
    """
    return sum(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))


def avgLoop(tree):
    """Returns the average number of lines in a loop of tree.

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: average number of lines in a loop of tree
    :rtype: float
    """

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
    """Returns whether a tree contains an if statement or variable assignment
    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains an if statement or variable assignment
    :rtype: bool
    """

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.Assign)):
            return True
    return False
  

def findBoolAlg(tree):
    """Returns whether a tree contains a boolean operator (if, and, not)

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains a boolean operator
    :rtype: bool
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.BoolOp):
            return True
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return True
    return False

def findDictionaries(tree):
    """Returns whether any dictionaries are made in an AST

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains any dictionaries
    :rtype: bool
    """

    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            return True
    return False

def findSlicing(tree):
    """Returns whether any objects in an AST are sliced

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether any objects in tree are sliced
    :rtype: bool
    """

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            return True
    return False

def findNestedLoops(tree):
    """Returns whether any nested loops exist within a given AST

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether at least one nested loop exists in the tree
    :rtype: bool
    """

    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            # Check if there's any loop node nested *anywhere* inside this loop's body
            for child in ast.walk(node):
                if child is not node and isinstance(child, (ast.For, ast.While)):
                    return True
    return False

def findLoops(tree):
    """Returns whether any loops exist within a given AST

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether at least one loop exists in tree
    :rtype: bool
    """
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            return True
    return False

        
def findRecursion(tree):
    """Returns whether an AST contains any recursive calls

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains any recursive calls
    :rtype: bool
    """

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
    """Returns whether any list comprehension is used in a tree.

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains any list comprehension
    :rtype: bool
    """

    for node in ast.walk(tree):
        if isinstance(node, ast.ListComp):
            return True
    return False

def findOop(tree):
    """Returns whether an AST contains a class and a method

    :param tree: an abstract syntax tree to analyze
    :type tree: ast.AST
    :return: whether tree contains a class and a method
    :rtype: bool
    """
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

def findExecutionTime(scriptPath, timeout=5):
    """
    Measure the execution time of a Python script with a timeout safeguard.
    We do NOT recommend running this code by default,
    as execution time varies and all other metrics are much faster to calculate.

    :param scriptPath: Path to the Python script whose runtime should be measured.
    :type scriptPath: str
    :param timeout: Maximum allowed execution time in seconds before terminating execution.
    :type timeout: int or float, optional (defaults to 5s)
    :return: 
        - The execution time in seconds if the script finishes normally.  
        - "timeout" if the script does not finish before the timeout.  
        - "error" if an unexpected exception occurs.  
    :rtype: float or str
    """
    try:
        startTime = time.time()
        result = testTimeout(scriptPath, timeout)
        if result == "Execution Timed Out":
            return 'timeout'

        endTime = time.time()
        return endTime - startTime
    
    except Exception as e:
        return 'error'

def allMetrics(scriptPath, tree=None):
    """
    Calculates metrics for a file given its file path and optional AST.

    :param scriptPath: path to the file to analyze
    :type scriptPath: str
    :param tree: AST of the file to analyze (optional)
    :type tree: ast.AST
    :return: MetricRecord dataclass
    """
    parseable = fileParsing.doesItParse(scriptPath)
    if not parseable:
        print(scriptPath, 'is not parseable')
        return

    with open(scriptPath, 'r', encoding='utf-8-sig', errors='ignore') as f:
        originalCode = f.read()

    cleanFile = fileParsing.cleanParseFile(scriptPath)
    codeOnlyFile = removeblank(removeDocstring(removeComment(originalCode)))

    # If tree wasn't passed, parse the clean code
    if tree is None:
        import ast
        tree = ast.parse(cleanFile)

    # Now AST-based metrics
    functions = findFunc(tree)
    lenFuncs = len(functions)
    avgFuncLen = avgFunc(tree)
    numLoops = countLoops(tree)
    avgLoopLen = avgLoop(tree)

    # string-based metrics
    totalLOC = len(originalCode.splitlines())
    commentPercentage, docstringPercentage, blankPercentage = calculatePercentage(scriptPath)
    totalCC = calculate_cyclomatic_complexity(cleanFile)
    depthChain = CallChain(splitFunc(cleanFile), funcName(tree))
    maxDepth = depthChain.depth

    executionTime = -1.0
    Class = fileParsing.getClassFromFilepath(scriptPath)
    Semester = fileParsing.getSemesterFromFilepath(scriptPath)
    Year = fileParsing.getYearFromFilepath(scriptPath)

    rec = MetricRecord(
        file=scriptPath,
        loc=totalLOC,
        comment_pct=commentPercentage,
        doc_pct=docstringPercentage,
        blank_pct=blankPercentage,
        num_funcs=lenFuncs,
        avg_func_len=avgFuncLen,
        num_loops=numLoops,
        avg_loop_len=avgLoopLen,
        cyclo=totalCC,
        max_depth=maxDepth,
        exec_time=executionTime,
        class_name=Class,
        semester=Semester,
        year=Year,
    )
    return rec
