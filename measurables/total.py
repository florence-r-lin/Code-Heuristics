import HardMetrics
import fileParsing
from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import csv
import fileinput



# yuanFilePath = '/Users/yuan/Desktop/CS5 data/pre-LLM data/cs5'#/2018 pre llm'#summer cs5 2024 section 1'
jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5'
#florenceFilePath = ''

print(fileParsing.getPathsForYears("/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/", 2018, 2023))

filePath = jennyFilePath
metricsList = []

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
    fieldDict["Weeks Covered"].append(i[5])       # Assuming i[6] is Weeks Covered


with open('Metrics Score.csv', 'w', newline='') as file:
    file.truncate(0) # clear file 
    writer = csv.writer(file)
    writer.writerow(fieldDict.keys())

    for i in metricsList:
        writer.writerow(x for x in i)

# depthList = []
# for i in fileList:
#     depthList.append(i[5][0])


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
    weeksUsedList.append(i[5])

statsCsv = 'histogram_stats.csv'
with open(statsCsv, 'w') as f:
    f.write('')
makeHistogram(weeksUsedList, numBins=6, graphName='Weeks Used', xaxis='Num Weeks', color=(217, 167, 202), fitLine=True, filename='weeks_used_histogram.png',csv_filename = statsCsv)
makeHistogram(Comments, numBins=30, graphName='Comments', xaxis='Percentages', filename='comments_histogram.png', csv_filename = statsCsv)
makeHistogram(FuncNum, numBins=7, graphName='Ambition', xaxis='Number Of Functions', filename='ambition_histogram.png', csv_filename = statsCsv)
makeHistogram(Cyclo, numBins=30, graphName='Cyclomatic Complexity', xaxis='Cyclomatic Complexity', filename='cyclomatic_complexity_histogram.png', csv_filename = statsCsv)
makeHistogram(Lines, numBins=30, graphName='Volume', xaxis='Lines Of Code', filename='volume_histogram.png', csv_filename = statsCsv)
