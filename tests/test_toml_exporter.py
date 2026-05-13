"""Tests for the TOML exporter."""

from __future__ import annotations

import io
from datetime import date

import pytest

try:
    import tomllib
except ImportError:  # pragma: no cover
    import tomli as tomllib  # type: ignore

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.toml_exporter import (
    entries_to_toml,
    entries_to_toml_str,
    summaries_to_toml,
    summaries_to_toml_str,
)


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=8.0,
        sugar_g=12.0,
        sodium_mg=900.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=250.0,
        total_fat_g=65.0,
        entry_count=4,
    )


def test_entries_toml_str_is_valid_toml(sample_entry):
    result = entries_to_toml_str([sample_entry])
    parsed = tomllib.loads(result)
    assert "entries" in parsed


def test_entries_toml_str_row_count(sample_entry):
    result = entries_to_toml_str([sample_entry, sample_entry])
    parsed = tomllib.loads(result)
    assert len(parsed["entries"]) == 2


def test_entries_toml_str_date_serialized(sample_entry):
    result = entries_to_toml_str([sample_entry])
    parsed = tomllib.loads(result)
    assert parsed["entries"][0]["date"] == "2024-03-15"


def test_entries_toml_str_fields(sample_entry):
    result = entries_to_toml_str([sample_entry])
    parsed = tomllib.loads(result)
    entry = parsed["entries"][0]
    assert entry["calories"] == 500.0
    assert entry["protein_g"] == 30.0
    assert entry["carbs_g"] == 60.0
    assert entry["fat_g"] == 15.0
    assert entry["fiber_g"] == 8.0
    assert entry["source"] == "myfitnesspal"


def test_entries_toml_optional_fields_omitted():
    entry = NutritionEntry(
        date=date(2024, 3, 15),
        source="cronometer",
        calories=300.0,
        protein_g=20.0,
        carbs_g=40.0,
        fat_g=10.0,
    )
    result = entries_to_toml_str([entry])
    parsed = tomllib.loads(result)
    assert "fiber_g" not in parsed["entries"][0]
    assert "sugar_g" not in parsed["entries"][0]
    assert "sodium_mg" not in parsed["entries"][0]


def test_summaries_toml_str_is_valid_toml(sample_summary):
    result = summaries_to_toml_str([sample_summary])
    parsed = tomllib.loads(result)
    assert "summaries" in parsed


def test_summaries_toml_str_fields(sample_summary):
    result = summaries_to_toml_str([sample_summary])
    parsed = tomllib.loads(result)
    s = parsed["summaries"][0]
    assert s["total_calories"] == 2000.0
    assert s["entry_count"] == 4
    assert s["date"] == "2024-03-15"


def test_entries_to_toml_writes_bytes(sample_entry):
    buf = io.BytesIO()
    entries_to_toml([sample_entry], buf)
    buf.seek(0)
    parsed = tomllib.load(buf)
    assert "entries" in parsed


def test_summaries_to_toml_writes_bytes(sample_summary):
    buf = io.BytesIO()
    summaries_to_toml([sample_summary], buf)
    buf.seek(0)
    parsed = tomllib.load(buf)
    assert "summaries" in parsed
