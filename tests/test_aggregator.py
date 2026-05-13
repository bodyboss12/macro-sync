"""Tests for macro_sync.aggregator."""

from datetime import date

import pytest

from macro_sync.schema import NutritionEntry
from macro_sync.aggregator import merge_entries, group_by_date, aggregate


DATE_A = date(2024, 1, 10)
DATE_B = date(2024, 1, 11)


def make_entry(d: date, calories: float, source: str = "test") -> NutritionEntry:
    return NutritionEntry(
        date=d,
        meal="Lunch",
        food="Apple",
        calories=calories,
        protein=1.0,
        carbs=10.0,
        fat=0.5,
        source=source,
    )


@pytest.fixture
def mfp_entries():
    return [make_entry(DATE_A, 200.0, "myfitnesspal"), make_entry(DATE_B, 300.0, "myfitnesspal")]


@pytest.fixture
def crono_entries():
    return [make_entry(DATE_A, 150.0, "cronometer"), make_entry(DATE_B, 250.0, "cronometer")]


def test_merge_entries_combines_lists(mfp_entries, crono_entries):
    merged = merge_entries([mfp_entries, crono_entries])
    assert len(merged) == 4


def test_merge_entries_empty():
    assert merge_entries([]) == []
    assert merge_entries([[], []]) == []


def test_group_by_date_keys(mfp_entries, crono_entries):
    all_entries = merge_entries([mfp_entries, crono_entries])
    grouped = group_by_date(all_entries)
    assert set(grouped.keys()) == {DATE_A, DATE_B}


def test_group_by_date_counts(mfp_entries, crono_entries):
    all_entries = merge_entries([mfp_entries, crono_entries])
    grouped = group_by_date(all_entries)
    assert len(grouped[DATE_A]) == 2
    assert len(grouped[DATE_B]) == 2


def test_aggregate_returns_one_summary_per_date(mfp_entries, crono_entries):
    summaries = aggregate([mfp_entries, crono_entries])
    assert len(summaries) == 2


def test_aggregate_sorted_by_date(mfp_entries, crono_entries):
    summaries = aggregate([mfp_entries, crono_entries])
    assert summaries[0].date == DATE_A
    assert summaries[1].date == DATE_B


def test_aggregate_calories_summed(mfp_entries, crono_entries):
    summaries = aggregate([mfp_entries, crono_entries])
    # DATE_A: 200 + 150 = 350
    assert summaries[0].total_calories == pytest.approx(350.0)
    # DATE_B: 300 + 250 = 550
    assert summaries[1].total_calories == pytest.approx(550.0)


def test_aggregate_empty_input():
    summaries = aggregate([])
    assert summaries == []
