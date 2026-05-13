"""Tests for the Parquet exporter."""
import datetime
import io
import pytest

pyarrow = pytest.importorskip("pyarrow")
import pyarrow.parquet as pq

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.parquet_exporter import (
    entries_to_parquet_bytes,
    summaries_to_parquet_bytes,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=datetime.date(2024, 3, 10),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=datetime.date(2024, 3, 10),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=250.0,
        total_fat_g=70.0,
        entry_count=4,
    )


def _read_table(data: bytes):
    return pq.read_table(io.BytesIO(data))


def test_entries_to_parquet_bytes_returns_bytes(sample_entry):
    result = entries_to_parquet_bytes([sample_entry])
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_entries_parquet_row_count(sample_entry):
    result = entries_to_parquet_bytes([sample_entry, sample_entry])
    table = _read_table(result)
    assert table.num_rows == 2


def test_entries_parquet_columns(sample_entry):
    result = entries_to_parquet_bytes([sample_entry])
    table = _read_table(result)
    assert "calories" in table.column_names
    assert "protein_g" in table.column_names
    assert "source" in table.column_names


def test_entries_parquet_values(sample_entry):
    result = entries_to_parquet_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("calories")[0].as_py() == pytest.approx(500.0)
    assert table.column("source")[0].as_py() == "myfitnesspal"


def test_entries_parquet_date_as_string(sample_entry):
    result = entries_to_parquet_bytes([sample_entry])
    table = _read_table(result)
    assert table.column("date")[0].as_py() == "2024-03-10"


def test_entries_parquet_empty_list():
    result = entries_to_parquet_bytes([])
    table = _read_table(result)
    assert table.num_rows == 0


def test_summaries_to_parquet_bytes_returns_bytes(sample_summary):
    result = summaries_to_parquet_bytes([sample_summary])
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_summaries_parquet_row_count(sample_summary):
    result = summaries_to_parquet_bytes([sample_summary, sample_summary])
    table = _read_table(result)
    assert table.num_rows == 2


def test_summaries_parquet_values(sample_summary):
    result = summaries_to_parquet_bytes([sample_summary])
    table = _read_table(result)
    assert table.column("total_calories")[0].as_py() == pytest.approx(2000.0)
    assert table.column("entry_count")[0].as_py() == 4
