from HardMetrics import HardMetrics
from Histograms import makeHistogram
from os import listdir
from os.path import isfile, join
import csv

onlyfiles = [f for f in listdir("studentScripts")]
#test
onlyfiles = [join("studentscripts/", f) for f in onlyfiles]
# print(onlyfiles)

fileList = []

for i in onlyfiles:
    fileList.append(HardMetrics(i)[1])

fieldDict = { # currently is only used for keys
    "File Name": [], 
    "LOC": [], 
    "Comment Percentage":[] , 
    "Number Of Functions": [], 
    "CycloComplexity": [],
    "Max Depth": [] , 
    "Weeks Covered": [] 
    }
          
with open('Metrics Numeber Score.csv', 'w', newline='') as file:
    file.truncate(0) # clear file 
    writer = csv.writer(file)
    writer.writerow(fieldDict.keys())

    for i in fileList:
        writer.writerow(x for x in i)

depthList = []
for i in fileList:
    depthList.append(i[5][0])

weeksUsedList = []

for i in fileList:
    weeksUsedList.append(i[6])

print(weeksUsedList)
makeHistogram(weeksUsedList, 10, 'Weeks Used', 'Num Weeks')