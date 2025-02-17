import HardMetrics
from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import csv
import fileinput
import ast

def getPathsForYears(intoOverallFilePath, startYear, endYear):
    pathList = []
    for i in range(endYear-startYear+1):
        pathName = intoOverallFilePath + str((startYear + i)) + " pre llm/"
        pathList.append([pathName, str((startYear + i))])
    return pathList

def getChildFolderNames(folderPath):
    folderTree = list(os.walk(folderPath))
    return folderTree[0][1]

#print(getChildFolderNames('/Users/yuan/Desktop/CS5 data'))

def getFullPathName(folderPath):
    childFolderNames = getChildFolderNames(folderPath)
    return [join(folderPath, i) for i in childFolderNames]

#print(getFullPathName('/Users/yuan/Desktop/CS5 data'))

def replaceErrorsInFile(filePath):
    HardMetrics.replaceInFile(filePath, "GlowScript", "#")
    HardMetrics.replaceInFile(filePath, "Web VPython", "#")
    HardMetrics.replaceInFile(filePath, "    if mag( wpos_noy - bpos_noy ) < smallest_dim \\",
                               "    if mag( wpos_noy - bpos_noy ) < smallest_dim or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):")
    HardMetrics.replaceInFile(filePath, "       or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):", "#")
    HardMetrics.replaceInFile(filePath, "else if", "elif")
    HardMetrics.replaceInFile(filePath, "%matplotlib inline", "#")
    HardMetrics.replaceInFile(filePath, "!git", "#")
    HardMetrics.replaceInFile(filePath, "%cd", "#")
    HardMetrics.replaceInFile(filePath, "!python", "#")
    HardMetrics.replaceInFile(filePath, "!tar", "#")
    HardMetrics.replaceInFile(filePath, "!pip", "#")
    HardMetrics.replaceInFile(filePath, "pip", "#")
    HardMetrics.replaceInFile(filePath, "%pwd", "#")
    HardMetrics.replaceInFile(filePath, "cd ..", "#")



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

def doesItParse(scriptPath):
    try:
        with open(scriptPath, "r") as file:
            s = file.read()
            isOnlyComments(s)
            tree = ast.parse(s, filename=scriptPath)
        return True
    except:
        return False

def isOnlyComments(inputStr):
    nonCommentList = []
    for i in inputStr:
        if not(i == "\n"):
           nonCommentList.append(i)
    if len(nonCommentList) == 0:
        print("Comment only file")
        raise Exception ("Comment only file")


def isAPythonFinal(filePath):
    fileName = filePath.split("/")[-1]
    return fileName[0:6] == "final|" and fileName[-3:] == ".py"

def backOneDir(filePath):
    return "/".join(filePath.split("/")[:-1])



#print(getAllPythonFilesInPath('/Users/yuan/Desktop/CS5 data'))

