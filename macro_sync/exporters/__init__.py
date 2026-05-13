"""Exporters package for macro-sync."""

from macro_sync.exporters.csv_exporter import (
    entries_to_csv,
    entries_to_csv_str,
    summaries_to_csv,
    summaries_to_csv_str,
)
from macro_sync.exporters.json_exporter import (
    entries_to_json,
    entries_to_json_str,
    summaries_to_json,
    summaries_to_json_str,
)
from macro_sync.exporters.markdown_exporter import (
    entries_to_markdown,
    entries_to_markdown_str,
    summaries_to_markdown,
    summaries_to_markdown_str,
)

try:
    from macro_sync.exporters.excel_exporter import (
        entries_to_excel_bytes,
        entries_to_workbook,
        summaries_to_excel_bytes,
        summaries_to_workbook,
    )
except ImportError:
    pass  # openpyxl not installed; Excel export unavailable

__all__ = [
    "entries_to_csv",
    "entries_to_csv_str",
    "summaries_to_csv",
    "summaries_to_csv_str",
    "entries_to_json",
    "entries_to_json_str",
    "summaries_to_json",
    "summaries_to_json_str",
    "entries_to_markdown",
    "entries_to_markdown_str",
    "summaries_to_markdown",
    "summaries_to_markdown_str",
    "entries_to_excel_bytes",
    "entries_to_workbook",
    "summaries_to_excel_bytes",
    "summaries_to_workbook",
]
