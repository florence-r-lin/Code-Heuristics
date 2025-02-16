import os
import json
import fileParsing

def isNotAlphaNumeric(s):
    if "\n" == s[-1]:
        return not s[:-1].isalnum()
    else:
        return not s.isalnum()

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
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    filtLines = list(filter(isNotAlphaNumeric, cell['source']))
                    filtLines.append("\n\n\n")
                    newT.writelines(filtLines) 
                else:
                    markT.writelines(cell['source'])
            newT.close()
            markT.close()
        
def notebookToPyOnFilePath(filePath):
    [notebookToPy(i) for i in fileParsing.getAllNotebookFilesInPath(filePath)]

"""
WARNING THIS WILL ACTIVELY DELETE EVERY FILE WITH THE .IPYNB.PY ENDING TAG IN THE PATH DO NOT USE UNLESS YOU MEAN TO
"""

def removeipynbpy(filePath):
    check = input("WARNING THIS WILL ACTIVELY DELETE EVERY FILE WITH THE .IPYNB.PY ENDING TAG IN THE PATH DO NOT USE UNLESS YOU MEAN TO (press y to continue) ")  
    if check == 'y':  
        result = list(os.walk(filePath))
        for folder_tuple in result:
            currentpath, subfolder, files = folder_tuple

            if '__MACOSX' in currentpath: continue

            for file in files:
                if file[-9:] == ".ipynb.py":
                    print(file)
                    os.remove(currentpath + "/" + file)
    #notebookToPy("/Users/yuan/Desktop/Work/School/Research/CS5 DATA/post-LLM data/cs35/submissions_cs35_s23/submission_185159375/Source_Code.ipynb")

notebookToPyOnFilePath("/home/edonson/METRICLab/Code-Heuristics/studentScripts/notebooks")
removeipynbpy("/home/edonson/METRICLab/Code-Heuristics/studentScripts/notebooks")