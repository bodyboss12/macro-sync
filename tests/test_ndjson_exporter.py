"""Tests for the NDJSON exporter."""

from __future__ import annotations

import json
from datetime import date

import pytest

from macro_sync.exporters.ndjson_exporter import (
    entries_to_ndjson,
    entries_to_ndjson_str,
    summaries_to_ndjson,
    summaries_to_ndjson_str,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 1, 15),
        source="mfp",
        food_name="Oatmeal",
        calories=150.0,
        protein=5.0,
        carbs=27.0,
        fat=3.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 1, 15),
        total_calories=1800.0,
        total_protein=120.0,
        total_carbs=200.0,
        total_fat=60.0,
        entry_count=5,
    )


def test_entries_ndjson_str_line_count(sample_entry):
    result = entries_to_ndjson_str([sample_entry, sample_entry])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_entries_ndjson_str_each_line_valid_json(sample_entry):
    result = entries_to_ndjson_str([sample_entry])
    for line in result.splitlines():
        if line.strip():
            parsed = json.loads(line)
            assert isinstance(parsed, dict)


def test_entries_ndjson_str_date_serialized(sample_entry):
    result = entries_to_ndjson_str([sample_entry])
    data = json.loads(result.splitlines()[0])
    assert data["date"] == "2024-01-15"


def test_entries_ndjson_str_fields(sample_entry):
    result = entries_to_ndjson_str([sample_entry])
    data = json.loads(result.splitlines()[0])
    assert data["food_name"] == "Oatmeal"
    assert data["calories"] == 150.0
    assert data["source"] == "mfp"


def test_entries_ndjson_str_empty():
    result = entries_to_ndjson_str([])
    assert result == ""


def test_summaries_ndjson_str_line_count(sample_summary):
    result = summaries_to_ndjson_str([sample_summary, sample_summary])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_summaries_ndjson_str_fields(sample_summary):
    result = summaries_to_ndjson_str([sample_summary])
    data = json.loads(result.splitlines()[0])
    assert data["total_calories"] == 1800.0
    assert data["entry_count"] == 5


def test_entries_to_ndjson_returns_bytesio(sample_entry):
    buf = entries_to_ndjson([sample_entry])
    content = buf.read().decode("utf-8")
    assert json.loads(content.splitlines()[0])["food_name"] == "Oatmeal"


def test_summaries_to_ndjson_returns_bytesio(sample_summary):
    buf = summaries_to_ndjson([sample_summary])
    content = buf.read().decode("utf-8")
    assert json.loads(content.splitlines()[0])["total_calories"] == 1800.0
