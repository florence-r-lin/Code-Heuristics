import HardMetrics
import fileParsing
import applyMetrics
import shutil
from Histograms import makeHistogram, makeMultipleHistograms
import textProcessing
import warnings
warnings.filterwarnings('ignore')

import cProfile
import pstats

# currently the AST strategy fails to collect metrics for any code that cannot be parsed
# it looks like there are other ways to parse broken Python code which we might want to look into

def main():
    stephanieFilePath = '/Users/summer-2024/Desktop/code metrics 25/All-Data/CS5-Data/assignments postllm/submissions_cs5_s2023'
    yuanFilePath = "/Users/yuan/Desktop/Work/School/Research/CS5 DATA/pre-llm data/cs5/2019 pre llm"
    currentFilePath = stephanieFilePath

    profiler = cProfile.Profile()
    profiler.enable()

    textProcessing.notebookToPyOnFilePath(currentFilePath)
    textProcessing.removeEmptyFile(currentFilePath)

    applyMetrics.metricsOnFilepath(currentFilePath)

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')

    stats.print_stats()

if __name__ == "__main__":
    main()

# statsCsv = 'histogram_stats.csv'
# outFolder = 'data'

# #To erase contents of folder, uncomment below
# shutil.rmtree(outFolder, ignore_errors=True)
# with open(statsCsv, 'w') as f:
#     f.write('')
