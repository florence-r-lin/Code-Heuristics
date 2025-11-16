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
    return applyMetrics.metricsOnFilepath(filepath, write_csv = False)

def main():
    import argparse
    import csv
    from applyMetrics import FIELDNAMES  # Assuming you have this

    # Add your CSV flag **after** existing parsing
    parser = argparse.ArgumentParser(description='Run the Metrics')
    parser.add_argument('-fp', '--projects_path', type=str, required=True, help='Path to your python projects')
    parser.add_argument('-p', '--profiler', type=bool, required=False, help='Here if you would like to see how long metrics take')
    parser.add_argument('--csv_out', type=str, required=False, help='Path/filename for the output CSV')

    args = parser.parse_args()

    if args.profiler:
        metrics_by_year = run_with_profiler(lambda: process_metrics(args.projects_path))
    else:
        metrics_by_year = process_metrics(args.projects_path)

    # Collect rows (existing code)
    all_rows = []
    for _, rows in metrics_by_year:
        all_rows.extend(rows)

    if not all_rows:
        print("No metrics collected.")
    else:
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


        csv_path = args.csv_out or args.csv_file 
        if csv_path:
            try:
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
                    writer.writeheader()
                    for row in all_rows:
                        writer.writerow(row)
                print(f"\nCSV written to: {csv_path}")
            except Exception as e:
                print(f"Error writing CSV: {e}")


if __name__ == "__main__":
    main()
