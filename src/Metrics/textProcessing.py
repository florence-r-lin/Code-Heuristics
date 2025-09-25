import os
import json
import fileParsing

def isNotAlphaNumeric(s):
    if len(s) <= 0 or "\n" == s[-1]:
        return not s[:-1].isalnum()
    else:
        return not s.isalnum()

def startsWithAlph(s):
    if len(s) > 0:
        return not s[0] in "%!"
    return True

def notebookToPy(filePath):
    #Take all text files, seperate markdown and python into seperate files
    # print(filePath)
    # for file in os.listdir(filePath):
    if filePath[-1] == "b":
    #print(filePath)
        with open(filePath, 'r') as tFile:
            notebook = json.load(tFile)
            #newT = open(filePath[:-6] + "-code.py", 'w')
            currentNotebook = filePath.split("/")[-1]
            currentNotebook = currentNotebook.split(".")[0]
            newT = open(fileParsing.backOneDir(filePath) + "/final|" + currentNotebook + ".py", "w")
            markT = open(filePath[:-6] + "-mark.txt", 'w')      
            writtenInCode = False

            for cell in notebook['cells']:
                if currentNotebook == "test":
                    print(cell['source'])
                if cell['cell_type'] == 'code' and len(cell['source']) > 0:
                    filtLines = list(filter(isNotAlphaNumeric, cell['source']))
                    filtLines = list(filter(startsWithAlph, filtLines)) #New line filters for stuff like # and %matplotlib
                    filtLines.append("\n\n\n")
                    newT.writelines(filtLines) 
                    writtenInCode = True
                else:
                    markT.writelines(cell['source'])
            if writtenInCode:
                newT.close()
            else:
                os.remove(fileParsing.backOneDir(filePath) + "/final|" + currentNotebook + ".py")
            markT.close()
        
def notebookToPyOnFilePath(filePath):
    [notebookToPy(i) for i in fileParsing.getAllNotebookFilesInPath(filePath)]

"""
WARNING THIS WILL ACTIVELY DELETE EVERY FILE WITH THE .IPYNB.PY ENDING TAG IN THE PATH DO NOT USE UNLESS YOU MEAN TO
"""

def removeipynbpy(filePath):
    result = list(os.walk(filePath))
    for folder_tuple in result:
        currentpath, subfolder, files = folder_tuple

        if '__MACOSX' in currentpath: continue

        for file in files:
            if file[-9:] == ".ipynb.py":
                print(file)
                os.remove(currentpath + "/" + file)

def removeEmptyFile(filePath):
    result = list(os.walk(filePath))
    for folder_tuple in result:
        currentpath, subfolder, files = folder_tuple

        if '__MACOSX' in currentpath: continue

        for file in files:
            if fileParsing.isAPythonFile(file):
                with open(currentpath + "/" + file, "r") as f:
                    lines = f.readlines()
                    lines = list(filter(lambda x: x != "\n", lines))
                    if not lines:
                        os.remove(currentpath + "/" + file)