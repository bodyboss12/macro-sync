import csv
import io
from datetime import date
from typing import List, Union

from macro_sync.schema import NutritionEntry, DailySummary

_ENTRY_FIELDS = [
    "date",
    "source",
    "calories",
    "protein_g",
    "carbs_g",
    "fat_g",
    "fiber_g",
    "sugar_g",
    "sodium_mg",
]

_SUMMARY_FIELDS = [
    "date",
    "total_calories",
    "total_protein_g",
    "total_carbs_g",
    "total_fat_g",
    "total_fiber_g",
    "total_sugar_g",
    "total_sodium_mg",
    "entry_count",
]


def _serialize_value(value):
    if isinstance(value, date):
        return value.isoformat()
    if value is None:
        return ""
    return value


def entries_to_csv(entries: List[NutritionEntry], stream: io.TextIOBase) -> None:
    writer = csv.DictWriter(stream, fieldnames=_ENTRY_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for entry in entries:
        row = {field: _serialize_value(getattr(entry, field, None)) for field in _ENTRY_FIELDS}
        writer.writerow(row)


def summaries_to_csv(summaries: List[DailySummary], stream: io.TextIOBase) -> None:
    writer = csv.DictWriter(stream, fieldnames=_SUMMARY_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for summary in summaries:
        row = {field: _serialize_value(getattr(summary, field, None)) for field in _SUMMARY_FIELDS}
        writer.writerow(row)


def entries_to_csv_str(entries: List[NutritionEntry]) -> str:
    buf = io.StringIO()
    entries_to_csv(entries, buf)
    return buf.getvalue()


def summaries_to_csv_str(summaries: List[DailySummary]) -> str:
    buf = io.StringIO()
    summaries_to_csv(summaries, buf)
    return buf.getvalue()
