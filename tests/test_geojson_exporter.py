import json
from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.geojson_exporter import (
    entries_to_geojson,
    entries_to_geojson_str,
    summaries_to_geojson,
    summaries_to_geojson_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=55.0,
        fat_g=5.0,
        fiber_g=4.0,
        sugar_g=6.0,
        sodium_mg=120.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=90.0,
        total_carbs_g=220.0,
        total_fat_g=60.0,
        total_fiber_g=25.0,
        total_sugar_g=40.0,
        total_sodium_mg=2000.0,
        entry_count=5,
    )


def test_entries_geojson_str_is_valid_json(sample_entry):
    result = entries_to_geojson_str([sample_entry])
    parsed = json.loads(result)
    assert isinstance(parsed, dict)


def test_entries_geojson_root_type(sample_entry):
    parsed = json.loads(entries_to_geojson_str([sample_entry]))
    assert parsed["type"] == "FeatureCollection"


def test_entries_geojson_feature_count(sample_entry):
    parsed = json.loads(entries_to_geojson_str([sample_entry, sample_entry]))
    assert len(parsed["features"]) == 2


def test_entries_geojson_feature_type(sample_entry):
    parsed = json.loads(entries_to_geojson_str([sample_entry]))
    feature = parsed["features"][0]
    assert feature["type"] == "Feature"
    assert feature["geometry"] is None


def test_entries_geojson_properties_fields(sample_entry):
    parsed = json.loads(entries_to_geojson_str([sample_entry]))
    props = parsed["features"][0]["properties"]
    assert props["date"] == "2024-03-15"
    assert props["source"] == "myfitnesspal"
    assert props["food_name"] == "Oatmeal"
    assert props["calories"] == 300.0
    assert props["protein_g"] == 10.0


def test_entries_geojson_bytes_returns_bytes(sample_entry):
    result = entries_to_geojson([sample_entry])
    assert isinstance(result, bytes)


def test_entries_geojson_bytes_decodable(sample_entry):
    result = entries_to_geojson([sample_entry])
    parsed = json.loads(result.decode("utf-8"))
    assert parsed["type"] == "FeatureCollection"


def test_summaries_geojson_feature_count(sample_summary):
    parsed = json.loads(summaries_to_geojson_str([sample_summary]))
    assert len(parsed["features"]) == 1


def test_summaries_geojson_properties_fields(sample_summary):
    parsed = json.loads(summaries_to_geojson_str([sample_summary]))
    props = parsed["features"][0]["properties"]
    assert props["date"] == "2024-03-15"
    assert props["total_calories"] == 1800.0
    assert props["entry_count"] == 5


def test_summaries_geojson_bytes(sample_summary):
    result = summaries_to_geojson([sample_summary])
    assert isinstance(result, bytes)
    parsed = json.loads(result)
    assert parsed["type"] == "FeatureCollection"


def test_entries_geojson_empty():
    parsed = json.loads(entries_to_geojson_str([]))
    assert parsed["features"] == []
