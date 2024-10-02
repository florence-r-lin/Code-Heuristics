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
          
#initializing fieldDict
for i in fileList:
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

    for i in fileList:
        writer.writerow(x for x in i)

# depthList = []
# for i in fileList:
#     depthList.append(i[5][0])

weeksUsedList = []

for i in fileList:
    weeksUsedList.append(i[5])

print(weeksUsedList)
makeHistogram(weeksUsedList, 10, 'Weeks Used', 'Num Weeks')