import HardMetrics
import fileParsing
import applyMetrics

yuanFilePath = '/Users/yuan/Desktop/CS5 data/pre-LLM data/cs5/'
jennyFilePath = '/Users/jennyngo/Downloads/CS5 DATA/pre-LLM data/cs5'
#florenceFilePath = ''

for i in fileParsing.getPathsForYears(yuanFilePath, 2018, 2022):
    applyMetrics.metricsOnFilepath(i[0], i[1])