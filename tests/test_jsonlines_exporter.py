"""Tests for macro_sync.exporters.jsonlines_exporter."""
from __future__ import annotations

import gzip
import json
from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.jsonlines_exporter import (
    entries_to_jsonlines_str,
    entries_to_jsonlines_bytes,
    summaries_to_jsonlines_str,
    summaries_to_jsonlines_bytes,
)


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="mfp",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=55.0,
        fat_g=5.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein_g=150.0,
        total_carbs_g=200.0,
        total_fat_g=70.0,
        entry_count=5,
    )


def test_entries_jsonlines_line_count(sample_entry):
    result = entries_to_jsonlines_str([sample_entry, sample_entry])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_entries_jsonlines_each_line_valid_json(sample_entry):
    result = entries_to_jsonlines_str([sample_entry])
    for line in result.splitlines():
        if line.strip():
            obj = json.loads(line)
            assert isinstance(obj, dict)


def test_entries_jsonlines_date_serialized(sample_entry):
    result = entries_to_jsonlines_str([sample_entry])
    obj = json.loads(result.splitlines()[0])
    assert obj["date"] == "2024-03-15"


def test_entries_jsonlines_fields(sample_entry):
    result = entries_to_jsonlines_str([sample_entry])
    obj = json.loads(result.splitlines()[0])
    assert obj["food_name"] == "Oatmeal"
    assert obj["calories"] == 300.0
    assert obj["source"] == "mfp"


def test_entries_jsonlines_empty():
    result = entries_to_jsonlines_str([])
    assert result == ""


def test_entries_jsonlines_bytes_returns_bytes(sample_entry):
    result = entries_to_jsonlines_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_jsonlines_bytes_utf8(sample_entry):
    result = entries_to_jsonlines_bytes([sample_entry])
    decoded = result.decode("utf-8")
    obj = json.loads(decoded.splitlines()[0])
    assert obj["food_name"] == "Oatmeal"


def test_entries_jsonlines_bytes_compressed(sample_entry):
    result = entries_to_jsonlines_bytes([sample_entry], compress=True)
    decompressed = gzip.decompress(result)
    obj = json.loads(decompressed.decode("utf-8").splitlines()[0])
    assert obj["food_name"] == "Oatmeal"


def test_summaries_jsonlines_line_count(sample_summary):
    result = summaries_to_jsonlines_str([sample_summary, sample_summary])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_summaries_jsonlines_fields(sample_summary):
    result = summaries_to_jsonlines_str([sample_summary])
    obj = json.loads(result.splitlines()[0])
    assert obj["total_calories"] == 2000.0
    assert obj["entry_count"] == 5
    assert obj["date"] == "2024-03-15"


def test_summaries_jsonlines_bytes_compressed(sample_summary):
    result = summaries_to_jsonlines_bytes([sample_summary], compress=True)
    decompressed = gzip.decompress(result)
    obj = json.loads(decompressed.decode("utf-8").splitlines()[0])
    assert obj["total_calories"] == 2000.0
