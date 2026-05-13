"""Tests for the YAML exporter."""
from __future__ import annotations

import datetime
import io

import pytest
import yaml

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.yaml_exporter import (
    entries_to_yaml,
    entries_to_yaml_str,
    summaries_to_yaml,
    summaries_to_yaml_str,
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
        total_protein=120.0,
        total_carbs=250.0,
        total_fat=65.0,
        entry_count=4,
    )


def test_entries_yaml_str_is_valid_yaml(sample_entry):
    result = entries_to_yaml_str([sample_entry])
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, list)


def test_entries_yaml_str_row_count(sample_entry):
    result = entries_to_yaml_str([sample_entry, sample_entry])
    parsed = yaml.safe_load(result)
    assert len(parsed) == 2


def test_entries_yaml_str_date_serialized(sample_entry):
    result = entries_to_yaml_str([sample_entry])
    parsed = yaml.safe_load(result)
    assert parsed[0]["date"] == "2024-03-15"


def test_entries_yaml_str_fields(sample_entry):
    result = entries_to_yaml_str([sample_entry])
    parsed = yaml.safe_load(result)
    row = parsed[0]
    assert row["source"] == "myfitnesspal"
    assert row["calories"] == pytest.approx(500.0)
    assert row["protein"] == pytest.approx(30.0)
    assert row["carbs"] == pytest.approx(60.0)
    assert row["fat"] == pytest.approx(15.0)


def test_entries_yaml_to_file(sample_entry):
    fp = io.StringIO()
    entries_to_yaml([sample_entry], fp)
    fp.seek(0)
    parsed = yaml.safe_load(fp.read())
    assert len(parsed) == 1


def test_summaries_yaml_str_is_valid_yaml(sample_summary):
    result = summaries_to_yaml_str([sample_summary])
    parsed = yaml.safe_load(result)
    assert isinstance(parsed, list)


def test_summaries_yaml_str_fields(sample_summary):
    result = summaries_to_yaml_str([sample_summary])
    parsed = yaml.safe_load(result)
    row = parsed[0]
    assert row["total_calories"] == pytest.approx(2000.0)
    assert row["entry_count"] == 4
    assert row["date"] == "2024-03-15"


def test_summaries_yaml_to_file(sample_summary):
    fp = io.StringIO()
    summaries_to_yaml([sample_summary], fp)
    fp.seek(0)
    parsed = yaml.safe_load(fp.read())
    assert len(parsed) == 1
