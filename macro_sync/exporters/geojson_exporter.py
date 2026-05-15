"""GeoJSON exporter — wraps nutrition entries/summaries in a GeoJSON
FeatureCollection.  Each record becomes a Feature with null geometry and
all nutrition fields stored in `properties`."""

from __future__ import annotations

import json
from datetime import date
from typing import List

from macro_sync.schema import DailySummary, NutritionEntry


def _default_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _entry_to_feature(entry: NutritionEntry) -> dict:
    return {
        "type": "Feature",
        "geometry": None,
        "properties": {
            "date": entry.date.isoformat(),
            "source": entry.source,
            "food_name": entry.food_name,
            "calories": entry.calories,
            "protein_g": entry.protein_g,
            "carbs_g": entry.carbs_g,
            "fat_g": entry.fat_g,
            "fiber_g": entry.fiber_g,
            "sugar_g": entry.sugar_g,
            "sodium_mg": entry.sodium_mg,
        },
    }


def _summary_to_feature(summary: DailySummary) -> dict:
    return {
        "type": "Feature",
        "geometry": None,
        "properties": {
            "date": summary.date.isoformat(),
            "total_calories": summary.total_calories,
            "total_protein_g": summary.total_protein_g,
            "total_carbs_g": summary.total_carbs_g,
            "total_fat_g": summary.total_fat_g,
            "total_fiber_g": summary.total_fiber_g,
            "total_sugar_g": summary.total_sugar_g,
            "total_sodium_mg": summary.total_sodium_mg,
            "entry_count": summary.entry_count,
        },
    }


def entries_to_geojson_str(entries: List[NutritionEntry], indent: int = 2) -> str:
    collection = {
        "type": "FeatureCollection",
        "features": [_entry_to_feature(e) for e in entries],
    }
    return json.dumps(collection, default=_default_serializer, indent=indent)


def summaries_to_geojson_str(summaries: List[DailySummary], indent: int = 2) -> str:
    collection = {
        "type": "FeatureCollection",
        "features": [_summary_to_feature(s) for s in summaries],
    }
    return json.dumps(collection, default=_default_serializer, indent=indent)


def entries_to_geojson(entries: List[NutritionEntry], indent: int = 2) -> bytes:
    return entries_to_geojson_str(entries, indent=indent).encode("utf-8")


def summaries_to_geojson(summaries: List[DailySummary], indent: int = 2) -> bytes:
    return summaries_to_geojson_str(summaries, indent=indent).encode("utf-8")
