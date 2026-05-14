"""Tests for the ODS exporter."""

from __future__ import annotations

import io
import datetime
import pytest

pyexcel_ods3 = pytest.importorskip("pyexcel_ods3")

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.ods_exporter import (
    entries_to_ods_bytes,
    summaries_to_ods_bytes,
)


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=datetime.date(2024, 3, 10),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=5.0,
        sugar_g=10.0,
        sodium_mg=800.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=datetime.date(2024, 3, 10),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=240.0,
        total_fat_g=60.0,
        entry_count=4,
    )


def _read_sheet(data: bytes, sheet_name: str) -> list:
    buf = io.BytesIO(data)
    workbook = pyexcel_ods3.get_data(buf)
    return workbook[sheet_name]


def test_entries_to_ods_bytes_returns_bytes(sample_entry):
    result = entries_to_ods_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_ods_bytes_nonempty(sample_entry):
    result = entries_to_ods_bytes([sample_entry])
    assert len(result) > 0


def test_entries_ods_sheet_name(sample_entry):
    data = entries_to_ods_bytes([sample_entry])
    buf = io.BytesIO(data)
    workbook = pyexcel_ods3.get_data(buf)
    assert "Entries" in workbook


def test_entries_ods_header_row(sample_entry):
    data = entries_to_ods_bytes([sample_entry])
    sheet = _read_sheet(data, "Entries")
    assert sheet[0][0] == "date"
    assert sheet[0][1] == "source"
    assert sheet[0][2] == "calories"


def test_entries_ods_row_count(sample_entry):
    data = entries_to_ods_bytes([sample_entry, sample_entry])
    sheet = _read_sheet(data, "Entries")
    # 1 header + 2 data rows
    assert len(sheet) == 3


def test_entries_ods_date_serialized(sample_entry):
    data = entries_to_ods_bytes([sample_entry])
    sheet = _read_sheet(data, "Entries")
    assert sheet[1][0] == "2024-03-10"


def test_summaries_to_ods_bytes_returns_bytes(sample_summary):
    result = summaries_to_ods_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_ods_sheet_name(sample_summary):
    data = summaries_to_ods_bytes([sample_summary])
    buf = io.BytesIO(data)
    workbook = pyexcel_ods3.get_data(buf)
    assert "Summaries" in workbook


def test_summaries_ods_row_count(sample_summary):
    data = summaries_to_ods_bytes([sample_summary, sample_summary])
    sheet = _read_sheet(data, "Summaries")
    assert len(sheet) == 3


def test_summaries_ods_entry_count_field(sample_summary):
    data = summaries_to_ods_bytes([sample_summary])
    sheet = _read_sheet(data, "Summaries")
    headers = sheet[0]
    idx = headers.index("entry_count")
    assert sheet[1][idx] == 4
