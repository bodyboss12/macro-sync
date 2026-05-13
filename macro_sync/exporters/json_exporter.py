"""Export aggregated nutrition data to JSON format."""

from __future__ import annotations

import json
from datetime import date
from typing import IO, List

from macro_sync.schema import DailySummary, NutritionEntry


def _default_serializer(obj):
    """Handle non-serializable types like date."""
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def entries_to_json(entries: List[NutritionEntry], fp: IO[str], indent: int = 2) -> None:
    """Serialize a list of NutritionEntry objects to a JSON stream."""
    data = [e.to_dict() for e in entries]
    json.dump(data, fp, default=_default_serializer, indent=indent)


def summaries_to_json(summaries: List[DailySummary], fp: IO[str], indent: int = 2) -> None:
    """Serialize a list of DailySummary objects to a JSON stream."""
    data = [s.to_dict() for s in summaries]
    json.dump(data, fp, default=_default_serializer, indent=indent)


def entries_to_json_str(entries: List[NutritionEntry], indent: int = 2) -> str:
    """Return a JSON string for a list of NutritionEntry objects."""
    data = [e.to_dict() for e in entries]
    return json.dumps(data, default=_default_serializer, indent=indent)


def summaries_to_json_str(summaries: List[DailySummary], indent: int = 2) -> str:
    """Return a JSON string for a list of DailySummary objects."""
    data = [s.to_dict() for s in summaries]
    return json.dumps(data, default=_default_serializer, indent=indent)
