from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import ast


def getChildFolderNames(folderPath):
    # test
    # print(f"Reading {folderPath}")
    folderTree = list(os.walk(folderPath))

    # test
    # if not folderTree:
    #     print(f"Folder not found in path {folderPath}")
    return folderTree[0][1]

def getFullPathName(folderPath):
    childFolderNames = getChildFolderNames(folderPath)
    return [join(folderPath, i) for i in childFolderNames]

def replaceInFile(scriptPath, toBeReplaced, replacer):
    f = open(scriptPath,'r')
    filedata = f.read()
    f.close()

    newdata = filedata.replace(toBeReplaced, replacer)

    f = open(scriptPath,'w')
    f.write(newdata)
    f.close()

def replaceErrorsInFile(filePath):
    replaceInFile(filePath, "GlowScript", "#")
    replaceInFile(filePath, "Web VPython", "#")
    replaceInFile(filePath, "    if mag( wpos_noy - bpos_noy ) < smallest_dim \\",
                               "    if mag( wpos_noy - bpos_noy ) < smallest_dim or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):")
    replaceInFile(filePath, "       or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):", "#")
    replaceInFile(filePath, "else if", "elif")
    replaceInFile(filePath, "%matplotlib inline", "#")
    replaceInFile(filePath, "!git", "#")
    replaceInFile(filePath, "%cd", "#")
    replaceInFile(filePath, "!python", "#")
    replaceInFile(filePath, "!tar", "#")
    replaceInFile(filePath, "!pip", "#")
    replaceInFile(filePath, "pip", "#")
    replaceInFile(filePath, "%pwd", "#")
    replaceInFile(filePath, "cd ..", "#")


def getAllPythonFilesInPath(filePath):
    pathList = []
    result = list(os.walk(filePath))
    for folder_tuple in result:
        currentpath, subfolder, files = folder_tuple

        if '__MACOSX' in currentpath: continue

        for file in files:
            pathList.append(currentpath + "/" + file)
    finalPyList = [f for f in pathList if f.endswith('.py')]
    return finalPyList

def getAllNotebookFilesInPath(filePath):
    pathList = []
    result = list(os.walk(filePath))
    for folder_tuple in result:
        currentpath, subfolder, files = folder_tuple

        if '__MACOSX' in currentpath: continue

        for file in files:
            pathList.append(currentpath + "/" + file)
    finalPyList = [f for f in pathList if f.endswith('.ipynb')]
    return finalPyList

def isOnlyComments(inputStr):
    nonCommentList = []
    for i in inputStr:
        if not(i == "\n"):
           nonCommentList.append(i)
    if len(nonCommentList) == 0:
        print("Comment only file")
        raise Exception ("Comment only file")

def isAPythonFile(filePath):
    fileName = filePath.split("/")[-1]
    return fileName[-3:] == ".py" #fileName[0:6] == "final|" and 

def backOneDir(filePath):
    return "/".join(filePath.split("/")[:-1])

def getClassFromFilepath(filePath):
    parts = filePath.split('/')
    for part in parts:
        if part.endswith('-Data') and 'All' not in part: # CS5-Data
            return part.replace('-Data', '') 
    return None

def getSemesterFromFilepath(filePath):
    parts = filePath.split('/')
    for part in parts:
        if part.startswith('submissions'): # submissions_cs35_sp2025
            parts2 = part.split('_')
            return parts2[-1] 
    return None

def getYearFromFilepath(filePath):
    parts = filePath.split('/')
    newFilepath = []
    skip = False
    for part in parts:
        if part == 'Users': # my user is summer-2024 T-T
            skip = True
            continue
        if skip:
            skip = False
            continue
        newFilepath.append(part)

    for part in newFilepath:
        for i in range(len(part)-3):
            year = part[i:i+4]
            if year.startswith('20') and year.isdigit():
                return int(year)
    return None

def doesItParse(scriptPath):
    try:
        with open(scriptPath, 'r', encoding='utf-8-sig', errors='ignore') as file:
            code = file.read()

        clean_lines = []
        for line in code.splitlines():
            stripped_line = line.lstrip()
            if not stripped_line.startswith(('!', '%')):  # skip magic/shell commands
                clean_lines.append(line.rstrip())  # strip trailing whitespace

        cleanFile = '\n'.join(clean_lines)
        
        ast.parse(cleanFile, filename=scriptPath)
        return True
    except:
        return False
    
def cleanParseFile(scriptPath):
    with open(scriptPath, 'r', encoding='utf-8-sig', errors='ignore') as file:
        code = file.read()

    clean_lines = []
    for line in code.splitlines():
        stripped_line = line.lstrip()
        if not stripped_line.startswith(('!', '%')):  # skip magic/shell commands
            clean_lines.append(line.rstrip())  # strip trailing whitespace

    cleanFile = '\n'.join(clean_lines)
    return cleanFile