"""ORC exporter for NutritionEntry and DailySummary."""
from __future__ import annotations

import io
from typing import List

import pyarrow as pa
import pyarrow.orc as orc

from macro_sync.schema import DailySummary, NutritionEntry


def _entries_to_table(entries: List[NutritionEntry]) -> pa.Table:
    return pa.table(
        {
            "date": [e.date.isoformat() for e in entries],
            "source": [e.source for e in entries],
            "calories": [e.calories for e in entries],
            "protein_g": [e.protein_g for e in entries],
            "carbs_g": [e.carbs_g for e in entries],
            "fat_g": [e.fat_g for e in entries],
            "fiber_g": [e.fiber_g if e.fiber_g is not None else float("nan") for e in entries],
            "sugar_g": [e.sugar_g if e.sugar_g is not None else float("nan") for e in entries],
            "sodium_mg": [e.sodium_mg if e.sodium_mg is not None else float("nan") for e in entries],
        }
    )


def _summaries_to_table(summaries: List[DailySummary]) -> pa.Table:
    return pa.table(
        {
            "date": [s.date.isoformat() for s in summaries],
            "total_calories": [s.total_calories for s in summaries],
            "total_protein_g": [s.total_protein_g for s in summaries],
            "total_carbs_g": [s.total_carbs_g for s in summaries],
            "total_fat_g": [s.total_fat_g for s in summaries],
            "total_fiber_g": [s.total_fiber_g if s.total_fiber_g is not None else float("nan") for s in summaries],
            "total_sugar_g": [s.total_sugar_g if s.total_sugar_g is not None else float("nan") for s in summaries],
            "total_sodium_mg": [s.total_sodium_mg if s.total_sodium_mg is not None else float("nan") for s in summaries],
            "entry_count": [s.entry_count for s in summaries],
        }
    )


def entries_to_orc_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to ORC bytes."""
    table = _entries_to_table(entries)
    buf = io.BytesIO()
    orc.write_table(table, buf)
    return buf.getvalue()


def summaries_to_orc_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to ORC bytes."""
    table = _summaries_to_table(summaries)
    buf = io.BytesIO()
    orc.write_table(table, buf)
    return buf.getvalue()
