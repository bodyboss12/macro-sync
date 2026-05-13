"""Tests for the JSON exporter module."""

from __future__ import annotations

import io
import json
from datetime import date

import pytest

from macro_sync.exporters.json_exporter import (
    entries_to_json,
    entries_to_json_str,
    summaries_to_json,
    summaries_to_json_str,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein=30.0,
        carbs=60.0,
        fat=15.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein=120.0,
        total_carbs=250.0,
        total_fat=70.0,
        sources=["myfitnesspal", "cronometer"],
        entry_count=4,
    )


def test_entries_to_json_str_is_valid_json(sample_entry):
    result = entries_to_json_str([sample_entry])
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 1


def test_entries_to_json_str_date_serialized(sample_entry):
    result = entries_to_json_str([sample_entry])
    parsed = json.loads(result)
    assert parsed[0]["date"] == "2024-03-15"


def test_entries_to_json_str_fields(sample_entry):
    result = entries_to_json_str([sample_entry])
    parsed = json.loads(result)[0]
    assert parsed["source"] == "myfitnesspal"
    assert parsed["calories"] == 500.0
    assert parsed["protein"] == 30.0
    assert parsed["carbs"] == 60.0
    assert parsed["fat"] == 15.0


def test_entries_to_json_writes_to_stream(sample_entry):
    fp = io.StringIO()
    entries_to_json([sample_entry], fp)
    fp.seek(0)
    parsed = json.loads(fp.read())
    assert len(parsed) == 1
    assert parsed[0]["source"] == "myfitnesspal"


def test_summaries_to_json_str_is_valid_json(sample_summary):
    result = summaries_to_json_str([sample_summary])
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert len(parsed) == 1


def test_summaries_to_json_str_fields(sample_summary):
    result = summaries_to_json_str([sample_summary])
    parsed = json.loads(result)[0]
    assert parsed["date"] == "2024-03-15"
    assert parsed["total_calories"] == 2000.0
    assert parsed["entry_count"] == 4
    assert "myfitnesspal" in parsed["sources"]


def test_summaries_to_json_writes_to_stream(sample_summary):
    fp = io.StringIO()
    summaries_to_json([sample_summary], fp)
    fp.seek(0)
    parsed = json.loads(fp.read())
    assert parsed[0]["total_protein"] == 120.0


def test_empty_entries_to_json_str():
    result = entries_to_json_str([])
    assert json.loads(result) == []
