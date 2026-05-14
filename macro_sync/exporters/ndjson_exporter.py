"""Newline-delimited JSON (NDJSON) exporter for NutritionEntry and DailySummary."""

from __future__ import annotations

import json
from datetime import date
from io import BytesIO
from typing import List

from macro_sync.schema import DailySummary, NutritionEntry


def _default_serializer(obj):
    """JSON serializer for types not natively supported."""
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def entries_to_ndjson_str(entries: List[NutritionEntry]) -> str:
    """Serialize a list of NutritionEntry objects to an NDJSON string."""
    lines = [
        json.dumps(entry.to_dict(), default=_default_serializer)
        for entry in entries
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def summaries_to_ndjson_str(summaries: List[DailySummary]) -> str:
    """Serialize a list of DailySummary objects to an NDJSON string."""
    lines = [
        json.dumps(summary.to_dict(), default=_default_serializer)
        for summary in summaries
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def entries_to_ndjson(entries: List[NutritionEntry]) -> BytesIO:
    """Return a BytesIO buffer containing NDJSON-encoded entries."""
    buf = BytesIO()
    buf.write(entries_to_ndjson_str(entries).encode("utf-8"))
    buf.seek(0)
    return buf


def summaries_to_ndjson(summaries: List[DailySummary]) -> BytesIO:
    """Return a BytesIO buffer containing NDJSON-encoded summaries."""
    buf = BytesIO()
    buf.write(summaries_to_ndjson_str(summaries).encode("utf-8"))
    buf.seek(0)
    return buf
