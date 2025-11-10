# Code Heuristics

Code Heuristics is a small, practical toolkit that analyzes Python source files and computes code-quality metrics and heuristics. It is targeted for researchers and educators who want fast, batchable metrics across many student submissions or code repositories.

## Highlights

- Lightweight, file-level metrics computed directly from Python source
- Batch processing across directories (including conversion of Jupyter notebooks)
- Exportable CSV output and basic histogram visualizations
- Command-line interface and importable API for custom processing

## Quick start

1. Clone the repository and enter the project folder:

```bash
git clone https://github.com/Yuan-Garcia/Code-Heuristics.git
cd Code-Heuristics
```

2. (Optional) create a Python virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run the CLI over a folder of Python projects or student submissions:

```bash
python -m src.Metrics.main -fp /path/to/projects
```

Add `-p True` to enable the profiler output (shows cProfile statistics).

## Command-line interface

The main CLI is implemented in `src/Metrics/main.py`.

Usage:

```text
python src/Metrics/main.py -fp <projects_path> [-c <csv_file>] [-p <ProfilerFlag>]
```

- `-fp, --projects_path` (required): Path to the directory containing Python files / project folders.
- `-c, --csv_file` (optional): Path where a CSV summary will be written (if supported by configuration).
- `-p, --profiler` (optional): If provided (e.g. `-p True`) the run will print cProfile statistics.

Example:

```bash
python src/Metrics/main.py -fp "Your/Filepath"
```

## API usage (importable)

You can import functions directly from the `src.Metrics` package in Python scripts or notebooks.

Example:

```python
from src.Metrics import applyMetrics

# returns a list of tuples (year, rows)
metrics_by_year = applyMetrics.metricsOnFilepath("/path/to/projects")

# each row is a dict-like record with the FIELDNAMES defined in applyMetrics
```

## What the tool computes

The project computes a set of file-level metrics. Typical metrics include:

- LOC (Lines of Code): number of non-blank, non-comment lines
- Comment Percentage: percent of lines that are comments
- Docstring Percentage: percent of functions / classes with docstrings
- Blank Percentage: percent of blank lines
- Number of Functions: functions defined in the file
- Average Function Length: mean lines per function
- Number of Loops: total `for`/`while` loops
- Average Loop Length: mean lines per loop
- Cyclomatic Complexity: control-flow complexity measure computed by `Cyclomatic.py`
- Max Depth: maximum nesting depth from `NestedDepth.py`

Refer to `src/Metrics/HardMetrics.py`, `Cyclomatic.py` and `NestedDepth.py` for the exact calculations and edge-case behavior.

## Project layout

```
src/
  Metrics/
    applyMetrics.py      # orchestrates metric collection and CSV output
    Cyclomatic.py        # cyclomatic complexity calculator
    fileParsing.py       # helpers for locating/reading files
    HardMetrics.py       # core metrics implementations
    Histograms.py        # utilities for histogram images
    main.py               # CLI entrypoint
    NestedDepth.py       # nested-depth and call-chain analysis
    submission.py        # Submission model and helpers
    textProcessing.py    # notebook conversion and file cleanup
tests/
  test_files.py          # unit tests for file parsing
  test_metrics.py        # unit tests for metrics
```

## Running tests

Run the tests with pytest from the repository root:

```bash
pytest -q
```

If tests require additional dependencies, install them using the project's `requirements.txt`.

## Developer notes

- The pipeline currently uses Python's AST for parsing; files that cannot be parsed will be skipped by the AST-based analysis. Consider using tolerant/parsing libraries if you expect broken syntax input.
- `main.py` includes a small profiler wrapper (`run_with_profiler`) which prints `cProfile` statistics when enabled.
- `applyMetrics.metricsOnFilepath()` is the high-level function that discovers files and returns canonical metric rows; see `applyMetrics.py` for field names and CSV export behavior.

## Contributing

Contributions are welcome. Please:

1. Fork the repo.
2. Create a topic branch: `git checkout -b feature/your-feature`.
3. Make changes and add tests for new behavior.
4. Run tests locally: `pytest -q`.
5. Open a pull request describing your change.

## Troubleshooting

- If the CLI prints "No metrics collected.", verify the `-fp` path and that it contains `.py` files or Jupyter notebooks convertible to Python.
- For profiling output: pass `-p True` to the CLI; heavy runs can produce large cProfile dumps.

## License

This project is distributed under the MIT License. See `LICENSE` for details.