"""Tests for the Apache Arrow IPC exporter."""
from __future__ import annotations

import io
from datetime import date

import pyarrow as pa
import pytest

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.arrow_exporter import (
    entries_to_arrow_bytes,
    entries_to_arrow_table,
    summaries_to_arrow_bytes,
    summaries_to_arrow_table,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 5, 1),
        source="cronometer",
        calories=400.0,
        protein_g=25.0,
        carbs_g=50.0,
        fat_g=10.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 5, 1),
        total_calories=2000.0,
        total_protein_g=100.0,
        total_carbs_g=250.0,
        total_fat_g=70.0,
        entry_count=4,
    )


def _read_arrow(data: bytes) -> pa.Table:
    buf = io.BytesIO(data)
    reader = pa.ipc.open_file(buf)
    return reader.read_all()


def test_entries_to_arrow_bytes_returns_bytes(sample_entry):
    result = entries_to_arrow_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_arrow_bytes_nonempty(sample_entry):
    assert len(entries_to_arrow_bytes([sample_entry])) > 0


def test_entries_arrow_row_count(sample_entry):
    table = _read_arrow(entries_to_arrow_bytes([sample_entry, sample_entry]))
    assert table.num_rows == 2


def test_entries_arrow_columns(sample_entry):
    table = _read_arrow(entries_to_arrow_bytes([sample_entry]))
    assert "calories" in table.schema.names
    assert "source" in table.schema.names
    assert "date" in table.schema.names


def test_entries_arrow_calories_value(sample_entry):
    table = _read_arrow(entries_to_arrow_bytes([sample_entry]))
    assert table["calories"][0].as_py() == pytest.approx(400.0, abs=0.1)


def test_entries_arrow_source_value(sample_entry):
    table = _read_arrow(entries_to_arrow_bytes([sample_entry]))
    assert table["source"][0].as_py() == "cronometer"


def test_summaries_to_arrow_bytes_returns_bytes(sample_summary):
    result = summaries_to_arrow_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_arrow_row_count(sample_summary):
    table = _read_arrow(summaries_to_arrow_bytes([sample_summary, sample_summary]))
    assert table.num_rows == 2


def test_summaries_arrow_entry_count(sample_summary):
    table = _read_arrow(summaries_to_arrow_bytes([sample_summary]))
    assert table["entry_count"][0].as_py() == 4


def test_summaries_arrow_total_calories(sample_summary):
    table = _read_arrow(summaries_to_arrow_bytes([sample_summary]))
    assert table["total_calories"][0].as_py() == pytest.approx(2000.0, abs=0.1)
