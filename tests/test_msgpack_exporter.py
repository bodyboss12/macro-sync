"""Tests for the MessagePack exporter."""

from __future__ import annotations

import datetime

import msgpack
import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.msgpack_exporter import (
    entries_from_msgpack_bytes,
    entries_to_msgpack_bytes,
    summaries_from_msgpack_bytes,
    summaries_to_msgpack_bytes,
)


@pytest.fixture()
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=datetime.date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein=30.0,
        carbs=60.0,
        fat=15.0,
    )


@pytest.fixture()
def sample_summary() -> DailySummary:
    return DailySummary(
        date=datetime.date(2024, 3, 15),
        total_calories=2000.0,
        total_protein=150.0,
        total_carbs=200.0,
        total_fat=70.0,
        entry_count=4,
    )


def test_entries_to_msgpack_bytes_returns_bytes(sample_entry):
    result = entries_to_msgpack_bytes([sample_entry])
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_entries_to_msgpack_bytes_is_valid_msgpack(sample_entry):
    result = entries_to_msgpack_bytes([sample_entry])
    unpacked = msgpack.unpackb(result, raw=False)
    assert isinstance(unpacked, list)
    assert len(unpacked) == 1


def test_entries_to_msgpack_date_serialized(sample_entry):
    result = entries_to_msgpack_bytes([sample_entry])
    unpacked = msgpack.unpackb(result, raw=False)
    assert unpacked[0]["date"] == "2024-03-15"


def test_entries_to_msgpack_fields(sample_entry):
    result = entries_to_msgpack_bytes([sample_entry])
    unpacked = msgpack.unpackb(result, raw=False)
    row = unpacked[0]
    assert row["calories"] == pytest.approx(500.0)
    assert row["protein"] == pytest.approx(30.0)
    assert row["source"] == "myfitnesspal"


def test_entries_roundtrip(sample_entry):
    raw = entries_to_msgpack_bytes([sample_entry])
    decoded = entries_from_msgpack_bytes(raw)
    assert decoded[0]["carbs"] == pytest.approx(60.0)
    assert decoded[0]["fat"] == pytest.approx(15.0)


def test_summaries_to_msgpack_bytes_returns_bytes(sample_summary):
    result = summaries_to_msgpack_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_to_msgpack_date_serialized(sample_summary):
    result = summaries_to_msgpack_bytes([sample_summary])
    unpacked = msgpack.unpackb(result, raw=False)
    assert unpacked[0]["date"] == "2024-03-15"


def test_summaries_roundtrip(sample_summary):
    raw = summaries_to_msgpack_bytes([sample_summary])
    decoded = summaries_from_msgpack_bytes(raw)
    assert decoded[0]["total_calories"] == pytest.approx(2000.0)
    assert decoded[0]["entry_count"] == 4
