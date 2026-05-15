"""Export a human-readable pivot report as plain text or markdown."""
from __future__ import annotations

from typing import List

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.pivot_summary import build_pivot, source_totals


def _fmt(val: float) -> str:
    return f"{val:.1f}"


def entries_to_pivot_text(entries: List[NutritionEntry]) -> str:
    """Render a plain-text pivot report grouped by date with source breakdown."""
    lines: list[str] = ["=== Pivot Report ===", ""]
    days = build_pivot(entries)
    for day in days:
        lines.append(f"Date: {day.date.isoformat()}")
        lines.append(f"  Total  | cal={_fmt(day.total_calories)} prot={_fmt(day.total_protein_g)} carbs={_fmt(day.total_carbs_g)} fat={_fmt(day.total_fat_g)} entries={day.entry_count}")
        for src, sb in sorted(day.by_source.items()):
            lines.append(f"  {src:<12}| cal={_fmt(sb.total_calories)} prot={_fmt(sb.total_protein_g)} carbs={_fmt(sb.total_carbs_g)} fat={_fmt(sb.total_fat_g)} entries={sb.entry_count}")
        lines.append("")

    totals = source_totals(entries)
    lines.append("=== Source Totals ===")
    for src, sb in sorted(totals.items()):
        lines.append(f"  {src:<12}| cal={_fmt(sb.total_calories)} prot={_fmt(sb.total_protein_g)} carbs={_fmt(sb.total_carbs_g)} fat={_fmt(sb.total_fat_g)} entries={sb.entry_count}")
    return "\n".join(lines)


def entries_to_pivot_markdown(entries: List[NutritionEntry]) -> str:
    """Render a markdown pivot report grouped by date."""
    lines: list[str] = ["# Pivot Report", ""]
    days = build_pivot(entries)
    for day in days:
        lines.append(f"## {day.date.isoformat()}")
        lines.append("")
        lines.append("| Source | Calories | Protein (g) | Carbs (g) | Fat (g) | Entries |")
        lines.append("|--------|----------|-------------|-----------|---------|---------|")
        for src, sb in sorted(day.by_source.items()):
            lines.append(f"| {src} | {_fmt(sb.total_calories)} | {_fmt(sb.total_protein_g)} | {_fmt(sb.total_carbs_g)} | {_fmt(sb.total_fat_g)} | {sb.entry_count} |")
        lines.append(f"| **Total** | **{_fmt(day.total_calories)}** | **{_fmt(day.total_protein_g)}** | **{_fmt(day.total_carbs_g)}** | **{_fmt(day.total_fat_g)}** | **{day.entry_count}** |")
        lines.append("")
    return "\n".join(lines)
