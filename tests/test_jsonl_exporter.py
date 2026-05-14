"""Tests for the JSONL exporter."""
from __future__ import annotations

import io
import json
from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.jsonl_exporter import (
    entries_to_jsonl,
    entries_to_jsonl_str,
    summaries_to_jsonl,
    summaries_to_jsonl_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=150.0,
        protein_g=5.0,
        carbs_g=27.0,
        fat_g=3.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=60.0,
        entry_count=4,
    )


def test_entries_jsonl_str_line_count(sample_entry):
    result = entries_to_jsonl_str([sample_entry, sample_entry])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_entries_jsonl_str_each_line_valid_json(sample_entry):
    result = entries_to_jsonl_str([sample_entry])
    for line in result.splitlines():
        if line.strip():
            obj = json.loads(line)
            assert isinstance(obj, dict)


def test_entries_jsonl_str_date_serialized(sample_entry):
    result = entries_to_jsonl_str([sample_entry])
    obj = json.loads(result.splitlines()[0])
    assert obj["date"] == "2024-03-15"


def test_entries_jsonl_str_fields(sample_entry):
    result = entries_to_jsonl_str([sample_entry])
    obj = json.loads(result.splitlines()[0])
    assert obj["source"] == "myfitnesspal"
    assert obj["food_name"] == "Oatmeal"
    assert obj["calories"] == 150.0
    assert obj["protein_g"] == 5.0


def test_entries_jsonl_str_empty():
    result = entries_to_jsonl_str([])
    assert result == ""


def test_summaries_jsonl_str_line_count(sample_summary):
    result = summaries_to_jsonl_str([sample_summary, sample_summary])
    lines = [l for l in result.splitlines() if l.strip()]
    assert len(lines) == 2


def test_summaries_jsonl_str_fields(sample_summary):
    result = summaries_to_jsonl_str([sample_summary])
    obj = json.loads(result.splitlines()[0])
    assert obj["total_calories"] == 1800.0
    assert obj["entry_count"] == 4
    assert obj["date"] == "2024-03-15"


def test_entries_to_jsonl_writes_bytes(sample_entry):
    buf = io.BytesIO()
    entries_to_jsonl([sample_entry], buf)
    buf.seek(0)
    content = buf.read().decode("utf-8")
    obj = json.loads(content.splitlines()[0])
    assert obj["food_name"] == "Oatmeal"


def test_summaries_to_jsonl_writes_bytes(sample_summary):
    buf = io.BytesIO()
    summaries_to_jsonl([sample_summary], buf)
    buf.seek(0)
    content = buf.read().decode("utf-8")
    obj = json.loads(content.splitlines()[0])
    assert obj["total_protein_g"] == 120.0
