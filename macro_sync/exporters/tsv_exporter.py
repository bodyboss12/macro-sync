"""TSV (Tab-Separated Values) exporter for NutritionEntry and DailySummary."""

from __future__ import annotations

import csv
import io
from typing import List

from macro_sync.schema import DailySummary, NutritionEntry

_ENTRY_FIELDS = [
    "date", "source", "food_name", "calories", "protein_g",
    "carbs_g", "fat_g", "fiber_g", "sugar_g", "sodium_mg",
]

_SUMMARY_FIELDS = [
    "date", "total_calories", "total_protein_g", "total_carbs_g",
    "total_fat_g", "total_fiber_g", "total_sugar_g", "total_sodium_mg",
    "entry_count",
]


def _serialize_value(value) -> str:
    if value is None:
        return ""
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


def entries_to_tsv_str(entries: List[NutritionEntry]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=_ENTRY_FIELDS, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    for entry in entries:
        d = entry.to_dict()
        writer.writerow({f: _serialize_value(d.get(f)) for f in _ENTRY_FIELDS})
    return buf.getvalue()


def summaries_to_tsv_str(summaries: List[DailySummary]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(
        buf, fieldnames=_SUMMARY_FIELDS, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    for summary in summaries:
        d = summary.to_dict()
        writer.writerow({f: _serialize_value(d.get(f)) for f in _SUMMARY_FIELDS})
    return buf.getvalue()


def entries_to_tsv(entries: List[NutritionEntry]) -> bytes:
    return entries_to_tsv_str(entries).encode("utf-8")


def summaries_to_tsv(summaries: List[DailySummary]) -> bytes:
    return summaries_to_tsv_str(summaries).encode("utf-8")
