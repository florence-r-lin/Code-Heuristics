import HardMetrics
import fileParsing
import applyMetrics

yuanFilePath = '/Users/yuan/Desktop/CS5 data/pre-LLM data/cs5/'
jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5/'
# jennyFilePath = '/Users/jennyngo/Documents/GitHub/Code-Heuristics/studentScripts'
#florenceFilePath = ''

pathList = fileParsing.getPathsForYears(yuanFilePath, 2018, 2023)
for i in pathList:
    applyMetrics.metricsOnFilepath(i[0], i[1])
applyMetrics.metricsOnFilepath(pathList[2][0], pathList[2][1], [6, 8, 6, 8, 8])
