"""Apache Arrow IPC exporter for NutritionEntry and DailySummary data."""
from __future__ import annotations

import io
from typing import List

import pyarrow as pa

from macro_sync.schema import NutritionEntry, DailySummary


_ENTRY_SCHEMA = pa.schema([
    pa.field("date", pa.date32()),
    pa.field("source", pa.string()),
    pa.field("calories", pa.float32()),
    pa.field("protein_g", pa.float32()),
    pa.field("carbs_g", pa.float32()),
    pa.field("fat_g", pa.float32()),
])

_SUMMARY_SCHEMA = pa.schema([
    pa.field("date", pa.date32()),
    pa.field("total_calories", pa.float32()),
    pa.field("total_protein_g", pa.float32()),
    pa.field("total_carbs_g", pa.float32()),
    pa.field("total_fat_g", pa.float32()),
    pa.field("entry_count", pa.int32()),
])


def entries_to_arrow_table(entries: List[NutritionEntry]) -> pa.Table:
    return pa.table(
        {
            "date": pa.array([e.date for e in entries], type=pa.date32()),
            "source": pa.array([e.source or "" for e in entries]),
            "calories": pa.array([e.calories or 0.0 for e in entries], type=pa.float32()),
            "protein_g": pa.array([e.protein_g or 0.0 for e in entries], type=pa.float32()),
            "carbs_g": pa.array([e.carbs_g or 0.0 for e in entries], type=pa.float32()),
            "fat_g": pa.array([e.fat_g or 0.0 for e in entries], type=pa.float32()),
        },
        schema=_ENTRY_SCHEMA,
    )


def summaries_to_arrow_table(summaries: List[DailySummary]) -> pa.Table:
    return pa.table(
        {
            "date": pa.array([s.date for s in summaries], type=pa.date32()),
            "total_calories": pa.array([s.total_calories or 0.0 for s in summaries], type=pa.float32()),
            "total_protein_g": pa.array([s.total_protein_g or 0.0 for s in summaries], type=pa.float32()),
            "total_carbs_g": pa.array([s.total_carbs_g or 0.0 for s in summaries], type=pa.float32()),
            "total_fat_g": pa.array([s.total_fat_g or 0.0 for s in summaries], type=pa.float32()),
            "entry_count": pa.array([s.entry_count for s in summaries], type=pa.int32()),
        },
        schema=_SUMMARY_SCHEMA,
    )


def entries_to_arrow_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize entries to Arrow IPC (feather v2) bytes."""
    buf = io.BytesIO()
    table = entries_to_arrow_table(entries)
    with pa.ipc.new_file(buf, table.schema) as writer:
        writer.write_table(table)
    return buf.getvalue()


def summaries_to_arrow_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize summaries to Arrow IPC (feather v2) bytes."""
    buf = io.BytesIO()
    table = summaries_to_arrow_table(summaries)
    with pa.ipc.new_file(buf, table.schema) as writer:
        writer.write_table(table)
    return buf.getvalue()
