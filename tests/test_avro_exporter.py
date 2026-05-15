"""Tests for macro_sync.exporters.avro_exporter."""
from __future__ import annotations

import io
from datetime import date

import fastavro
import pytest

from macro_sync.exporters.avro_exporter import (
    entries_to_avro_bytes,
    summaries_to_avro_bytes,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein=30.0,
        carbs=60.0,
        fat=15.0,
        fiber=5.0,
        sugar=10.0,
        sodium=800.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein=120.0,
        total_carbs=240.0,
        total_fat=60.0,
        total_fiber=20.0,
        total_sugar=40.0,
        total_sodium=3200.0,
        entry_count=4,
    )


def _read_avro(data: bytes) -> list:
    return list(fastavro.reader(io.BytesIO(data)))


def test_entries_to_avro_bytes_returns_bytes(sample_entry):
    result = entries_to_avro_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_avro_bytes_nonempty(sample_entry):
    result = entries_to_avro_bytes([sample_entry])
    assert len(result) > 0


def test_entries_avro_row_count(sample_entry):
    result = entries_to_avro_bytes([sample_entry, sample_entry])
    records = _read_avro(result)
    assert len(records) == 2


def test_entries_avro_date_serialized(sample_entry):
    result = entries_to_avro_bytes([sample_entry])
    records = _read_avro(result)
    assert records[0]["date"] == "2024-03-15"


def test_entries_avro_macros(sample_entry):
    result = entries_to_avro_bytes([sample_entry])
    records = _read_avro(result)
    r = records[0]
    assert r["calories"] == pytest.approx(500.0)
    assert r["protein"] == pytest.approx(30.0)
    assert r["carbs"] == pytest.approx(60.0)
    assert r["fat"] == pytest.approx(15.0)


def test_entries_avro_optional_fields(sample_entry):
    result = entries_to_avro_bytes([sample_entry])
    records = _read_avro(result)
    r = records[0]
    assert r["fiber"] == pytest.approx(5.0)
    assert r["sugar"] == pytest.approx(10.0)
    assert r["sodium"] == pytest.approx(800.0)


def test_entries_avro_optional_fields_none():
    entry = NutritionEntry(
        date=date(2024, 3, 15),
        source="cronometer",
        calories=300.0,
        protein=20.0,
        carbs=40.0,
        fat=10.0,
    )
    result = entries_to_avro_bytes([entry])
    records = _read_avro(result)
    assert records[0]["fiber"] is None


def test_summaries_to_avro_bytes_returns_bytes(sample_summary):
    result = summaries_to_avro_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_avro_row_count(sample_summary):
    result = summaries_to_avro_bytes([sample_summary, sample_summary])
    records = _read_avro(result)
    assert len(records) == 2


def test_summaries_avro_fields(sample_summary):
    result = summaries_to_avro_bytes([sample_summary])
    records = _read_avro(result)
    r = records[0]
    assert r["date"] == "2024-03-15"
    assert r["total_calories"] == pytest.approx(2000.0)
    assert r["entry_count"] == 4
