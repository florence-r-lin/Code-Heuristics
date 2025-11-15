import applyMetrics
from Histograms import makeHistogram, makeMultipleHistograms
import textProcessing
import warnings
import argparse
warnings.filterwarnings('ignore')

import cProfile
import pstats

# TODO: Investigate alternative parsing methods for broken Python code
# The current AST strategy fails to collect metrics for code that cannot be parsed

def run_with_profiler(func):
    """Run a function with profiling and print performance statistics.

    This function wraps the execution of any given function with Python's cProfile
    profiler to measure performance metrics and execution time.

    :param func: Callable to be profiled
    :type func: callable
    :return: Result of the function execution
    :rtype: Any
    """
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func()
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
    
    return result

def process_metrics(filepath):
    """Process and analyze metrics for Python files in the given directory.

    This function performs the following operations:
    1. Converts any Jupyter notebooks to Python files
    2. Removes empty files
    3. Calculates metrics for all Python files

    :param filepath: Path to the directory containing Python projects
    :type filepath: str
    :return: List of metrics grouped by year
    :rtype: list[tuple[str, list[dict]]]
    """
    textProcessing.notebookToPyOnFilePath(filepath)
    textProcessing.removeEmptyFile(filepath)
    return applyMetrics.metricsOnFilepath(filepath)

def main():
    """Main entry point for the metrics calculation program.
    
    Parses command line arguments and runs the metrics analysis pipeline.
    Displays average metrics across all analyzed files.
    
    Command line arguments:
        -fp, --projects_path: Path to the Python projects to analyze
        -c, --csv_file: Optional path for CSV output
        -p, --profiler: Optional flag to enable performance profiling
    """
    parser = argparse.ArgumentParser(description='Run the Metrics')
    parser.add_argument('-fp', '--projects_path', type=str, required=True, help='Path to your python projects')
    parser.add_argument('-c', '--csv_file', type=str, required=False, help='Path to output CSV file')
    parser.add_argument('-p', '--profiler', type=bool, required=False, help='Here if you would like to see how long metrics take')
    
    args = parser.parse_args()
    
    if args.profiler:
        metrics_by_year = run_with_profiler(lambda: process_metrics(args.projects_path))
    else:
        metrics_by_year = process_metrics(args.projects_path)

    # to view more stats
    all_rows = []
    for _, rows in metrics_by_year:
        all_rows.extend(rows)

    if not all_rows:
        print("No metrics collected.")
        return

    from collections import defaultdict
    import numpy as np

    aggregate = defaultdict(list)

    for row in all_rows:
        for key, value in row.items():
            if isinstance(value, (int, float)):
                aggregate[key].append(value)

    print("\n=== Average Metrics Across All Files ===")
    for key, values in aggregate.items():
        avg = np.mean(values)
        print(f"{key}: {avg:.2f}")


if __name__ == "__main__":
    main()

# statsCsv = 'histogram_stats.csv'
# outFolder = 'data'

# To erase contents of folder, uncomment below
# shutil.rmtree(outFolder, ignore_errors=True)
# with open(statsCsv, 'w') as f:
#     f.write('')
