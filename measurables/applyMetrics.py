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


def metricsOnFilepath(inputFilepath, binNumsInput = None):
    filePath = inputFilepath
    metricsList = []
    # binNums = [6, 30, 7, 30, 30] if binNumsInput == None else binNumsInput

    finalPyList = fileParsing.getAllPythonFilesInPath(filePath)
    # print(list(set(finalPyList)))    
    for i in list(set(finalPyList)):
        # preproccessing portion
        fileParsing.replaceErrorsInFile(i)
        # calling all metrics portion
        # TODO: put in isAPythonFinal function in here!
        result = None
        if(fileParsing.isAPythonFile(i)):
            result = HardMetrics.allMetrics(i)
        if (result != None):
            metricsList.append(result)

    dataByYear = {}

    for i in metricsList:
        year = i[14] # change year !!!
        if year not in dataByYear:
            dataByYear[year] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], []] # 15

        # scriptPath, totalLOC, commentPercentage, docstringPercentage, blankPercentage, lenFuncs, avgFuncLen, numLoops, avgLoopLen, totalCC, ambitionScore, executionTime, Class, Semester, Year
        dataByYear[year][0].append(i[0]) # File Name
        dataByYear[year][1].append(i[1]) # LOC
        dataByYear[year][2].append(i[2]) # Comment Percentage
        dataByYear[year][3].append(i[3]) # Docstring Percentage
        dataByYear[year][4].append(i[4]) # Blank Percentage
        dataByYear[year][5].append(i[5]) # Number of Functions
        dataByYear[year][6].append(i[6]) # Average Function Length
        dataByYear[year][7].append(i[7]) # Number of Loops
        dataByYear[year][8].append(i[8]) # Average Loop Length
        dataByYear[year][9].append(i[9]) # Cyclo Complexity
        dataByYear[year][10].append(i[10]) # Max Depth
        dataByYear[year][11].append(i[11]) # Execution Time
        dataByYear[year][12].append(i[12]) # Class
        dataByYear[year][13].append(i[13]) # Semester
        dataByYear[year][14].append(i[14]) # Year

    dataByYearList = []
    for year, data in dataByYear.items():
        dataByYearList.append([year, data])

    fieldDict = { # currently is only used for keys
            "File Name": [], 
            "LOC": [], 
            "Comment Percentage": [], 
            "Docstring Percentage": [],
            "Blank Percentage": [], 
            "Number Of Functions": [], 
            "Average Function Length": [],
            "Number of Loops": [],
            "Average Loop Length": [],
            "CycloComplexity": [],
            "Max Depth": [], 
            "Execution Time": [],
            "Class": [],
            "Semester": [],
            "Year": []
            }
    
    for year, data in dataByYear.items():
        outputFile = f'Metrics Score {year}.csv'
        with open(outputFile, 'w', newline='') as file:
            file.truncate(0) # clear file 
            writer = csv.writer(file)
            writer.writerow(fieldDict.keys())

            for i in range(len(data[0])):
                writer.writerow([
                    data[0][i], 
                    data[1][i], 
                    data[2][i], 
                    data[3][i], 
                    data[4][i], 
                    data[5][i], 
                    data[6][i], 
                    data[7][i], 
                    data[8][i],
                    data[9][i],
                    data[10][i],
                    data[11][i],
                    data[12][i],
                    data[13][i],
                    year
                ])

    return dataByYearList

print(metricsOnFilepath('/Users/summer-2024/Desktop/code metrics 25/All-Data/CS35-Data/assignments postllm/submissions_cs35_sp2025/submission_351/final|hw4pr1 .py'))
# ['filepath', 800, 24.75, 4.125, 37.25, 7, 12.857142857142858, 3, 3.0, 11, 1, 1.3178491592407227, 'CS35', 'sp2025', 2025]
# ['filepath', 800, 24.75, 4.125, 37.25, 7, 12.857142857142858, 3, 3.0, 11, 1, 1.287416934967041, 'CS35', 'sp2025', 2025]

# statsCsv = 'histogram_stats.csv'
# outFolder = 'data'

# #To erase contents of folder, uncomment below
# shutil.rmtree(outFolder, ignore_errors=True)
# with open(statsCsv, 'w') as f:
#     f.write('')


# # Individual histograms
# makeHistogram(weeksUsedList, numBins=6, graphName='Weeks Used', xaxis='Num Weeks', color=(217, 167, 202), 
#                 fitLine=True, filename='weeks_used_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
# makeHistogram(Comments, numBins=30, graphName='Comments', xaxis='Percentages', 
#                 filename='comments_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
# makeHistogram(FuncNum, numBins=7, graphName='Ambition', xaxis='Number Of Functions', 
#                 filename='ambition_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
# makeHistogram(Cyclo, numBins=30, graphName='Cyclomatic Complexity', xaxis='Cyclomatic Complexity', 
#                 filename='cyclomatic_complexity_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
# makeHistogram(Depth, numBins=5, graphName='Max Depth', xaxis='Depth', 
#                 filename='maximum_depth_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)
# makeHistogram(Lines, numBins=30, graphName='Volume', xaxis='Lines Of Code', 
#                 filename='volume_histogram_' + str(year) + '.png', csv_filename=statsCsv, output_dir=outFolder)

# inputList = [weeksUsedList, Comments, FuncNum, Cyclo, Depth, Lines]
# numBins = [6, 30, 7, 30, 5, 30]
# graphNames = ['Weeks Used', 'Comments', 'Ambition', 'Cyclomatic Complexity', 'Max Depth', 'Volume']
# xaxis = ['Num Weeks', 'Percentages', 'Number Of Functions', 'Cyclomatic Complexity', 'Depth', 'Lines Of Code']
# colors = [(217, 167, 202), (148, 181, 242), (120, 160, 240), (180, 140, 220), (230, 200, 250), (150, 180, 230)]
# filename = 'Combined Histogram' + year
# fitLine = [True] * len(inputList)  # all histograms to fit a line
# makeMultipleHistograms(
#     inputList=inputList,
#     numBins=numBins,
#     graphName=graphNames,
#     xaxis=xaxis,
#     color=colors,
#     fitLine=fitLine,  
#     filename=filename,
#     output_dir=outFolder
# )