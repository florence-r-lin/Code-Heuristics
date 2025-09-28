"""Run HardMetrics across a set of Python files and export per-year CSV summaries.

This module focuses on clarity and safety:
- Accepts either the legacy list output or newer dict output from HardMetrics.allMetrics.
- Groups metrics by year using dicts for readability.
- Writes CSVs using csv.DictWriter for column-safe output.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict, List
import dataclasses

import fileParsing
import HardMetrics


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


def _normalize_metrics(raw: Any) -> Dict[str, Any]:
    """Normalize different shapes (MetricRecord/dataclass, dict, list) to a flat dict keyed by FIELDNAMES."""
    if raw is None:
        return {}

    # If it's a dataclass (MetricRecord), convert to dict first
    if dataclasses.is_dataclass(raw):
        data = dataclasses.asdict(raw)
    elif isinstance(raw, dict):
        data = raw
    elif isinstance(raw, (list, tuple)):
        # legacy list order
        try:
            keys = [
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
            data = dict(zip(keys, raw))
        except Exception:
            return {}
    else:
        return {}

    # mapping of canonical FIELDNAMES to candidate keys in `data`
    key_candidates = {
        "File Name": ["File Name", "file", "scriptPath"],
        "LOC": ["LOC", "loc"],
        "Comment Percentage": ["Comment Percentage", "comment_pct"],
        "Docstring Percentage": ["Docstring Percentage", "doc_pct"],
        "Blank Percentage": ["Blank Percentage", "blank_pct"],
        "Number Of Functions": ["Number Of Functions", "num_funcs"],
        "Average Function Length": ["Average Function Length", "avg_func_len"],
        "Number of Loops": ["Number of Loops", "num_loops"],
        "Average Loop Length": ["Average Loop Length", "avg_loop_len"],
        "CycloComplexity": ["CycloComplexity", "cyclo"],
        "Max Depth": ["Max Depth", "max_depth"],
        "Execution Time": ["Execution Time", "exec_time"],
        "Class": ["Class", "class_name", "class"],
        "Semester": ["Semester", "semester"],
        "Year": ["Year", "year"],
    }

    out: Dict[str, Any] = {}
    for canonical, candidates in key_candidates.items():
        for c in candidates:
            if c in data and data[c] is not None:
                out[canonical] = data[c]
                break
        else:
            out[canonical] = None
    return out


def metricsOnFilepath(input_filepath: str, write_csv: bool = True) -> List[List[Any]]:
    """Compute metrics across Python files under input_filepath and optionally write per-year CSVs.

    Returns a list [[year, [metrics_dicts...]], ...]
    """
    base = Path(input_filepath)
    all_files = fileParsing.getAllPythonFilesInPath(str(base))
    files = sorted(set(all_files))

    metrics_by_year: Dict[Any, List[Dict[str, Any]]] = {}

    for fp in files:
        if not fileParsing.isAPythonFile(fp):
            continue

        # attempt to clean file in-place as previous code did
        try:
            fileParsing.replaceErrorsInFile(fp)
        except Exception:
            # non-fatal
            pass

        raw = HardMetrics.allMetrics(fp)
        nm = _normalize_metrics(raw)
        if not nm:
            continue

        year = nm.get("Year")
        metrics_by_year.setdefault(year, []).append(nm)

    if write_csv:
        for year, rows in metrics_by_year.items():
            out = Path(f"Metrics Score {year}.csv")
            with out.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
                writer.writeheader()
                for r in rows:
                    # ensure all fields present
                    row = {k: r.get(k) for k in FIELDNAMES}
                    writer.writerow(row)

    return [[year, rows] for year, rows in metrics_by_year.items()]


def sortDataByYear(metrics_list: List[Dict[str, Any]]) -> Dict[Any, List[Dict[str, Any]]]:
    """Utility: group already-normalized metric dicts by Year.

    Accepts a list of metric dicts (as returned by _normalize_metrics) and groups them.
    """
    by_year: Dict[Any, List[Dict[str, Any]]] = {}
    for m in metrics_list:
        year = m.get("Year")
        by_year.setdefault(year, []).append(m)
    return by_year


__all__ = ["metricsOnFilepath", "sortDataByYear"]