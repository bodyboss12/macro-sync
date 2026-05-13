"""Export nutrition data to TOML format."""

from __future__ import annotations

from typing import IO, List

try:
    import tomllib  # Python 3.11+
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

import tomli_w

from macro_sync.schema import DailySummary, NutritionEntry


def _prepare_entry(entry: NutritionEntry) -> dict:
    d = {
        "date": entry.date.isoformat(),
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


def _prepare_summary(summary: DailySummary) -> dict:
    return {
        "date": summary.date.isoformat(),
        "total_calories": summary.total_calories,
        "total_protein_g": summary.total_protein_g,
        "total_carbs_g": summary.total_carbs_g,
        "total_fat_g": summary.total_fat_g,
        "entry_count": summary.entry_count,
    }


def entries_to_toml_str(entries: List[NutritionEntry]) -> str:
    """Serialize a list of NutritionEntry objects to a TOML string."""
    payload = {"entries": [_prepare_entry(e) for e in entries]}
    return tomli_w.dumps(payload)


def summaries_to_toml_str(summaries: List[DailySummary]) -> str:
    """Serialize a list of DailySummary objects to a TOML string."""
    payload = {"summaries": [_prepare_summary(s) for s in summaries]}
    return tomli_w.dumps(payload)


def entries_to_toml(entries: List[NutritionEntry], stream: IO[bytes]) -> None:
    """Write entries as TOML to a binary stream."""
    stream.write(entries_to_toml_str(entries).encode())


def summaries_to_toml(summaries: List[DailySummary], stream: IO[bytes]) -> None:
    """Write summaries as TOML to a binary stream."""
    stream.write(summaries_to_toml_str(summaries).encode())
