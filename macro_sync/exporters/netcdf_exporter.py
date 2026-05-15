"""NetCDF exporter for NutritionEntry and DailySummary data."""
from __future__ import annotations

import io
from datetime import date
from typing import List

import numpy as np
import netCDF4 as nc

from macro_sync.schema import NutritionEntry, DailySummary


def _date_to_ordinal(d: date) -> int:
    return d.toordinal()


def entries_to_netcdf_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to NetCDF4 bytes."""
    buf = io.BytesIO()
    ds = nc.Dataset("in-memory", mode="w", memory=1024)
    ds.createDimension("record", len(entries))

    date_var = ds.createVariable("date", "i4", ("record",))
    date_var.units = "ordinal days since 0001-01-01"
    calories_var = ds.createVariable("calories", "f4", ("record",))
    protein_var = ds.createVariable("protein_g", "f4", ("record",))
    carbs_var = ds.createVariable("carbs_g", "f4", ("record",))
    fat_var = ds.createVariable("fat_g", "f4", ("record",))
    source_var = ds.createVariable("source", str, ("record",))

    date_var[:] = np.array([_date_to_ordinal(e.date) for e in entries], dtype="i4")
    calories_var[:] = np.array([e.calories or 0.0 for e in entries], dtype="f4")
    protein_var[:] = np.array([e.protein_g or 0.0 for e in entries], dtype="f4")
    carbs_var[:] = np.array([e.carbs_g or 0.0 for e in entries], dtype="f4")
    fat_var[:] = np.array([e.fat_g or 0.0 for e in entries], dtype="f4")
    source_var[:] = np.array([e.source or "" for e in entries])

    data = ds.close()
    return bytes(data)


def summaries_to_netcdf_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to NetCDF4 bytes."""
    ds = nc.Dataset("in-memory", mode="w", memory=1024)
    ds.createDimension("record", len(summaries))

    date_var = ds.createVariable("date", "i4", ("record",))
    date_var.units = "ordinal days since 0001-01-01"
    calories_var = ds.createVariable("total_calories", "f4", ("record",))
    protein_var = ds.createVariable("total_protein_g", "f4", ("record",))
    carbs_var = ds.createVariable("total_carbs_g", "f4", ("record",))
    fat_var = ds.createVariable("total_fat_g", "f4", ("record",))
    count_var = ds.createVariable("entry_count", "i4", ("record",))

    date_var[:] = np.array([_date_to_ordinal(s.date) for s in summaries], dtype="i4")
    calories_var[:] = np.array([s.total_calories or 0.0 for s in summaries], dtype="f4")
    protein_var[:] = np.array([s.total_protein_g or 0.0 for s in summaries], dtype="f4")
    carbs_var[:] = np.array([s.total_carbs_g or 0.0 for s in summaries], dtype="f4")
    fat_var[:] = np.array([s.total_fat_g or 0.0 for s in summaries], dtype="f4")
    count_var[:] = np.array([s.entry_count for s in summaries], dtype="i4")

    data = ds.close()
    return bytes(data)
