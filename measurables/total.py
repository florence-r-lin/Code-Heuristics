import HardMetrics
import fileParsing
from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import csv
import fileinput



yuanFilePath = '/Users/yuan/Desktop/CS5 data/post-LLM data'#summer cs5 2024 section 1'
#jennyFilePath = ''
#florenceFilePath = ''

filePath = yuanFilePath
metricsList = []

finalPyList = fileParsing.getAllPythonFilesInPath(filePath)

for i in finalPyList:
    #preproccessing portion
    fileParsing.replaceErrorsInFile(i)
    #calling all metrics portion
    metricsList.append((HardMetrics.allMetrics(i)))

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

#print(weeksUsedList)
makeHistogram(weeksUsedList, 6, 'Weeks Used', 'Num Weeks')
makeHistogram(Comments, 30, 'Comments', 'Percentages')
makeHistogram(FuncNum, 10, 'Ambition', 'Number Of Functions')
makeHistogram(Cyclo, 30, 'Cyclomatic complexity', 'Cyclomatic complexity')
makeHistogram(Lines, 5, 'Volume', 'Lines Of Code')