"""LaTeX table exporter for NutritionEntry and DailySummary lists."""
from __future__ import annotations

from typing import List

from macro_sync.schema import DailySummary, NutritionEntry

_ENTRY_COLS = ["date", "source", "calories", "protein_g", "carbs_g", "fat_g"]
_SUMMARY_COLS = ["date", "total_calories", "total_protein_g", "total_carbs_g", "total_fat_g", "entry_count"]


def _escape(value: str) -> str:
    """Escape special LaTeX characters in a string."""
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    for char, replacement in replacements.items():
        value = value.replace(char, replacement)
    return value


def _serialize(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return _escape(str(value))


def _build_table(cols: List[str], rows: List[List[str]]) -> str:
    col_spec = "l" * len(cols)
    header = " & ".join(_escape(c) for c in cols) + r" \\"
    lines = [
        r"\begin{tabular}{" + col_spec + "}",
        r"\hline",
        header,
        r"\hline",
    ]
    for row in rows:
        lines.append(" & ".join(row) + r" \\")
    lines += [r"\hline", r"\end{tabular}"]
    return "\n".join(lines)


def entries_to_latex_str(entries: List[NutritionEntry]) -> str:
    rows = [
        [_serialize(getattr(e, c, None)) for c in _ENTRY_COLS]
        for e in entries
    ]
    return _build_table(_ENTRY_COLS, rows)


def summaries_to_latex_str(summaries: List[DailySummary]) -> str:
    rows = [
        [_serialize(getattr(s, c, None)) for c in _SUMMARY_COLS]
        for s in summaries
    ]
    return _build_table(_SUMMARY_COLS, rows)


def entries_to_latex(entries: List[NutritionEntry]) -> bytes:
    return entries_to_latex_str(entries).encode("utf-8")


def summaries_to_latex(summaries: List[DailySummary]) -> bytes:
    return summaries_to_latex_str(summaries).encode("utf-8")
