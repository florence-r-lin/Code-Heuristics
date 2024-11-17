import HardMetrics
import fileParsing
import shutil
from Histograms import makeHistogram, makeMultipleHistograms
import os
from os import listdir
from os.path import isfile, join
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import pandas as pd  # Make sure to import pandas for CSV handling
import fileinput

def metricsOnFilepath(inputFilepath, year, binNumsInput = None):
    filePath = inputFilepath
    metricsList = []
    binNums = [6, 30, 7, 30, 30] if binNumsInput == None else binNumsInput

    finalPyList = fileParsing.getAllPythonFilesInPath(filePath)

    for i in finalPyList:
        #preproccessing portion
        fileParsing.replaceErrorsInFile(i)
        #calling all metrics portion
        result = HardMetrics.allMetrics(i)
        if (result != None):
            metricsList.append(result)

    fieldDict = { # currently is only used for keys
        "File Name": [], 
        "LOC": [], 
        "Comment Percentage":[] , 
        "Number Of Functions": [], 
        "CycloComplexity": [],
        "Max Depth": [] , 
        "Weeks Covered": [] 
        }
            
    #initializing fieldDict
    for i in metricsList:
        fieldDict["File Name"].append(i[0])           # Assuming i[0] is File Name
        fieldDict["LOC"].append(i[1])                 # Assuming i[1] is LOC
        fieldDict["Comment Percentage"].append(i[2])  # Assuming i[2] is Comment Percentage
        fieldDict["Number Of Functions"].append(i[3]) # Assuming i[3] is Number Of Functions
        fieldDict["CycloComplexity"].append(i[4])     # Assuming i[4] is Cyclomatic Complexity
        fieldDict["Max Depth"].append(i[5])           # Assuming i[5] is Max Depth
        fieldDict["Weeks Covered"].append(i[6])       # Assuming i[6] is Weeks Covered


    with open('Metrics Score ' + str(year) + '.csv', 'w', newline='') as file:
        file.truncate(0) # clear file 
        writer = csv.writer(file)
        writer.writerow(fieldDict.keys())

        for i in metricsList:
            writer.writerow(x for x in i)

    Lines = []
    Comments = []
    FuncNum = []
    Cyclo =[]
    Depth = []
    weeksUsedList = []


    for i in metricsList:
        Lines.append(i[1])
        Comments.append(i[2])
        FuncNum.append(i[3])
        Cyclo.append(i[4])
        Depth.append(i[5])
        weeksUsedList.append(i[6])

    statsCsv = 'histogram_stats.csv'+ year
    outFolder = 'data' + year

    #To erase contents of folder, uncomment below
    shutil.rmtree(outFolder, ignore_errors=True)
    with open(statsCsv, 'w') as f:
        f.write('')

    # Individual histograms
    makeHistogram(weeksUsedList, numBins=6, graphName='Weeks Used', xaxis='Num Weeks', color=(217, 167, 202), 
                  fitLine=True, filename='weeks_used_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    makeHistogram(Comments, numBins=30, graphName='Comments', xaxis='Percentages', 
                  filename='comments_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    makeHistogram(FuncNum, numBins=7, graphName='Ambition', xaxis='Number Of Functions', 
                  filename='ambition_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    makeHistogram(Cyclo, numBins=30, graphName='Cyclomatic Complexity', xaxis='Cyclomatic Complexity', 
                  filename='cyclomatic_complexity_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    makeHistogram(Depth, numBins=5, graphName='Max Depth', xaxis='Depth', 
                  filename='maximum_depth_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    makeHistogram(Lines, numBins=30, graphName='Volume', xaxis='Lines Of Code', 
                  filename='volume_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
    
    inputList = [weeksUsedList, Comments, FuncNum, Cyclo, Depth, Lines]
    numBins = [6, 30, 7, 30, 5, 30]
    graphNames = ['Weeks Used', 'Comments', 'Ambition', 'Cyclomatic Complexity', 'Max Depth', 'Volume']
    xaxis = ['Num Weeks', 'Percentages', 'Number Of Functions', 'Cyclomatic Complexity', 'Depth', 'Lines Of Code']
    colors = [(217, 167, 202), (148, 181, 242), (120, 160, 240), (180, 140, 220), (230, 200, 250), (150, 180, 230)]
    filename = 'Combined Histogram' + year
    fitLine = [True] * len(inputList)  # all histograms to fit a line
    makeMultipleHistograms(
        inputList=inputList,
        numBins=numBins,
        graphName=graphNames,
        xaxis=xaxis,
        color=colors,
        fitLine=fitLine,  
        filename=filename,
        output_dir=outFolder
    )