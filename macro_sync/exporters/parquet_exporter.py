"""Parquet exporter for NutritionEntry and DailySummary lists."""
from __future__ import annotations

from typing import List
import io

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "pyarrow is required for the parquet exporter: pip install pyarrow"
    ) from exc

from macro_sync.schema import NutritionEntry, DailySummary


def _entries_to_table(entries: List[NutritionEntry]) -> pa.Table:
    """Convert a list of NutritionEntry objects to a PyArrow Table."""
    rows = [e.to_dict() for e in entries]
    if not rows:
        schema = pa.schema([
            ("date", pa.string()),
            ("source", pa.string()),
            ("calories", pa.float64()),
            ("protein_g", pa.float64()),
            ("carbs_g", pa.float64()),
            ("fat_g", pa.float64()),
            ("fiber_g", pa.float64()),
            ("sugar_g", pa.float64()),
            ("sodium_mg", pa.float64()),
        ])
        return pa.table({f.name: [] for f in schema}, schema=schema)

    # Normalise date to ISO string
    for row in rows:
        if row.get("date") is not None:
            row["date"] = str(row["date"])

    keys = list(rows[0].keys())
    columns = {k: [r.get(k) for r in rows] for k in keys}
    return pa.table(columns)


def _summaries_to_table(summaries: List[DailySummary]) -> pa.Table:
    """Convert a list of DailySummary objects to a PyArrow Table."""
    rows = [s.to_dict() for s in summaries]
    if not rows:
        return pa.table({})
    for row in rows:
        if row.get("date") is not None:
            row["date"] = str(row["date"])
    keys = list(rows[0].keys())
    columns = {k: [r.get(k) for r in rows] for k in keys}
    return pa.table(columns)


def entries_to_parquet_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialise entries to Parquet format and return raw bytes."""
    table = _entries_to_table(entries)
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue()


def summaries_to_parquet_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialise daily summaries to Parquet format and return raw bytes."""
    table = _summaries_to_table(summaries)
    buf = io.BytesIO()
    pq.write_table(table, buf)
    return buf.getvalue()
