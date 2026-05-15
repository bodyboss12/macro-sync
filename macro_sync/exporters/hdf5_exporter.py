"""HDF5 exporter for NutritionEntry and DailySummary lists."""
from __future__ import annotations

import io
from typing import List

import h5py
import numpy as np

from macro_sync.schema import DailySummary, NutritionEntry

_ENTRY_FIELDS = ["date", "source", "calories", "protein", "carbs", "fat", "fiber", "sugar", "sodium"]
_SUMMARY_FIELDS = ["date", "total_calories", "total_protein", "total_carbs", "total_fat", "total_fiber", "total_sugar", "total_sodium", "entry_count"]


def entries_to_hdf5_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to HDF5 bytes."""
    buf = io.BytesIO()
    with h5py.File(buf, "w") as f:
        grp = f.create_group("entries")
        dates = [e.date.isoformat() for e in entries]
        sources = [e.source for e in entries]
        grp.create_dataset("date", data=np.array(dates, dtype=h5py.special_dtype(vlen=str)))
        grp.create_dataset("source", data=np.array(sources, dtype=h5py.special_dtype(vlen=str)))
        for field in ("calories", "protein", "carbs", "fat", "fiber", "sugar", "sodium"):
            values = [getattr(e, field) or 0.0 for e in entries]
            grp.create_dataset(field, data=np.array(values, dtype=np.float64))
    return buf.getvalue()


def summaries_to_hdf5_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to HDF5 bytes."""
    buf = io.BytesIO()
    with h5py.File(buf, "w") as f:
        grp = f.create_group("summaries")
        dates = [s.date.isoformat() for s in summaries]
        grp.create_dataset("date", data=np.array(dates, dtype=h5py.special_dtype(vlen=str)))
        for field in ("total_calories", "total_protein", "total_carbs", "total_fat", "total_fiber", "total_sugar", "total_sodium"):
            values = [getattr(s, field) or 0.0 for s in summaries]
            grp.create_dataset(field, data=np.array(values, dtype=np.float64))
        grp.create_dataset("entry_count", data=np.array([s.entry_count for s in summaries], dtype=np.int64))
    return buf.getvalue()
