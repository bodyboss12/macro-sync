import csv
import io
from datetime import date

import pytest

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.csv_exporter import (
    entries_to_csv_str,
    summaries_to_csv_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=8.0,
        sugar_g=10.0,
        sodium_mg=400.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=60.0,
        total_fiber_g=25.0,
        total_sugar_g=40.0,
        total_sodium_mg=1500.0,
        entry_count=4,
    )


def test_entries_to_csv_str_is_valid_csv(sample_entry):
    result = entries_to_csv_str([sample_entry])
    reader = csv.DictReader(io.StringIO(result))
    rows = list(reader)
    assert len(rows) == 1


def test_entries_to_csv_str_date_serialized(sample_entry):
    result = entries_to_csv_str([sample_entry])
    assert "2024-03-15" in result


def test_entries_to_csv_str_fields(sample_entry):
    result = entries_to_csv_str([sample_entry])
    reader = csv.DictReader(io.StringIO(result))
    row = next(reader)
    assert row["source"] == "myfitnesspal"
    assert float(row["calories"]) == 500.0
    assert float(row["protein_g"]) == 30.0
    assert float(row["carbs_g"]) == 60.0
    assert float(row["fat_g"]) == 15.0


def test_entries_to_csv_str_optional_none_is_empty_string():
    entry = NutritionEntry(
        date=date(2024, 3, 15),
        source="cronometer",
        calories=300.0,
        protein_g=20.0,
        carbs_g=40.0,
        fat_g=10.0,
    )
    result = entries_to_csv_str([entry])
    reader = csv.DictReader(io.StringIO(result))
    row = next(reader)
    assert row["fiber_g"] == ""
    assert row["sugar_g"] == ""


def test_summaries_to_csv_str_is_valid_csv(sample_summary):
    result = summaries_to_csv_str([sample_summary])
    reader = csv.DictReader(io.StringIO(result))
    rows = list(reader)
    assert len(rows) == 1


def test_summaries_to_csv_str_fields(sample_summary):
    result = summaries_to_csv_str([sample_summary])
    reader = csv.DictReader(io.StringIO(result))
    row = next(reader)
    assert row["date"] == "2024-03-15"
    assert float(row["total_calories"]) == 1800.0
    assert int(row["entry_count"]) == 4


def test_entries_to_csv_str_multiple_rows(sample_entry):
    entries = [sample_entry, sample_entry]
    result = entries_to_csv_str(entries)
    reader = csv.DictReader(io.StringIO(result))
    rows = list(reader)
    assert len(rows) == 2
