"""Tests for the TSV exporter."""

import csv
import io
from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.tsv_exporter import (
    entries_to_tsv,
    entries_to_tsv_str,
    summaries_to_tsv,
    summaries_to_tsv_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=54.0,
        fat_g=5.0,
        fiber_g=4.0,
        sugar_g=1.0,
        sodium_mg=120.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein_g=150.0,
        total_carbs_g=200.0,
        total_fat_g=70.0,
        total_fiber_g=25.0,
        total_sugar_g=50.0,
        total_sodium_mg=2300.0,
        entry_count=5,
    )


def _parse_tsv(text: str):
    return list(csv.DictReader(io.StringIO(text), delimiter="\t"))


def test_entries_to_tsv_str_is_valid_tsv(sample_entry):
    result = entries_to_tsv_str([sample_entry])
    rows = _parse_tsv(result)
    assert len(rows) == 1


def test_entries_to_tsv_str_date_serialized(sample_entry):
    result = entries_to_tsv_str([sample_entry])
    rows = _parse_tsv(result)
    assert rows[0]["date"] == "2024-03-15"


def test_entries_to_tsv_str_fields(sample_entry):
    result = entries_to_tsv_str([sample_entry])
    rows = _parse_tsv(result)
    assert rows[0]["source"] == "myfitnesspal"
    assert rows[0]["food_name"] == "Oatmeal"
    assert rows[0]["calories"] == "300.0"


def test_entries_to_tsv_str_optional_none(sample_entry):
    sample_entry.fiber_g = None
    result = entries_to_tsv_str([sample_entry])
    rows = _parse_tsv(result)
    assert rows[0]["fiber_g"] == ""


def test_entries_to_tsv_returns_bytes(sample_entry):
    result = entries_to_tsv([sample_entry])
    assert isinstance(result, bytes)
    assert b"Oatmeal" in result


def test_summaries_to_tsv_str_is_valid_tsv(sample_summary):
    result = summaries_to_tsv_str([sample_summary])
    rows = _parse_tsv(result)
    assert len(rows) == 1


def test_summaries_to_tsv_str_fields(sample_summary):
    result = summaries_to_tsv_str([sample_summary])
    rows = _parse_tsv(result)
    assert rows[0]["total_calories"] == "2000.0"
    assert rows[0]["entry_count"] == "5"
    assert rows[0]["date"] == "2024-03-15"


def test_summaries_to_tsv_returns_bytes(sample_summary):
    result = summaries_to_tsv([sample_summary])
    assert isinstance(result, bytes)
    assert b"2000.0" in result
