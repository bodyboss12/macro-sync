"""Tests for the ORC exporter."""
from __future__ import annotations

import io
from datetime import date

import pyarrow.orc as orc
import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.orc_exporter import entries_to_orc_bytes, summaries_to_orc_bytes


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 10),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=8.0,
        sugar_g=12.0,
        sodium_mg=400.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 10),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=240.0,
        total_fat_g=60.0,
        total_fiber_g=30.0,
        total_sugar_g=50.0,
        total_sodium_mg=1600.0,
        entry_count=4,
    )


def _read_table(data: bytes):
    return orc.read_table(io.BytesIO(data))


def test_entries_to_orc_bytes_returns_bytes(sample_entry):
    result = entries_to_orc_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_orc_bytes_nonempty(sample_entry):
    result = entries_to_orc_bytes([sample_entry])
    assert len(result) > 0


def test_entries_orc_row_count(sample_entry):
    result = entries_to_orc_bytes([sample_entry, sample_entry])
    table = _read_table(result)
    assert table.num_rows == 2


def test_entries_orc_columns(sample_entry):
    result = entries_to_orc_bytes([sample_entry])
    table = _read_table(result)
    assert "date" in table.column_names
    assert "calories" in table.column_names
    assert "protein_g" in table.column_names


def test_entries_orc_date_value(sample_entry):
    result = entries_to_orc_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("date")[0].as_py() == "2024-03-10"


def test_entries_orc_calorie_value(sample_entry):
    result = entries_to_orc_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("calories")[0].as_py() == pytest.approx(500.0)


def test_summaries_to_orc_bytes_returns_bytes(sample_summary):
    result = summaries_to_orc_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_orc_row_count(sample_summary):
    result = summaries_to_orc_bytes([sample_summary])
    table = _read_table(result)
    assert table.num_rows == 1


def test_summaries_orc_entry_count_column(sample_summary):
    result = summaries_to_orc_bytes([sample_summary])
    table = _read_table(result)
    assert table.column("entry_count")[0].as_py() == 4


def test_entries_orc_optional_none_is_nan(sample_entry):
    entry = NutritionEntry(
        date=date(2024, 3, 11),
        source="cronometer",
        calories=300.0,
        protein_g=20.0,
        carbs_g=40.0,
        fat_g=10.0,
    )
    result = entries_to_orc_bytes([entry])
    table = _read_table(result)
    import math
    assert math.isnan(table.column("fiber_g")[0].as_py())
