import HardMetrics
from Histograms import makeHistogram
import os
from os import listdir
from os.path import isfile, join
import csv
import fileinput



yuanFilePath = '/Users/yuan/Downloads/Some year cs5'
#jennyFilePath = ''
#florenceFilePath = ''

filePath = yuanFilePath

#TODO: turn this into a function, probably called pruning



result = list(os.walk(filePath))
pathList = []


for folder_tuple in result:
    currentpath, subfolder, files = folder_tuple

    if '__MACOSX' in currentpath: continue

    for file in files:
        pathList.append(currentpath + "/" + file)
        
finalPyList = [f for f in pathList if f.endswith('.py')]


metricsList = []

# TODO: figure out what to do with the taken out Vpython files :(

for i in finalPyList:
    #if not(HardMetrics.containsString("VPython", HardMetrics.noCommentsFromFile(i))):
    HardMetrics.replaceInFile(i, "GlowScript", "#")
    HardMetrics.replaceInFile(i, "    if mag( wpos_noy - bpos_noy ) < smallest_dim \\",
                               "    if mag( wpos_noy - bpos_noy ) < smallest_dim or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):")
    HardMetrics.replaceInFile(i, "       or (-wLENGTH < b_axial < wLENGTH and -wWIDTH < b_perp < wWIDTH):", "#")
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
makeHistogram(weeksUsedList, 10, 'Weeks Used', 'Num Weeks')
makeHistogram(Comments, 100, 'Weeks Used', 'Num Weeks')
makeHistogram(FuncNum, 10, 'Weeks Used', 'Num Weeks')
makeHistogram(Cyclo, 10, 'Weeks Used', 'Num Weeks')
makeHistogram(Lines, 10, 'Weeks Used', 'Num Weeks')

