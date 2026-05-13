"""Tests for macro_sync.exporters.markdown_exporter."""

import datetime
import pytest
from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.markdown_exporter import (
    entries_to_markdown_str,
    summaries_to_markdown_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=datetime.date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=55.0,
        fat_g=5.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=datetime.date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=60.0,
        entry_count=4,
    )


def test_entries_markdown_has_header(sample_entry):
    result = entries_to_markdown_str([sample_entry])
    assert "Date" in result
    assert "Calories" in result
    assert "Protein (g)" in result


def test_entries_markdown_has_separator(sample_entry):
    lines = entries_to_markdown_str([sample_entry]).splitlines()
    assert lines[1].startswith("|")
    assert "---" in lines[1]


def test_entries_markdown_row_count(sample_entry):
    result = entries_to_markdown_str([sample_entry, sample_entry])
    lines = result.splitlines()
    # header + separator + 2 data rows
    assert len(lines) == 4


def test_entries_markdown_data_values(sample_entry):
    result = entries_to_markdown_str([sample_entry])
    assert "2024-03-15" in result
    assert "myfitnesspal" in result
    assert "Oatmeal" in result
    assert "300.0" in result
    assert "10.0" in result


def test_entries_markdown_empty():
    result = entries_to_markdown_str([])
    lines = result.splitlines()
    assert len(lines) == 2  # header + separator only


def test_summaries_markdown_has_header(sample_summary):
    result = summaries_to_markdown_str([sample_summary])
    assert "Date" in result
    assert "Entries" in result
    assert "Calories" in result


def test_summaries_markdown_data_values(sample_summary):
    result = summaries_to_markdown_str([sample_summary])
    assert "2024-03-15" in result
    assert "1800.0" in result
    assert "120.0" in result
    assert "4" in result


def test_summaries_markdown_row_count(sample_summary):
    result = summaries_to_markdown_str([sample_summary, sample_summary])
    lines = result.splitlines()
    assert len(lines) == 4
