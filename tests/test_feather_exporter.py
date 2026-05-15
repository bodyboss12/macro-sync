"""Tests for the Feather exporter."""
from __future__ import annotations

import io
from datetime import date

import pyarrow.feather as feather
import pytest

from macro_sync.exporters.feather_exporter import (
    entries_to_feather_bytes,
    summaries_to_feather_bytes,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 1, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=5.0,
        sugar_g=10.0,
        sodium_mg=800.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 1, 15),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=250.0,
        total_fat_g=65.0,
        total_fiber_g=25.0,
        entry_count=4,
    )


def _read_table(data: bytes):
    return feather.read_table(io.BytesIO(data))


def test_entries_to_feather_bytes_returns_bytes(sample_entry):
    result = entries_to_feather_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_feather_bytes_nonempty(sample_entry):
    result = entries_to_feather_bytes([sample_entry])
    assert len(result) > 0


def test_entries_feather_row_count(sample_entry):
    result = entries_to_feather_bytes([sample_entry, sample_entry])
    table = _read_table(result)
    assert table.num_rows == 2


def test_entries_feather_columns(sample_entry):
    result = entries_to_feather_bytes([sample_entry])
    table = _read_table(result)
    assert "date" in table.column_names
    assert "calories" in table.column_names
    assert "protein_g" in table.column_names


def test_entries_feather_date_value(sample_entry):
    result = entries_to_feather_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("date")[0].as_py() == "2024-01-15"


def test_entries_feather_calorie_value(sample_entry):
    result = entries_to_feather_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("calories")[0].as_py() == 500.0


def test_summaries_to_feather_bytes_returns_bytes(sample_summary):
    result = summaries_to_feather_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_feather_row_count(sample_summary):
    result = summaries_to_feather_bytes([sample_summary, sample_summary])
    table = _read_table(result)
    assert table.num_rows == 2


def test_summaries_feather_columns(sample_summary):
    result = summaries_to_feather_bytes([sample_summary])
    table = _read_table(result)
    assert "date" in table.column_names
    assert "total_calories" in table.column_names
    assert "entry_count" in table.column_names


def test_entries_feather_empty_list():
    result = entries_to_feather_bytes([])
    table = _read_table(result)
    assert table.num_rows == 0


def test_entries_feather_optional_none():
    entry = NutritionEntry(
        date=date(2024, 3, 1),
        source="cronometer",
        calories=300.0,
        protein_g=20.0,
        carbs_g=40.0,
        fat_g=10.0,
    )
    result = entries_to_feather_bytes([entry])
    table = _read_table(result)
    assert table.num_rows == 1
