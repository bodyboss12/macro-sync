"""Export nutrition data as JSON Lines (one JSON object per line, .jsonl/.jl).

Distinct from the existing ndjson/jsonl exporters — this one focuses on
streaming-friendly output with optional gzip compression.
"""
from __future__ import annotations

import gzip
import io
import json
from datetime import date
from typing import Iterable

from macro_sync.schema import DailySummary, NutritionEntry


def _default_serializer(obj: object) -> str:
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _entry_to_dict(entry: NutritionEntry) -> dict:
    return {
        "date": _default_serializer(entry.date),
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
        "date": _default_serializer(summary.date),
        "total_calories": summary.total_calories,
        "total_protein_g": summary.total_protein_g,
        "total_carbs_g": summary.total_carbs_g,
        "total_fat_g": summary.total_fat_g,
        "total_fiber_g": summary.total_fiber_g,
        "total_sugar_g": summary.total_sugar_g,
        "total_sodium_mg": summary.total_sodium_mg,
        "entry_count": summary.entry_count,
    }


def _compress_bytes(data: bytes) -> bytes:
    """Gzip-compress *data* and return the compressed bytes."""
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(data)
    return buf.getvalue()


def entries_to_jsonlines_str(entries: Iterable[NutritionEntry]) -> str:
    """Return newline-delimited JSON string for *entries*."""
    lines = [json.dumps(_entry_to_dict(e)) for e in entries]
    return "\n".join(lines) + ("\n" if lines else "")


def summaries_to_jsonlines_str(summaries: Iterable[DailySummary]) -> str:
    """Return newline-delimited JSON string for *summaries*."""
    lines = [json.dumps(_summary_to_dict(s)) for s in summaries]
    return "\n".join(lines) + ("\n" if lines else "")


def entries_to_jsonlines_bytes(entries: Iterable[NutritionEntry], *, compress: bool = False) -> bytes:
    """Return UTF-8 encoded JSON Lines bytes, optionally gzip-compressed."""
    raw = entries_to_jsonlines_str(entries).encode("utf-8")
    return _compress_bytes(raw) if compress else raw


def summaries_to_jsonlines_bytes(summaries: Iterable[DailySummary], *, compress: bool = False) -> bytes:
    """Return UTF-8 encoded JSON Lines bytes, optionally gzip-compressed."""
    raw = summaries_to_jsonlines_str(summaries).encode("utf-8")
    return _compress_bytes(raw) if compress else raw
