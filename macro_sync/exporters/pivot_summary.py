"""Compute pivot-style aggregations over NutritionEntry lists."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

from macro_sync.schema import NutritionEntry


@dataclass
class SourceBreakdown:
    source: str
    entry_count: int = 0
    total_calories: float = 0.0
    total_protein_g: float = 0.0
    total_carbs_g: float = 0.0
    total_fat_g: float = 0.0


@dataclass
class DayPivot:
    date: date
    total_calories: float = 0.0
    total_protein_g: float = 0.0
    total_carbs_g: float = 0.0
    total_fat_g: float = 0.0
    entry_count: int = 0
    by_source: Dict[str, SourceBreakdown] = field(default_factory=dict)


def build_pivot(entries: List[NutritionEntry]) -> List[DayPivot]:
    """Group entries by date and break down totals by source."""
    pivot_map: Dict[date, DayPivot] = {}

    for e in entries:
        if e.date not in pivot_map:
            pivot_map[e.date] = DayPivot(date=e.date)
        day = pivot_map[e.date]
        day.total_calories += e.calories or 0.0
        day.total_protein_g += e.protein_g or 0.0
        day.total_carbs_g += e.carbs_g or 0.0
        day.total_fat_g += e.fat_g or 0.0
        day.entry_count += 1

        src = e.source or "unknown"
        if src not in day.by_source:
            day.by_source[src] = SourceBreakdown(source=src)
        sb = day.by_source[src]
        sb.entry_count += 1
        sb.total_calories += e.calories or 0.0
        sb.total_protein_g += e.protein_g or 0.0
        sb.total_carbs_g += e.carbs_g or 0.0
        sb.total_fat_g += e.fat_g or 0.0

    return sorted(pivot_map.values(), key=lambda d: d.date)


def source_totals(entries: List[NutritionEntry]) -> Dict[str, SourceBreakdown]:
    """Aggregate totals across all dates, keyed by source."""
    totals: Dict[str, SourceBreakdown] = {}
    for e in entries:
        src = e.source or "unknown"
        if src not in totals:
            totals[src] = SourceBreakdown(source=src)
        sb = totals[src]
        sb.entry_count += 1
        sb.total_calories += e.calories or 0.0
        sb.total_protein_g += e.protein_g or 0.0
        sb.total_carbs_g += e.carbs_g or 0.0
        sb.total_fat_g += e.fat_g or 0.0
    return totals
