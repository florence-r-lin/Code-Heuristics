import re

class CallChain:
    def __init__(self, functions=None, funcNames=None):
        if functions is None and funcNames is None:
            return
        
        self.functions = functions
        self.names = funcNames
        self.depth = self.findLongestBranch()[0]
        self.longestChain = self.findLongestBranch()[1]

        self.totalFuncCalls = 0 # gets updated after self.maxFunctionCalls is initialized

        self.maxFunctionCalls = self.findFunctionCalls()[0] 
        self.maxFunctionCallsList = self.findFunctionCalls()[1] # list of function calls in function with the most calls
        if self.maxFunctionCalls == 0:
            self.functionMostCalls = ''
        else:
            self.functionMostCalls = self.maxFunctionCallsList[0] # function with the most calls
        # broken until I put [0] in ???
        # self.averageDepth = self.depth/len(self.names)
        # self.averageCalls = self.totalFuncCalls/len(self.names)
        

    # def findBranches(self, func, funcs, names, currentPath):
    #     funcBody = func.split(':', 1)[1].strip()  # get everything behind the colon

    #     funcName = re.search("def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)  # before colon
    #     # print("Function name is\n", funcName)
    #     # print("Function Body is\n", funcBody)
    #     isRecursive = funcName in funcBody
        
    #     if funcName in currentPath:
    #         return currentPath

    #     currentPath.append(funcName)
    #     # base case: if there is no function call in the function
    #     if isRecursive or not any(name in funcBody for name in names):  # if function doesn't have another function call or function is recursive, terminate
    #         return currentPath
    #     else:
    #         for name in names:
    #             if name in funcBody and name not in currentPath:  # Only add if not already in path
    #                 # Find function corresponding to the name
    #                 nestedFunc = funcs[names.index(name)]
    #                 # Recursively call findBranches for the nested function
    #                 nestedPath = self.findBranches(nestedFunc, funcs, names, currentPath.copy())
    #                 if nestedPath:  # If nested call is non-empty, add it
    #                     currentPath.append(nestedPath)
    #         return currentPath
        

    def findBranches(self, func, funcs, names, currentPath):
        funcBody = func.split(':', 1)[1].strip()  # Get function body
        funcName = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)  # Extract function name

        if funcName in currentPath:
            return currentPath  # Terminate if function already in currentPath to avoid infinite recursion

        currentPath.append(funcName)
        isRecursive = funcName in funcBody

        # Base case: if no further function call or function is recursive, terminate
        if isRecursive or not any(name in funcBody for name in names):
            return currentPath
        else:
            for name in names:
                if name in funcBody and name not in currentPath:  # Only add if not already in path
                    nestedFunc = funcs[names.index(name)]
                    # Recursively call findBranches for the nested function
                    nestedPath = self.findBranches(nestedFunc, funcs, names, currentPath.copy())
                    tempPath = []
                    # Extend currentPath with unique elements from nestedPath
                    for func_in_path in nestedPath:
                        if func_in_path not in currentPath:
                            tempPath.append(func_in_path)
                    currentPath.append(tempPath)
            # print('the current path is', currentPath)
            return currentPath

    def findLongestBranch(self):  # longest chain of dependencies without recursion, takes in function list and function names list
        allPaths = []
        
        for func in self.functions:
            currentPath = []
            # print("\n\n\nCURRENT FUNCTION!!", func)
            currentPath.append(re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)) 
            path = self.findBranches(func, self.functions, self.names, [])
            # print('currentPath appending', path)
            allPaths.append(path)
            # print('allPaths =', allPaths)

        if allPaths is None or allPaths == []:
            return 0,[]
        longestPath = max(allPaths, key=lambda x: self.findMaxDepth(x))
        # print('longest chain length is', self.findMaxDepth(longestPath))

        return self.findMaxDepth(longestPath)[0], self.findMaxDepth(longestPath)[1]

    def findMaxDepth(self, nestedList, currentDepth=1):
        if not isinstance(nestedList, list) or not nestedList:
            return [ 0, [nestedList] ]
        if nestedList == []:
            return [ 0, [] ]
        if type(nestedList[0]) != type(''):
            print("Illegal!", nestedList)
            return 42
        maxDepth = currentDepth
        best_depth = 0
        best_cp = []
        best_name = nestedList[0]
        for item in nestedList:  # so, nestedList is a list!
            item_depth_pair = self.findMaxDepth(item, currentDepth + 1)
            item_depth = item_depth_pair[0]
            item_cp = item_depth_pair[1]
            if item_depth > best_depth:
                best_depth = item_depth
                best_cp = item_cp
        retvalue = [ best_depth+1, [ best_name ] + best_cp ]
        #print(f"{retvalue = }")
        return [ best_depth+1,  [ best_name ] + best_cp ]
   
    def findFunctionCalls(self): # How many function calls inside a function, ignoring depth and recursion
        callsList = []
        maxCalls = 1
        for func in self.functions:
            currentNumCalls = 1
            # print("\n\n\nCURRENT FUNCTION!!", func)
            funcBody = func.split(':', 1)[1].strip()  # get everything behind the colon
            funcName = re.search(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", func).group(1)
            currentPath = [funcName]
            for name in self.names:
                if name in funcBody and name not in funcName and name not in currentPath:
                    currentPath.append(name)
                    self.totalFuncCalls += 1
                    currentNumCalls += 1
            maxCalls = max(maxCalls, currentNumCalls)
            callsList.append(currentPath)
        if callsList == [] or callsList is None:
            return 0, []
        else:
            maxCallsList = max(callsList, key=len)
        # print('The most function calls within a function', maxCallsList)
        # print('The function with the most calls in it is', maxCallsList[0])
            return maxCalls, maxCallsList



# fsf = """
# def f(x):
#   z(42)
#   y(14)
# """
# fsz = """
# def z(x):
#   g(42)
#   f(8)
# """
# fsy = """
# def y(x):
#   z(42)
#   y(h(14))
# """
# cc = CallChain([fsf,fsz,fsy], ['f','z','y'])

# res = cc.findBranches(fsz, [fsf,fsz,fsy], ['f','z','y'], [])
# print(f"{res=}")

# print('longest branch', cc.findLongestBranch())

# ob = 77
# import ast
# tree = ast.parse(fsz, filename="localstr")
# functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
# for f in functions:
#     print(f"{f.name=}")
#     for ob in f.body:
#         print(f"    {ob.value.func.id=}")
# res = cc.findMaxDepth(fsz, ['f','z','y'])

#get a list of things that z calls FIRST and then run the func on those
