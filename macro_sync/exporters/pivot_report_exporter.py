"""Plain-text and Markdown pivot report exporter."""
from __future__ import annotations

from typing import List

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.pivot_summary import build_pivot, source_totals


def _fmt(value: float) -> str:
    return f"{value:.1f}"


def entries_to_pivot_text(entries: List[NutritionEntry]) -> str:
    """Render a plain-text pivot report grouped by date with source breakdown."""
    days = build_pivot(entries)
    lines: List[str] = []
    lines.append(f"{'Date':<12} {'Source':<14} {'Calories':>10} {'Protein':>9} {'Carbs':>9} {'Fat':>9}")
    lines.append("-" * 68)
    for day in days:
        for src, bd in day.by_source.items():
            lines.append(
                f"{str(day.date):<12} {src:<14} {_fmt(bd.calories):>10}"
                f" {_fmt(bd.protein):>9} {_fmt(bd.carbs):>9} {_fmt(bd.fat):>9}"
            )
        lines.append(
            f"{'':12} {'TOTAL':<14} {_fmt(day.total_calories):>10}"
            f" {_fmt(day.total_protein):>9} {_fmt(day.total_carbs):>9} {_fmt(day.total_fat):>9}"
        )
        lines.append("")
    totals = source_totals(entries)
    lines.append("-" * 68)
    lines.append("Grand totals by source:")
    for src, bd in totals.items():
        lines.append(
            f"  {src:<14} {_fmt(bd.calories):>10} {_fmt(bd.protein):>9}"
            f" {_fmt(bd.carbs):>9} {_fmt(bd.fat):>9}"
        )
    return "\n".join(lines)


def entries_to_pivot_markdown(entries: List[NutritionEntry]) -> str:
    """Render a Markdown pivot report grouped by date with source breakdown."""
    days = build_pivot(entries)
    lines: List[str] = []
    lines.append("| Date | Source | Calories | Protein | Carbs | Fat |")
    lines.append("|------|--------|----------|---------|-------|-----|")
    for day in days:
        for src, bd in day.by_source.items():
            lines.append(
                f"| {day.date} | {src} | {_fmt(bd.calories)} |"
                f" {_fmt(bd.protein)} | {_fmt(bd.carbs)} | {_fmt(bd.fat)} |"
            )
        lines.append(
            f"| **{day.date}** | **TOTAL** | **{_fmt(day.total_calories)}** |"
            f" **{_fmt(day.total_protein)}** | **{_fmt(day.total_carbs)}** | **{_fmt(day.total_fat)}** |"
        )
    return "\n".join(lines)
