"""Build pivot structures from NutritionEntry lists."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from macro_sync.schema import NutritionEntry


@dataclass
class SourceBreakdown:
    calories: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0


@dataclass
class DayPivot:
    date: date
    entry_count: int = 0
    total_calories: float = 0.0
    total_protein_g: float = 0.0
    total_carbs_g: float = 0.0
    total_fat_g: float = 0.0
    by_source: Dict[str, SourceBreakdown] = field(default_factory=dict)


def build_pivot(entries: List[NutritionEntry]) -> List[DayPivot]:
    """Aggregate entries into per-day DayPivot objects, sorted by date."""
    index: Dict[date, DayPivot] = {}
    for entry in entries:
        pivot = index.setdefault(entry.date, DayPivot(date=entry.date))
        pivot.entry_count += 1
        pivot.total_calories += entry.calories or 0.0
        pivot.total_protein_g += entry.protein_g or 0.0
        pivot.total_carbs_g += entry.carbs_g or 0.0
        pivot.total_fat_g += entry.fat_g or 0.0

        src = pivot.by_source.setdefault(entry.source, SourceBreakdown())
        src.calories += entry.calories or 0.0
        src.protein_g += entry.protein_g or 0.0
        src.carbs_g += entry.carbs_g or 0.0
        src.fat_g += entry.fat_g or 0.0

    return sorted(index.values(), key=lambda d: d.date)


def source_totals(pivots: List[DayPivot]) -> Dict[str, SourceBreakdown]:
    """Collapse per-day source breakdowns into overall source totals."""
    totals: Dict[str, SourceBreakdown] = {}
    for pivot in pivots:
        for src, bd in pivot.by_source.items():
            agg = totals.setdefault(src, SourceBreakdown())
            agg.calories += bd.calories
            agg.protein_g += bd.protein_g
            agg.carbs_g += bd.carbs_g
            agg.fat_g += bd.fat_g
    return totals
