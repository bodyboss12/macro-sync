import csv
import io
from datetime import date
from typing import List, Union

from macro_sync.schema import NutritionEntry


def _parse_float(value: str) -> float:
    """Parse a float from a string, returning 0.0 if empty or invalid."""
    try:
        return float(value.strip()) if value.strip() else 0.0
    except (ValueError, AttributeError):
        return 0.0


def _parse_date(value: str) -> date:
    """Parse a date string in YYYY-MM-DD format."""
    return date.fromisoformat(value.strip())


def _parse_reader(reader: csv.DictReader) -> List[NutritionEntry]:
    """Parse rows from a DictReader into NutritionEntry objects."""
    entries = []
    for row in reader:
        # MyFitnessPal CSV export uses 'Date', 'Meal', 'Calories', etc.
        entry = NutritionEntry(
            date=_parse_date(row["Date"]),
            source="myfitnesspal",
            calories=_parse_float(row.get("Calories", "0")),
            protein_g=_parse_float(row.get("Protein (g)", "0")),
            carbs_g=_parse_float(row.get("Carbohydrates (g)", "0")),
            fat_g=_parse_float(row.get("Fat (g)", "0")),
            fiber_g=_parse_float(row.get("Fiber (g)", "")) or None,
            sugar_g=_parse_float(row.get("Sugar (g)", "")) or None,
            sodium_mg=_parse_float(row.get("Sodium (mg)", "")) or None,
        )
        entries.append(entry)
    return entries


def parse_csv(source: Union[str, io.TextIOBase]) -> List[NutritionEntry]:
    """Parse a MyFitnessPal nutrition export CSV.

    Args:
        source: A file path string or a text stream.

    Returns:
        A list of NutritionEntry objects.
    """
    if isinstance(source, str):
        with open(source, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return _parse_reader(reader)
    else:
        reader = csv.DictReader(source)
        return _parse_reader(reader)
