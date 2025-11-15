"""Compute and export metrics produced by `HardMetrics`.

This module assumes `HardMetrics.allMetrics(path)` returns a `MetricRecord` dataclass.
It provides a small dict/attribute fallback for backward compatibility. The module
is intentionally small and focuses on: discovering files, invoking `allMetrics`,
normalizing the result to a canonical CSV row, grouping by year, and writing CSVs.
"""

# above docstring is outdated, we can rewrite it once the code is finalized

from __future__ import annotations

import csv
from dataclasses import is_dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

import fileParsing
from submission import Submission



FIELDNAMES = [
    "File Name",
    "LOC",
    "Comment Percentage",
    "Docstring Percentage",
    "Blank Percentage",
    "Number Of Functions",
    "Average Function Length",
    "Number of Loops",
    "Average Loop Length",
    "CycloComplexity",
    "Max Depth",
    "Execution Time",
    "Class",
    "Semester",
    "Year",
]


def _to_row(obj: Any) -> Dict[str, Any]:
    """Convert a MetricRecord (or legacy dict/obj) to a canonical CSV row dict.

    Prefer dataclass conversion. If a dict is provided, use its keys.
    If an object with attributes is provided, attempt to read common attribute names.
    """
    if obj is None:
        return {}

    if is_dataclass(obj):
        data = asdict(obj)
    elif isinstance(obj, dict):
        data = obj
    else:
        data = {}
        for attr in (
            "file",
            "loc",
            "comment_pct",
            "doc_pct",
            "blank_pct",
            "num_funcs",
            "avg_func_len",
            "num_loops",
            "avg_loop_len",
            "cyclo",
            "max_depth",
            "exec_time",
            "class_name",
            "semester",
            "year",
        ):
            if hasattr(obj, attr):
                data[attr] = getattr(obj, attr)

    mapping = {
        "File Name": ("File Name", "file", "scriptPath"),
        "LOC": ("LOC", "loc"),
        "Comment Percentage": ("Comment Percentage", "comment_pct"),
        "Docstring Percentage": ("Docstring Percentage", "doc_pct"),
        "Blank Percentage": ("Blank Percentage", "blank_pct"),
        "Number Of Functions": ("Number Of Functions", "num_funcs"),
        "Average Function Length": ("Average Function Length", "avg_func_len"),
        "Number of Loops": ("Number of Loops", "num_loops"),
        "Average Loop Length": ("Average Loop Length", "avg_loop_len"),
        "CycloComplexity": ("CycloComplexity", "cyclo"),
        "Max Depth": ("Max Depth", "max_depth"),
        "Execution Time": ("Execution Time", "exec_time"),
        "Class": ("Class", "class_name", "class"),
        "Semester": ("Semester", "semester"),
        "Year": ("Year", "year"),
    }

    out: Dict[str, Any] = {}
    for canonical, candidates in mapping.items():
        val = None
        for c in candidates:
            if c in data and data[c] is not None:
                val = data[c]
                break
        out[canonical] = val
    return out


def _write_per_year(metrics_by_year: Dict[Optional[int], List[Dict[str, Any]]], output_dir: Optional[Path] = None) -> None:
    """Write one CSV file per-year containing the metric rows."""
    if output_dir is None:
        output_dir = Path.cwd()

    for year, rows in metrics_by_year.items():
        filename = output_dir / f"Metrics Score {year if year is not None else 'unknown'}.csv"
        with filename.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
            writer.writeheader()
            for r in rows:
                writer.writerow({k: r.get(k) for k in FIELDNAMES})


# this is the main attraction
def metricsOnFilepath(input_filepath: str, write_csv: bool = True) -> List[List[Any]]:
    """Discover Python files under `input_filepath`, compute metrics and group by year.

    Returns: list of [year, rows] pairs where rows are canonical dicts matching FIELDNAMES.
    """
    base = Path(input_filepath)
    all_files = fileParsing.getAllPythonFilesInPath(str(base))
    files = sorted(set(all_files))

    metrics_by_year: Dict[Optional[int], List[Dict[str, Any]]] = {}


    for fp in files:
        if not fileParsing.isAPythonFile(fp):
            continue

        try:
            fileParsing.replaceErrorsInFile(fp)
        except Exception:
            # ignore and continue
            pass

        submission = Submission(fp)
        raw = submission.get_metrics()  
        row = _to_row(raw)
        if not row:
            continue

        year = row.get("Year")
        metrics_by_year.setdefault(year, []).append(row)


    if write_csv:
        _write_per_year(metrics_by_year)

    return [[year, rows] for year, rows in metrics_by_year.items()]


def sortDataByYear(metrics_list: List[Dict[str, Any]]) -> Dict[Any, List[Dict[str, Any]]]:
    """Group a list of normalized metric dicts by Year."""
    by_year: Dict[Any, List[Dict[str, Any]]] = {}
    for m in metrics_list:
        year = m.get("Year")
        by_year.setdefault(year, []).append(m)
    return by_year


__all__ = ["metricsOnFilepath", "sortDataByYear"]