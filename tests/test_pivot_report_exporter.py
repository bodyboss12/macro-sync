"""Tests for pivot_report_exporter."""
import datetime
import pytest

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.pivot_report_exporter import (
    entries_to_pivot_text,
    entries_to_pivot_markdown,
)


def make_entry(date_str: str, source: str, calories: float, protein: float = 10.0,
               carbs: float = 20.0, fat: float = 5.0) -> NutritionEntry:
    return NutritionEntry(
        date=datetime.date.fromisoformat(date_str),
        source=source,
        calories=calories,
        protein=protein,
        carbs=carbs,
        fat=fat,
    )


@pytest.fixture
def mixed_entries():
    return [
        make_entry("2024-01-01", "myfitnesspal", 500.0, protein=30.0, carbs=60.0, fat=10.0),
        make_entry("2024-01-01", "cronometer", 300.0, protein=20.0, carbs=40.0, fat=5.0),
        make_entry("2024-01-02", "myfitnesspal", 700.0, protein=50.0, carbs=80.0, fat=15.0),
    ]


def test_pivot_text_returns_string(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    assert isinstance(result, str)


def test_pivot_text_contains_dates(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    assert "2024-01-01" in result
    assert "2024-01-02" in result


def test_pivot_text_contains_sources(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    assert "myfitnesspal" in result
    assert "cronometer" in result


def test_pivot_text_contains_totals(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    assert "TOTAL" in result


def test_pivot_text_grand_totals_section(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    assert "Grand totals by source" in result


def test_pivot_text_calorie_values(mixed_entries):
    result = entries_to_pivot_text(mixed_entries)
    # day 1 total calories = 800.0
    assert "800.0" in result


def test_pivot_markdown_returns_string(mixed_entries):
    result = entries_to_pivot_markdown(mixed_entries)
    assert isinstance(result, str)


def test_pivot_markdown_has_header_row(mixed_entries):
    result = entries_to_pivot_markdown(mixed_entries)
    assert "| Date | Source | Calories |" in result


def test_pivot_markdown_has_separator(mixed_entries):
    result = entries_to_pivot_markdown(mixed_entries)
    assert "|------|" in result


def test_pivot_markdown_contains_bold_totals(mixed_entries):
    result = entries_to_pivot_markdown(mixed_entries)
    assert "**TOTAL**" in result


def test_pivot_markdown_row_count(mixed_entries):
    lines = [l for l in entries_to_pivot_markdown(mixed_entries).splitlines() if l.startswith("|")]
    # header + separator + 2 source rows for day1 + 1 total row for day1
    # + 1 source row for day2 + 1 total row for day2 = 8
    assert len(lines) >= 7


def test_pivot_text_empty_entries():
    result = entries_to_pivot_text([])
    assert isinstance(result, str)
    assert "Grand totals by source" in result


def test_pivot_markdown_empty_entries():
    result = entries_to_pivot_markdown([])
    assert isinstance(result, str)
    assert "| Date |" in result
