import HardMetrics
import fileParsing
import applyMetrics
import shutil
from Histograms import makeHistogram, makeMultipleHistograms
import textProcessing
import warnings
warnings.filterwarnings('ignore')

yuanFilePath = '/Users/yuan/Desktop/Work/School/Research/CS5 DATA/post-LLM data/cs35/'

# jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5/'
#florenceFilePath = ''

yearsLines = []
yearsComments = []
yearsFuncNum = []
yearsCyclo =[]
yearsDepth = []
yearsweeksUsedList = []
yearsTotal = []

#print(applyMetrics.metricsOnFilepath("/", 1999))

textProcessing.notebookToPyOnFilePath(yuanFilePath)
textProcessing.removeEmptyFile(yuanFilePath)


applyMetrics.metricsOnFilepath(yuanFilePath, 2024)
pathList = fileParsing.getPathsForYears(yuanFilePath, 2018, 2023)
for i in pathList:
    yearsTotal.append(applyMetrics.metricsOnFilepath(i[0], i[1]))

for i in yearsTotal:
    yearsLines.append([i[0],i[1][0]])
    yearsComments.append([i[0],i[1][1]])
    yearsFuncNum.append([i[0],i[1][2]])
    yearsCyclo.append([i[0],i[1][3]])
    yearsDepth.append([i[0],i[1][4]])
    yearsweeksUsedList.append([i[0],i[1][5]])

print(yearsLines)

statsCsv = 'histogram_stats.csv'
outFolder = 'data'

#To erase contents of folder, uncomment below
shutil.rmtree(outFolder, ignore_errors=True)
with open(statsCsv, 'w') as f:
    f.write('')