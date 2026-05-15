"""Tests for the HDF5 exporter."""
from __future__ import annotations

import io
from datetime import date

import h5py
import numpy as np
import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.hdf5_exporter import entries_to_hdf5_bytes, summaries_to_hdf5_bytes


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 1, 15),
        source="myfitnesspal",
        calories=500.0,
        protein=30.0,
        carbs=60.0,
        fat=15.0,
        fiber=5.0,
        sugar=10.0,
        sodium=800.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 1, 15),
        total_calories=2000.0,
        total_protein=120.0,
        total_carbs=240.0,
        total_fat=60.0,
        total_fiber=20.0,
        total_sugar=40.0,
        total_sodium=3200.0,
        entry_count=4,
    )


def _open_bytes(raw: bytes) -> h5py.File:
    return h5py.File(io.BytesIO(raw), "r")


def test_entries_to_hdf5_bytes_returns_bytes(sample_entry):
    result = entries_to_hdf5_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_hdf5_bytes_nonempty(sample_entry):
    result = entries_to_hdf5_bytes([sample_entry])
    assert len(result) > 0


def test_entries_hdf5_has_entries_group(sample_entry):
    raw = entries_to_hdf5_bytes([sample_entry])
    with _open_bytes(raw) as f:
        assert "entries" in f


def test_entries_hdf5_row_count(sample_entry):
    raw = entries_to_hdf5_bytes([sample_entry, sample_entry])
    with _open_bytes(raw) as f:
        assert len(f["entries"]["calories"]) == 2


def test_entries_hdf5_date_serialized(sample_entry):
    raw = entries_to_hdf5_bytes([sample_entry])
    with _open_bytes(raw) as f:
        date_val = f["entries"]["date"][0].decode()
        assert date_val == "2024-01-15"


def test_entries_hdf5_calories(sample_entry):
    raw = entries_to_hdf5_bytes([sample_entry])
    with _open_bytes(raw) as f:
        assert f["entries"]["calories"][0] == pytest.approx(500.0)


def test_summaries_to_hdf5_bytes_returns_bytes(sample_summary):
    result = summaries_to_hdf5_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_hdf5_has_summaries_group(sample_summary):
    raw = summaries_to_hdf5_bytes([sample_summary])
    with _open_bytes(raw) as f:
        assert "summaries" in f


def test_summaries_hdf5_entry_count(sample_summary):
    raw = summaries_to_hdf5_bytes([sample_summary])
    with _open_bytes(raw) as f:
        assert f["summaries"]["entry_count"][0] == 4


def test_summaries_hdf5_total_calories(sample_summary):
    raw = summaries_to_hdf5_bytes([sample_summary])
    with _open_bytes(raw) as f:
        assert f["summaries"]["total_calories"][0] == pytest.approx(2000.0)
