import HardMetrics
from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import csv
import fileinput

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

#print(getAllPythonFilesInPath('/Users/yuan/Desktop/CS5 data'))