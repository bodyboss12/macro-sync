"""Tests for the NetCDF exporter."""
from __future__ import annotations

import pytest
from datetime import date

import netCDF4 as nc
import numpy as np

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.netcdf_exporter import (
    entries_to_netcdf_bytes,
    summaries_to_netcdf_bytes,
    _date_to_ordinal,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=60.0,
        entry_count=3,
    )


def _open_bytes(data: bytes):
    return nc.Dataset("in-memory", memory=data, mode="r")


def test_entries_to_netcdf_bytes_returns_bytes(sample_entry):
    result = entries_to_netcdf_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_netcdf_bytes_nonempty(sample_entry):
    result = entries_to_netcdf_bytes([sample_entry])
    assert len(result) > 0


def test_entries_netcdf_row_count(sample_entry):
    entries = [sample_entry, sample_entry]
    result = entries_to_netcdf_bytes(entries)
    ds = _open_bytes(result)
    assert ds.dimensions["record"].size == 2
    ds.close()


def test_entries_netcdf_calories(sample_entry):
    result = entries_to_netcdf_bytes([sample_entry])
    ds = _open_bytes(result)
    assert float(ds.variables["calories"][0]) == pytest.approx(500.0, abs=0.1)
    ds.close()


def test_entries_netcdf_date_is_ordinal(sample_entry):
    result = entries_to_netcdf_bytes([sample_entry])
    ds = _open_bytes(result)
    expected = _date_to_ordinal(date(2024, 3, 15))
    assert int(ds.variables["date"][0]) == expected
    ds.close()


def test_entries_netcdf_source(sample_entry):
    result = entries_to_netcdf_bytes([sample_entry])
    ds = _open_bytes(result)
    assert str(ds.variables["source"][0]) == "myfitnesspal"
    ds.close()


def test_summaries_to_netcdf_bytes_returns_bytes(sample_summary):
    result = summaries_to_netcdf_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_netcdf_row_count(sample_summary):
    result = summaries_to_netcdf_bytes([sample_summary, sample_summary])
    ds = _open_bytes(result)
    assert ds.dimensions["record"].size == 2
    ds.close()


def test_summaries_netcdf_total_calories(sample_summary):
    result = summaries_to_netcdf_bytes([sample_summary])
    ds = _open_bytes(result)
    assert float(ds.variables["total_calories"][0]) == pytest.approx(1800.0, abs=0.1)
    ds.close()


def test_summaries_netcdf_entry_count(sample_summary):
    result = summaries_to_netcdf_bytes([sample_summary])
    ds = _open_bytes(result)
    assert int(ds.variables["entry_count"][0]) == 3
    ds.close()
