"""Exporters package for macro-sync.

Provides helpers to export NutritionEntry and DailySummary objects
to various formats: JSON, CSV, Markdown, Excel, and SQLite.
"""

from macro_sync.exporters.json_exporter import (
    entries_to_json_str,
    summaries_to_json_str,
    entries_to_json,
    summaries_to_json,
)
from macro_sync.exporters.csv_exporter import (
    entries_to_csv_str,
    summaries_to_csv_str,
    entries_to_csv,
    summaries_to_csv,
)
from macro_sync.exporters.markdown_exporter import (
    entries_to_markdown_str,
    summaries_to_markdown_str,
    entries_to_markdown,
    summaries_to_markdown,
)
from macro_sync.exporters.excel_exporter import (
    entries_to_excel_bytes,
    summaries_to_excel_bytes,
    entries_to_workbook,
    summaries_to_workbook,
)
from macro_sync.exporters.sqlite_exporter import (
    entries_to_sqlite_bytes,
    summaries_to_sqlite_bytes,
    entries_to_connection,
    summaries_to_connection,
)

__all__ = [
    "entries_to_json_str",
    "summaries_to_json_str",
    "entries_to_json",
    "summaries_to_json",
    "entries_to_csv_str",
    "summaries_to_csv_str",
    "entries_to_csv",
    "summaries_to_csv",
    "entries_to_markdown_str",
    "summaries_to_markdown_str",
    "entries_to_markdown",
    "summaries_to_markdown",
    "entries_to_excel_bytes",
    "summaries_to_excel_bytes",
    "entries_to_workbook",
    "summaries_to_workbook",
    "entries_to_sqlite_bytes",
    "summaries_to_sqlite_bytes",
    "entries_to_connection",
    "summaries_to_connection",
]
