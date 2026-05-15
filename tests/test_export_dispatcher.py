"""Tests for the unified export() dispatcher in macro_sync/exporters/__init__.py."""
from __future__ import annotations

from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters import export


@pytest.fixture
def entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 10),
        source="cronometer",
        calories=600.0,
        protein=40.0,
        carbs=70.0,
        fat=20.0,
    )


@pytest.fixture
def summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 10),
        total_calories=1800.0,
        total_protein=100.0,
        total_carbs=200.0,
        total_fat=55.0,
        entry_count=3,
    )


@pytest.mark.parametrize("fmt", ["json", "csv", "tsv", "markdown", "html", "xml", "yaml", "toml", "ndjson", "jsonl", "latex"])
def test_export_text_formats_return_str(entry, fmt):
    result = export([entry], fmt)
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.parametrize("fmt", ["excel", "parquet", "arrow", "feather", "msgpack", "sqlite", "pdf", "ods", "netcdf", "hdf5"])
def test_export_binary_formats_return_bytes(entry, fmt):
    result = export([entry], fmt)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_export_summary_json(summary):
    result = export([summary], "json")
    assert isinstance(result, str)
    assert "total_calories" in result


def test_export_summary_csv(summary):
    result = export([summary], "csv")
    assert isinstance(result, str)
    assert "total_calories" in result


def test_export_unsupported_format_raises(entry):
    with pytest.raises(ValueError, match="Unsupported export format"):
        export([entry], "avro")


def test_export_hdf5_entries(entry):
    result = export([entry], "hdf5")
    assert isinstance(result, bytes)
    # HDF5 magic bytes: \x89HDF
    assert result[:4] == b"\x89HDF"


def test_export_empty_list_json():
    result = export([], "json")
    assert result == "[]"
