"""ODS (OpenDocument Spreadsheet) exporter for NutritionEntry and DailySummary."""

from __future__ import annotations

import io
from typing import List

try:
    import pyexcel_ods3 as ods
except ImportError as exc:  # pragma: no cover
    raise ImportError("pyexcel-ods3 is required for ODS export: pip install pyexcel-ods3") from exc

from macro_sync.schema import NutritionEntry, DailySummary

_ENTRY_HEADERS = ["date", "source", "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g", "sodium_mg"]
_SUMMARY_HEADERS = ["date", "total_calories", "total_protein_g", "total_carbs_g", "total_fat_g", "entry_count"]


def _entry_row(entry: NutritionEntry) -> list:
    return [
        entry.date.isoformat(),
        entry.source,
        entry.calories,
        entry.protein_g,
        entry.carbs_g,
        entry.fat_g,
        entry.fiber_g,
        entry.sugar_g,
        entry.sodium_mg,
    ]


def _summary_row(summary: DailySummary) -> list:
    return [
        summary.date.isoformat(),
        summary.total_calories,
        summary.total_protein_g,
        summary.total_carbs_g,
        summary.total_fat_g,
        summary.entry_count,
    ]


def entries_to_ods_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to ODS bytes."""
    rows = [_ENTRY_HEADERS] + [_entry_row(e) for e in entries]
    data = {"Entries": rows}
    buf = io.BytesIO()
    ods.save_data(buf, data)
    return buf.getvalue()


def summaries_to_ods_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to ODS bytes."""
    rows = [_SUMMARY_HEADERS] + [_summary_row(s) for s in summaries]
    data = {"Summaries": rows}
    buf = io.BytesIO()
    ods.save_data(buf, data)
    return buf.getvalue()
