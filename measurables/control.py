import HardMetrics
import fileParsing
import applyMetrics

yuanFilePath = '/Users/yuan/Desktop/CS5 data/pre-LLM data/cs5/'
jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5/'
# jennyFilePath = '/Users/jennyngo/Documents/GitHub/Code-Heuristics/studentScripts'
#florenceFilePath = ''

for i in fileParsing.getPathsForYears(jennyFilePath, 2018, 2022):
    applyMetrics.metricsOnFilepath(i[0], i[1])