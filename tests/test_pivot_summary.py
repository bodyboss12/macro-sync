"""Tests for the pivot_summary module."""
from __future__ import annotations

from datetime import date

import pytest

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.pivot_summary import build_pivot, source_totals, DayPivot, SourceBreakdown


def make_entry(d: date, source: str, calories: float, protein: float = 0.0, carbs: float = 0.0, fat: float = 0.0) -> NutritionEntry:
    return NutritionEntry(date=d, source=source, calories=calories, protein_g=protein, carbs_g=carbs, fat_g=fat)


@pytest.fixture
def mixed_entries():
    return [
        make_entry(date(2024, 1, 1), "mfp", 400.0, protein=20.0, carbs=50.0, fat=10.0),
        make_entry(date(2024, 1, 1), "cronometer", 300.0, protein=15.0, carbs=30.0, fat=8.0),
        make_entry(date(2024, 1, 2), "mfp", 500.0, protein=25.0, carbs=60.0, fat=12.0),
    ]


def test_build_pivot_returns_sorted_days(mixed_entries):
    result = build_pivot(mixed_entries)
    assert len(result) == 2
    assert result[0].date == date(2024, 1, 1)
    assert result[1].date == date(2024, 1, 2)


def test_build_pivot_totals_calories(mixed_entries):
    result = build_pivot(mixed_entries)
    day1 = result[0]
    assert day1.total_calories == pytest.approx(700.0)


def test_build_pivot_entry_count(mixed_entries):
    result = build_pivot(mixed_entries)
    assert result[0].entry_count == 2
    assert result[1].entry_count == 1


def test_build_pivot_by_source_keys(mixed_entries):
    result = build_pivot(mixed_entries)
    day1 = result[0]
    assert "mfp" in day1.by_source
    assert "cronometer" in day1.by_source


def test_build_pivot_by_source_calories(mixed_entries):
    result = build_pivot(mixed_entries)
    day1 = result[0]
    assert day1.by_source["mfp"].total_calories == pytest.approx(400.0)
    assert day1.by_source["cronometer"].total_calories == pytest.approx(300.0)


def test_build_pivot_empty():
    result = build_pivot([])
    assert result == []


def test_source_totals_keys(mixed_entries):
    result = source_totals(mixed_entries)
    assert set(result.keys()) == {"mfp", "cronometer"}


def test_source_totals_calories(mixed_entries):
    result = source_totals(mixed_entries)
    assert result["mfp"].total_calories == pytest.approx(900.0)
    assert result["cronometer"].total_calories == pytest.approx(300.0)


def test_source_totals_entry_count(mixed_entries):
    result = source_totals(mixed_entries)
    assert result["mfp"].entry_count == 2
    assert result["cronometer"].entry_count == 1


def test_source_totals_empty():
    result = source_totals([])
    assert result == {}


def test_source_totals_unknown_source():
    entries = [make_entry(date(2024, 1, 1), None, 200.0)]
    result = source_totals(entries)
    assert "unknown" in result
