"""Tests for the unified nutrition schema."""

import pytest
from datetime import date
from macro_sync.schema import NutritionEntry, DailySummary


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        name="Chicken Breast",
        calories=165.0,
        protein_g=31.0,
        carbs_g=0.0,
        fat_g=3.6,
        date=date(2024, 1, 15),
        source="myfitnesspal",
        serving_size="100g",
        sodium_mg=74.0,
        meal="lunch",
    )


@pytest.fixture
def sample_entries():
    return [
        NutritionEntry(
            name="Oatmeal",
            calories=150.0,
            protein_g=5.0,
            carbs_g=27.0,
            fat_g=3.0,
            date=date(2024, 1, 15),
            source="cronometer",
            fiber_g=4.0,
            sugar_g=1.0,
            sodium_mg=0.0,
            meal="breakfast",
        ),
        NutritionEntry(
            name="Banana",
            calories=89.0,
            protein_g=1.1,
            carbs_g=23.0,
            fat_g=0.3,
            date=date(2024, 1, 15),
            source="myfitnesspal",
            fiber_g=2.6,
            sugar_g=12.0,
            sodium_mg=1.0,
            meal="breakfast",
        ),
    ]


def test_entry_to_dict(sample_entry):
    result = sample_entry.to_dict()
    assert result["name"] == "Chicken Breast"
    assert result["calories"] == 165.0
    assert result["date"] == "2024-01-15"
    assert result["source"] == "myfitnesspal"
    assert result["meal"] == "lunch"


def test_entry_optional_fields_default_none():
    entry = NutritionEntry(
        name="Plain Rice",
        calories=206.0,
        protein_g=4.3,
        carbs_g=45.0,
        fat_g=0.4,
        date=date(2024, 1, 15),
        source="cronometer",
    )
    assert entry.fiber_g is None
    assert entry.sugar_g is None
    assert entry.sodium_mg is None
    assert entry.meal is None


def test_daily_summary_from_entries(sample_entries):
    summary = DailySummary.from_entries(date(2024, 1, 15), sample_entries)
    assert summary.total_calories == pytest.approx(239.0)
    assert summary.total_protein_g == pytest.approx(6.1)
    assert summary.total_carbs_g == pytest.approx(50.0)
    assert summary.total_fiber_g == pytest.approx(6.6)
    assert summary.total_sugar_g == pytest.approx(13.0)
    assert len(summary.entries) == 2


def test_daily_summary_to_dict(sample_entries):
    summary = DailySummary.from_entries(date(2024, 1, 15), sample_entries)
    result = summary.to_dict()
    assert result["date"] == "2024-01-15"
    assert result["entry_count"] == 2
    assert "total_calories" in result


def test_daily_summary_empty_entries():
    summary = DailySummary.from_entries(date(2024, 1, 15), [])
    assert summary.total_calories == 0.0
    assert summary.total_protein_g == 0.0
    assert len(summary.entries) == 0
