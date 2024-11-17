import HardMetrics
import fileParsing
import applyMetrics
import shutil
from Histograms import makeHistogram, makeMultipleHistograms

# yuanFilePath = '/Users/yuan/Desktop/CS5 data/pre-LLM data/cs5/'
jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5/'
#florenceFilePath = ''

yearsLines = []
yearsComments = []
yearsFuncNum = []
yearsCyclo =[]
yearsDepth = []
yearsweeksUsedList = []

# applyMetrics.metricsOnFilepath(jennyFilePath, 2024)
pathList = fileParsing.getPathsForYears(jennyFilePath, 2018, 2023)
for i in pathList:
    yearsDepth.append(applyMetrics.metricsOnFilepath(i[0], i[1]))
    print(yearsDepth)
applyMetrics.metricsOnFilepath(pathList[2][0], pathList[2][1], [6, 8, 6, 8, 8])

statsCsv = 'histogram_stats.csv'
outFolder = 'data'

#To erase contents of folder, uncomment below
shutil.rmtree(outFolder, ignore_errors=True)
with open(statsCsv, 'w') as f:
    f.write('')