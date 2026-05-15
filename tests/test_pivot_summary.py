"""Tests for pivot_summary helpers."""
from __future__ import annotations

from datetime import date

import pytest

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.pivot_summary import build_pivot, source_totals, DayPivot


def make_entry(d: date, source: str, cal: float, pro: float, carb: float, fat: float):
    return NutritionEntry(
        date=d, source=source,
        calories=cal, protein_g=pro, carbs_g=carb, fat_g=fat,
    )


@pytest.fixture
def mixed_entries():
    return [
        make_entry(date(2024, 3, 1), "MyFitnessPal", 600, 40, 70, 18),
        make_entry(date(2024, 3, 1), "Cronometer", 400, 25, 50, 12),
        make_entry(date(2024, 3, 2), "MyFitnessPal", 700, 45, 80, 22),
        make_entry(date(2024, 3, 2), "Cronometer", 350, 22, 45, 10),
        make_entry(date(2024, 3, 2), "Cronometer", 150, 10, 20, 5),
    ]


def test_build_pivot_returns_sorted_days(mixed_entries):
    pivots = build_pivot(mixed_entries)
    dates = [p.date for p in pivots]
    assert dates == sorted(dates)


def test_build_pivot_totals_calories(mixed_entries):
    pivots = build_pivot(mixed_entries)
    day1 = pivots[0]
    assert day1.total_calories == pytest.approx(1000.0)


def test_build_pivot_entry_count(mixed_entries):
    pivots = build_pivot(mixed_entries)
    assert pivots[0].entry_count == 2
    assert pivots[1].entry_count == 3


def test_build_pivot_by_source_keys(mixed_entries):
    pivots = build_pivot(mixed_entries)
    assert set(pivots[0].by_source.keys()) == {"MyFitnessPal", "Cronometer"}


def test_build_pivot_source_calories(mixed_entries):
    pivots = build_pivot(mixed_entries)
    day2 = pivots[1]
    assert day2.by_source["Cronometer"].calories == pytest.approx(500.0)


def test_build_pivot_protein_aggregated(mixed_entries):
    pivots = build_pivot(mixed_entries)
    day2 = pivots[1]
    assert day2.total_protein_g == pytest.approx(77.0)


def test_build_pivot_empty():
    pivots = build_pivot([])
    assert pivots == []


def test_source_totals_keys(mixed_entries):
    pivots = build_pivot(mixed_entries)
    totals = source_totals(pivots)
    assert set(totals.keys()) == {"MyFitnessPal", "Cronometer"}


def test_source_totals_calories(mixed_entries):
    pivots = build_pivot(mixed_entries)
    totals = source_totals(pivots)
    assert totals["MyFitnessPal"].calories == pytest.approx(1300.0)
    assert totals["Cronometer"].calories == pytest.approx(900.0)


def test_source_totals_empty():
    totals = source_totals([])
    assert totals == {}
