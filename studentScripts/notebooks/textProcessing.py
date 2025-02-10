import os
import json

def isNotAlphaNumeric(s):
    if "\n" == s[-1]:
        return not s[:-1].isalnum()
    else:
        return not s.isalnum()

def notebookToPy(filePath):
    #Take all text files, seperate markdown and python into seperate files
    #for file in os.listdir(filePath):
    if filePath[-1] == "b":
        #print(filePath)
        with open(filePath, 'r') as tFile:
            notebook = json.load(tFile)
            #newT = open(filePath[:-6] + "-code.py", 'w')
            newT = open("final.py", "w")
            markT = open(filePath[:-6] + "-mark.txt", 'w')                
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    filtLines = list(filter(isNotAlphaNumeric, cell['source']))
                    if "d\n" in filtLines:
                        print(list(filtLines))
                    newT.writelines(filtLines) 
                else:
                    markT.writelines(cell['source'])
            newT.close()
            markT.close()


notebookToPy("/home/edonson/METRICLab/Code-Heuristics/studentScripts/notebooks/final_project.ipynb") #Takes path to notebook
                        