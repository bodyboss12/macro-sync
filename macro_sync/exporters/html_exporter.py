"""HTML exporter for NutritionEntry and DailySummary lists."""

from __future__ import annotations

from typing import IO, List

from macro_sync.schema import DailySummary, NutritionEntry

_ENTRY_HEADERS = ["date", "source", "calories", "protein", "carbs", "fat", "fiber", "sugar", "sodium"]
_SUMMARY_HEADERS = ["date", "total_calories", "total_protein", "total_carbs", "total_fat", "entry_count"]


def _html_table(headers: List[str], rows: List[List[str]]) -> str:
    header_cells = "".join(f"<th>{h}</th>" for h in headers)
    header_row = f"<tr>{header_cells}</tr>"
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    body = "\n".join(body_rows)
    return f"<table>\n<thead>\n{header_row}\n</thead>\n<tbody>\n{body}\n</tbody>\n</table>"


def entries_to_html_str(entries: List[NutritionEntry]) -> str:
    rows = [
        [
            str(e.date),
            e.source,
            str(e.calories) if e.calories is not None else "",
            str(e.protein) if e.protein is not None else "",
            str(e.carbs) if e.carbs is not None else "",
            str(e.fat) if e.fat is not None else "",
            str(e.fiber) if e.fiber is not None else "",
            str(e.sugar) if e.sugar is not None else "",
            str(e.sodium) if e.sodium is not None else "",
        ]
        for e in entries
    ]
    table = _html_table(_ENTRY_HEADERS, rows)
    return f"<!DOCTYPE html>\n<html>\n<body>\n{table}\n</body>\n</html>\n"


def summaries_to_html_str(summaries: List[DailySummary]) -> str:
    rows = [
        [
            str(s.date),
            str(s.total_calories),
            str(s.total_protein),
            str(s.total_carbs),
            str(s.total_fat),
            str(s.entry_count),
        ]
        for s in summaries
    ]
    table = _html_table(_SUMMARY_HEADERS, rows)
    return f"<!DOCTYPE html>\n<html>\n<body>\n{table}\n</body>\n</html>\n"


def entries_to_html(entries: List[NutritionEntry], stream: IO[str]) -> None:
    stream.write(entries_to_html_str(entries))


def summaries_to_html(summaries: List[DailySummary], stream: IO[str]) -> None:
    stream.write(summaries_to_html_str(summaries))
