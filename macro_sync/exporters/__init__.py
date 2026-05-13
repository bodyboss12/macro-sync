"""Exporters package for macro-sync.

Provides serialization utilities to export nutrition data
into various output formats.

Available modules:
    json_exporter: Export NutritionEntry and DailySummary objects to JSON.
"""

from macro_sync.exporters.json_exporter import (
    entries_to_json,
    entries_to_json_str,
    summaries_to_json,
    summaries_to_json_str,
)

__all__ = [
    "entries_to_json",
    "entries_to_json_str",
    "summaries_to_json",
    "summaries_to_json_str",
]
