"""CBOR exporter for NutritionEntry and DailySummary objects."""
from __future__ import annotations

from datetime import date
from typing import Any

import cbor2

from macro_sync.schema import DailySummary, NutritionEntry


def _prepare_entry(entry: NutritionEntry) -> dict[str, Any]:
    """Convert a NutritionEntry to a CBOR-serialisable dict."""
    d = {
        "date": entry.date.isoformat() if isinstance(entry.date, date) else entry.date,
        "source": entry.source,
        "calories": entry.calories,
        "protein_g": entry.protein_g,
        "carbs_g": entry.carbs_g,
        "fat_g": entry.fat_g,
    }
    if entry.fiber_g is not None:
        d["fiber_g"] = entry.fiber_g
    if entry.sugar_g is not None:
        d["sugar_g"] = entry.sugar_g
    if entry.sodium_mg is not None:
        d["sodium_mg"] = entry.sodium_mg
    return d


def _prepare_summary(summary: DailySummary) -> dict[str, Any]:
    """Convert a DailySummary to a CBOR-serialisable dict."""
    return {
        "date": summary.date.isoformat() if isinstance(summary.date, date) else summary.date,
        "total_calories": summary.total_calories,
        "total_protein_g": summary.total_protein_g,
        "total_carbs_g": summary.total_carbs_g,
        "total_fat_g": summary.total_fat_g,
        "total_fiber_g": summary.total_fiber_g,
        "total_sugar_g": summary.total_sugar_g,
        "total_sodium_mg": summary.total_sodium_mg,
        "entry_count": summary.entry_count,
    }


def entries_to_cbor_bytes(entries: list[NutritionEntry]) -> bytes:
    """Serialise a list of NutritionEntry objects to CBOR bytes."""
    payload = [_prepare_entry(e) for e in entries]
    return cbor2.dumps(payload)


def summaries_to_cbor_bytes(summaries: list[DailySummary]) -> bytes:
    """Serialise a list of DailySummary objects to CBOR bytes."""
    payload = [_prepare_summary(s) for s in summaries]
    return cbor2.dumps(payload)


def entries_from_cbor_bytes(data: bytes) -> list[dict[str, Any]]:
    """Deserialise CBOR bytes back to a list of dicts."""
    return cbor2.loads(data)


def summaries_from_cbor_bytes(data: bytes) -> list[dict[str, Any]]:
    """Deserialise CBOR bytes back to a list of dicts."""
    return cbor2.loads(data)
