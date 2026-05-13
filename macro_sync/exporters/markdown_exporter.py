"""Markdown table exporter for nutrition entries and daily summaries."""

from typing import List
from macro_sync.schema import NutritionEntry, DailySummary


_ENTRY_HEADERS = ["Date", "Source", "Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"]
_SUMMARY_HEADERS = ["Date", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)", "Entries"]


def _md_row(cells: List[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def _md_separator(n: int) -> str:
    return "| " + " | ".join(["---"] * n) + " |"


def entries_to_markdown(entries: List[NutritionEntry]) -> List[str]:
    """Return list of markdown table lines for a list of NutritionEntry objects."""
    lines = [_md_row(_ENTRY_HEADERS), _md_separator(len(_ENTRY_HEADERS))]
    for e in entries:
        row = [
            str(e.date),
            e.source or "",
            e.food_name or "",
            f"{e.calories:.1f}" if e.calories is not None else "",
            f"{e.protein_g:.1f}" if e.protein_g is not None else "",
            f"{e.carbs_g:.1f}" if e.carbs_g is not None else "",
            f"{e.fat_g:.1f}" if e.fat_g is not None else "",
        ]
        lines.append(_md_row(row))
    return lines


def summaries_to_markdown(summaries: List[DailySummary]) -> List[str]:
    """Return list of markdown table lines for a list of DailySummary objects."""
    lines = [_md_row(_SUMMARY_HEADERS), _md_separator(len(_SUMMARY_HEADERS))]
    for s in summaries:
        row = [
            str(s.date),
            f"{s.total_calories:.1f}" if s.total_calories is not None else "",
            f"{s.total_protein_g:.1f}" if s.total_protein_g is not None else "",
            f"{s.total_carbs_g:.1f}" if s.total_carbs_g is not None else "",
            f"{s.total_fat_g:.1f}" if s.total_fat_g is not None else "",
            str(s.entry_count),
        ]
        lines.append(_md_row(row))
    return lines


def entries_to_markdown_str(entries: List[NutritionEntry]) -> str:
    """Return a markdown table string for a list of NutritionEntry objects."""
    return "\n".join(entries_to_markdown(entries))


def summaries_to_markdown_str(summaries: List[DailySummary]) -> str:
    """Return a markdown table string for a list of DailySummary objects."""
    return "\n".join(summaries_to_markdown(summaries))
