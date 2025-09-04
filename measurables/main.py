import HardMetrics
import fileParsing
import applyMetrics
import shutil
from Histograms import makeHistogram, makeMultipleHistograms
import textProcessing
import warnings
warnings.filterwarnings('ignore')


def main():
    stephanieFilePath = '/Users/summer-2024/Desktop/code metrics 25/All-Data/CS5-Data/assignments postllm/submissions_cs5_s2023'
    currentFilePath = stephanieFilePath

    textProcessing.notebookToPyOnFilePath(currentFilePath)
    textProcessing.removeEmptyFile(currentFilePath)

    applyMetrics.metricsOnFilepath(currentFilePath)

if __name__ == "__main__":
    main()

# statsCsv = 'histogram_stats.csv'
# outFolder = 'data'

# #To erase contents of folder, uncomment below
# shutil.rmtree(outFolder, ignore_errors=True)
# with open(statsCsv, 'w') as f:
#     f.write('')