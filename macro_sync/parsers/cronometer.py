"""Parser for Cronometer CSV export data."""

import csv
import io
from datetime import date
from typing import List, Union

from macro_sync.schema import NutritionEntry

# Cronometer CSV column mappings
COLUMN_MAP = {
    "Date": "date",
    "Energy (kcal)": "calories",
    "Protein (g)": "protein_g",
    "Carbohydrates (g)": "carbs_g",
    "Fat (g)": "fat_g",
    "Fiber (g)": "fiber_g",
    "Sugar (g)": "sugar_g",
    "Sodium (mg)": "sodium_mg",
}


def _parse_float(value: str) -> float:
    """Parse a float from a string, returning 0.0 for empty/invalid values."""
    try:
        return float(value.strip()) if value.strip() else 0.0
    except ValueError:
        return 0.0


def _parse_date(value: str) -> date:
    """Parse a date string in YYYY-MM-DD format."""
    return date.fromisoformat(value.strip())


def parse_csv(source: Union[str, io.StringIO]) -> List[NutritionEntry]:
    """
    Parse a Cronometer CSV export into a list of NutritionEntry objects.

    Args:
        source: Either a file path string or a StringIO object containing CSV data.

    Returns:
        List of NutritionEntry instances, one per row.
    """
    if isinstance(source, str):
        with open(source, newline="", encoding="utf-8") as f:
            return _parse_reader(csv.DictReader(f))
    else:
        return _parse_reader(csv.DictReader(source))


def _parse_reader(reader: csv.DictReader) -> List[NutritionEntry]:
    entries = []
    for row in reader:
        entry = NutritionEntry(
            source="cronometer",
            date=_parse_date(row.get("Date", "")),
            calories=_parse_float(row.get("Energy (kcal)", "0")),
            protein_g=_parse_float(row.get("Protein (g)", "0")),
            carbs_g=_parse_float(row.get("Carbohydrates (g)", "0")),
            fat_g=_parse_float(row.get("Fat (g)", "0")),
            fiber_g=_parse_float(row.get("Fiber (g)", "")) or None,
            sugar_g=_parse_float(row.get("Sugar (g)", "")) or None,
            sodium_mg=_parse_float(row.get("Sodium (mg)", "")) or None,
        )
        entries.append(entry)
    return entries
