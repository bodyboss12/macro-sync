"""Tests for macro_sync.exporters.html_exporter."""

import io
from datetime import date

import pytest

from macro_sync.exporters.html_exporter import (
    entries_to_html,
    entries_to_html_str,
    summaries_to_html_str,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 10),
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
        date=date(2024, 3, 10),
        total_calories=2000.0,
        total_protein=120.0,
        total_carbs=240.0,
        total_fat=60.0,
        entry_count=4,
    )


def test_entries_html_is_valid_html(sample_entry):
    html = entries_to_html_str([sample_entry])
    assert html.startswith("<!DOCTYPE html>")
    assert "</html>" in html


def test_entries_html_has_table(sample_entry):
    html = entries_to_html_str([sample_entry])
    assert "<table>" in html
    assert "</table>" in html


def test_entries_html_has_headers(sample_entry):
    html = entries_to_html_str([sample_entry])
    for header in ["date", "source", "calories", "protein", "carbs", "fat"]:
        assert f"<th>{header}</th>" in html


def test_entries_html_contains_data(sample_entry):
    html = entries_to_html_str([sample_entry])
    assert "2024-03-10" in html
    assert "myfitnesspal" in html
    assert "500.0" in html
    assert "30.0" in html


def test_entries_html_row_count(sample_entry):
    entries = [sample_entry, sample_entry]
    html = entries_to_html_str(entries)
    # 2 data rows + 1 header row = 3 <tr> tags
    assert html.count("<tr>") == 3


def test_summaries_html_has_summary_headers(sample_summary):
    html = summaries_to_html_str([sample_summary])
    for header in ["total_calories", "total_protein", "entry_count"]:
        assert f"<th>{header}</th>" in html


def test_summaries_html_contains_data(sample_summary):
    html = summaries_to_html_str([sample_summary])
    assert "2024-03-10" in html
    assert "2000.0" in html
    assert "4" in html


def test_entries_to_html_writes_to_stream(sample_entry):
    stream = io.StringIO()
    entries_to_html([sample_entry], stream)
    content = stream.getvalue()
    assert "<table>" in content
    assert "myfitnesspal" in content


def test_entries_html_optional_fields_empty(sample_entry):
    entry = NutritionEntry(date=date(2024, 3, 10), source="cronometer")
    html = entries_to_html_str([entry])
    assert "cronometer" in html
    assert "<td></td>" in html
