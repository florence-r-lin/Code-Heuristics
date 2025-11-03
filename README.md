# Code Heuristics

A Python-based tool for analyzing code metrics and quality heuristics in Python source files. This project provides comprehensive analysis of code characteristics including complexity metrics, documentation coverage, and structural patterns.

## Features

- **Code Metrics Analysis**
  - Lines of Code (LOC)
  - Comment and Docstring Coverage
  - Function Analysis (count and length)
  - Loop Analysis (count and length)
  - Cyclomatic Complexity
  - Nested Depth Analysis

- **Performance Monitoring**
  - Execution Time Tracking
  - Memory Usage Analysis
  - Performance Profiling Support

- **Data Processing**
  - Jupyter Notebook to Python Conversion
  - Empty File Detection and Handling
  - Batch Processing Support
  - CSV Export Capabilities

## Project Structure

```
src/
  Metrics/
    applyMetrics.py      # Core metrics computation and export
    Cyclomatic.py        # Cyclomatic complexity analysis
    fileParsing.py       # File handling and parsing utilities
    HardMetrics.py       # Core metric calculations
    Histograms.py        # Data visualization tools
    main.py             # Main execution entry point
    NestedDepth.py      # Nested structure analysis
    submission.py       # Submission handling
    textProcessing.py   # Text processing utilities
tests/
    test_files.py       # File handling tests
    test_metrics.py     # Metrics calculation tests
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Yuan-Garcia/Code-Heuristics.git
cd Code-Heuristics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Basic Usage:
```python
from src.Metrics import main
main.main()
```

2. Custom Analysis:
```python
from src.Metrics import applyMetrics
metrics = applyMetrics.metricsOnFilepath("/path/to/your/code")
```

## Metrics Description

- **LOC (Lines of Code)**: Total number of code lines excluding comments and blank lines
- **Comment Percentage**: Percentage of lines that contain comments
- **Docstring Percentage**: Percentage of documented functions/classes
- **Blank Percentage**: Percentage of blank lines
- **Number of Functions**: Total function count
- **Average Function Length**: Mean length of functions in lines
- **Number of Loops**: Total loop count
- **Average Loop Length**: Mean length of loops in lines
- **Cyclomatic Complexity**: Measure of code complexity based on control flow
- **Max Depth**: Maximum nesting depth in the code

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.