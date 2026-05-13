"""Aggregates NutritionEntry lists from multiple sources into DailySummary objects."""

from collections import defaultdict
from datetime import date
from typing import List, Dict

from macro_sync.schema import NutritionEntry, DailySummary


def merge_entries(entry_lists: List[List[NutritionEntry]]) -> List[NutritionEntry]:
    """Flatten multiple lists of NutritionEntry into a single list."""
    merged: List[NutritionEntry] = []
    for entries in entry_lists:
        merged.extend(entries)
    return merged


def group_by_date(entries: List[NutritionEntry]) -> Dict[date, List[NutritionEntry]]:
    """Group a flat list of NutritionEntry objects by their date."""
    groups: Dict[date, List[NutritionEntry]] = defaultdict(list)
    for entry in entries:
        groups[entry.date].append(entry)
    return dict(groups)


def aggregate(entry_lists: List[List[NutritionEntry]]) -> List[DailySummary]:
    """
    Merge entries from multiple sources and produce one DailySummary per date.

    Returns summaries sorted ascending by date.
    """
    all_entries = merge_entries(entry_lists)
    grouped = group_by_date(all_entries)

    summaries: List[DailySummary] = []
    for day_date in sorted(grouped.keys()):
        summary = DailySummary.from_entries(grouped[day_date])
        summaries.append(summary)

    return summaries
