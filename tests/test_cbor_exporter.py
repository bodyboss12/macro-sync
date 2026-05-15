"""Tests for the CBOR exporter."""
from __future__ import annotations

import datetime

import cbor2
import pytest

from macro_sync.exporters.cbor_exporter import (
    entries_from_cbor_bytes,
    entries_to_cbor_bytes,
    summaries_from_cbor_bytes,
    summaries_to_cbor_bytes,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture()
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=datetime.date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=8.0,
        sugar_g=12.0,
        sodium_mg=400.0,
    )


@pytest.fixture()
def sample_summary() -> DailySummary:
    return DailySummary(
        date=datetime.date(2024, 3, 15),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=240.0,
        total_fat_g=60.0,
        total_fiber_g=30.0,
        total_sugar_g=50.0,
        total_sodium_mg=1500.0,
        entry_count=4,
    )


def test_entries_to_cbor_bytes_returns_bytes(sample_entry):
    result = entries_to_cbor_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_cbor_bytes_nonempty(sample_entry):
    result = entries_to_cbor_bytes([sample_entry])
    assert len(result) > 0


def test_entries_to_cbor_bytes_is_valid_cbor(sample_entry):
    result = entries_to_cbor_bytes([sample_entry])
    decoded = cbor2.loads(result)
    assert isinstance(decoded, list)


def test_entries_to_cbor_row_count(sample_entry):
    result = entries_to_cbor_bytes([sample_entry, sample_entry])
    decoded = cbor2.loads(result)
    assert len(decoded) == 2


def test_entries_to_cbor_date_serialized(sample_entry):
    result = entries_to_cbor_bytes([sample_entry])
    decoded = cbor2.loads(result)
    assert decoded[0]["date"] == "2024-03-15"


def test_entries_to_cbor_fields(sample_entry):
    result = entries_to_cbor_bytes([sample_entry])
    decoded = cbor2.loads(result)
    row = decoded[0]
    assert row["calories"] == 500.0
    assert row["protein_g"] == 30.0
    assert row["source"] == "myfitnesspal"


def test_entries_from_cbor_bytes_roundtrip(sample_entry):
    raw = entries_to_cbor_bytes([sample_entry])
    records = entries_from_cbor_bytes(raw)
    assert records[0]["calories"] == sample_entry.calories
    assert records[0]["date"] == sample_entry.date.isoformat()


def test_summaries_to_cbor_bytes_returns_bytes(sample_summary):
    result = summaries_to_cbor_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_to_cbor_fields(sample_summary):
    result = summaries_to_cbor_bytes([sample_summary])
    decoded = cbor2.loads(result)
    row = decoded[0]
    assert row["total_calories"] == 2000.0
    assert row["entry_count"] == 4


def test_summaries_from_cbor_bytes_roundtrip(sample_summary):
    raw = summaries_to_cbor_bytes([sample_summary])
    records = summaries_from_cbor_bytes(raw)
    assert records[0]["total_protein_g"] == sample_summary.total_protein_g
