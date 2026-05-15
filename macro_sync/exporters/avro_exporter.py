"""Avro exporter for NutritionEntry and DailySummary lists."""
from __future__ import annotations

import io
from typing import List

import fastavro

from macro_sync.schema import DailySummary, NutritionEntry

_ENTRY_SCHEMA = {
    "type": "record",
    "name": "NutritionEntry",
    "fields": [
        {"name": "date", "type": "string"},
        {"name": "source", "type": "string"},
        {"name": "calories", "type": "double"},
        {"name": "protein", "type": "double"},
        {"name": "carbs", "type": "double"},
        {"name": "fat", "type": "double"},
        {"name": "fiber", "type": ["null", "double"], "default": None},
        {"name": "sugar", "type": ["null", "double"], "default": None},
        {"name": "sodium", "type": ["null", "double"], "default": None},
    ],
}

_SUMMARY_SCHEMA = {
    "type": "record",
    "name": "DailySummary",
    "fields": [
        {"name": "date", "type": "string"},
        {"name": "total_calories", "type": "double"},
        {"name": "total_protein", "type": "double"},
        {"name": "total_carbs", "type": "double"},
        {"name": "total_fat", "type": "double"},
        {"name": "total_fiber", "type": ["null", "double"], "default": None},
        {"name": "total_sugar", "type": ["null", "double"], "default": None},
        {"name": "total_sodium", "type": ["null", "double"], "default": None},
        {"name": "entry_count", "type": "int"},
    ],
}


def _prepare_entry(entry: NutritionEntry) -> dict:
    return {
        "date": entry.date.isoformat(),
        "source": entry.source,
        "calories": entry.calories,
        "protein": entry.protein,
        "carbs": entry.carbs,
        "fat": entry.fat,
        "fiber": entry.fiber,
        "sugar": entry.sugar,
        "sodium": entry.sodium,
    }


def _prepare_summary(summary: DailySummary) -> dict:
    return {
        "date": summary.date.isoformat(),
        "total_calories": summary.total_calories,
        "total_protein": summary.total_protein,
        "total_carbs": summary.total_carbs,
        "total_fat": summary.total_fat,
        "total_fiber": summary.total_fiber,
        "total_sugar": summary.total_sugar,
        "total_sodium": summary.total_sodium,
        "entry_count": summary.entry_count,
    }


def entries_to_avro_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to Avro bytes."""
    parsed_schema = fastavro.parse_schema(_ENTRY_SCHEMA)
    buf = io.BytesIO()
    fastavro.writer(buf, parsed_schema, [_prepare_entry(e) for e in entries])
    return buf.getvalue()


def summaries_to_avro_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to Avro bytes."""
    parsed_schema = fastavro.parse_schema(_SUMMARY_SCHEMA)
    buf = io.BytesIO()
    fastavro.writer(buf, parsed_schema, [_prepare_summary(s) for s in summaries])
    return buf.getvalue()
