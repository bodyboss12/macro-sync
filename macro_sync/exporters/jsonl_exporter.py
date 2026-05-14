"""JSONL (JSON Lines) exporter — one JSON object per line, newline-delimited."""
from __future__ import annotations

import io
import json
from datetime import date
from typing import IO, List

from macro_sync.schema import DailySummary, NutritionEntry


def _default_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _entry_to_dict(entry: NutritionEntry) -> dict:
    return {
        "date": entry.date,
        "source": entry.source,
        "food_name": entry.food_name,
        "calories": entry.calories,
        "protein_g": entry.protein_g,
        "carbs_g": entry.carbs_g,
        "fat_g": entry.fat_g,
        "fiber_g": entry.fiber_g,
        "sugar_g": entry.sugar_g,
        "sodium_mg": entry.sodium_mg,
    }


def _summary_to_dict(summary: DailySummary) -> dict:
    return {
        "date": summary.date,
        "total_calories": summary.total_calories,
        "total_protein_g": summary.total_protein_g,
        "total_carbs_g": summary.total_carbs_g,
        "total_fat_g": summary.total_fat_g,
        "total_fiber_g": summary.total_fiber_g,
        "total_sugar_g": summary.total_sugar_g,
        "total_sodium_mg": summary.total_sodium_mg,
        "entry_count": summary.entry_count,
    }


def entries_to_jsonl_str(entries: List[NutritionEntry]) -> str:
    lines = [
        json.dumps(_entry_to_dict(e), default=_default_serializer)
        for e in entries
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def summaries_to_jsonl_str(summaries: List[DailySummary]) -> str:
    lines = [
        json.dumps(_summary_to_dict(s), default=_default_serializer)
        for s in summaries
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def entries_to_jsonl(entries: List[NutritionEntry], stream: IO[bytes]) -> None:
    stream.write(entries_to_jsonl_str(entries).encode("utf-8"))


def summaries_to_jsonl(summaries: List[DailySummary], stream: IO[bytes]) -> None:
    stream.write(summaries_to_jsonl_str(summaries).encode("utf-8"))
