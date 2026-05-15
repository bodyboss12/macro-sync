"""Tests for xlsx_pivot_chart_exporter."""
from __future__ import annotations

import io
from datetime import date

import pytest

openpyxl = pytest.importorskip("openpyxl")

from macro_sync.schema import NutritionEntry
from macro_sync.exporters.xlsx_pivot_chart_exporter import (
    entries_to_pivot_chart_bytes,
    entries_to_pivot_chart_workbook,
)


@pytest.fixture
def sample_entries():
    return [
        NutritionEntry(
            date=date(2024, 1, 10),
            source="MyFitnessPal",
            calories=500.0,
            protein_g=30.0,
            carbs_g=60.0,
            fat_g=15.0,
        ),
        NutritionEntry(
            date=date(2024, 1, 10),
            source="Cronometer",
            calories=300.0,
            protein_g=20.0,
            carbs_g=40.0,
            fat_g=8.0,
        ),
        NutritionEntry(
            date=date(2024, 1, 11),
            source="MyFitnessPal",
            calories=700.0,
            protein_g=50.0,
            carbs_g=80.0,
            fat_g=20.0,
        ),
    ]


def test_returns_bytes(sample_entries):
    result = entries_to_pivot_chart_bytes(sample_entries)
    assert isinstance(result, bytes)


def test_bytes_nonempty(sample_entries):
    result = entries_to_pivot_chart_bytes(sample_entries)
    assert len(result) > 0


def test_bytes_xlsx_magic(sample_entries):
    result = entries_to_pivot_chart_bytes(sample_entries)
    # xlsx files are ZIP archives starting with PK
    assert result[:2] == b"PK"


def test_workbook_has_two_sheets(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    assert len(wb.sheetnames) == 2
    assert "Daily Pivot" in wb.sheetnames
    assert "Source Totals" in wb.sheetnames


def test_pivot_sheet_header(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Daily Pivot"]
    headers = [cell.value for cell in ws[1]]
    assert headers == ["date", "entries", "calories", "protein_g", "carbs_g", "fat_g"]


def test_pivot_sheet_row_count(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Daily Pivot"]
    # 1 header + 2 days
    assert ws.max_row == 3


def test_pivot_sheet_calories_aggregated(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Daily Pivot"]
    # Row 2 = 2024-01-10, calories = 500 + 300 = 800
    row2 = [cell.value for cell in ws[2]]
    assert row2[2] == pytest.approx(800.0)


def test_pivot_sheet_rows_sorted_by_date(sample_entries):
    """Dates in the Daily Pivot sheet should be in ascending order."""
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Daily Pivot"]
    # Skip header row; collect date values from column 1
    date_values = [ws.cell(row=r, column=1).value for r in range(2, ws.max_row + 1)]
    assert date_values == sorted(date_values)


def test_source_totals_sheet_header(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Source Totals"]
    headers = [cell.value for cell in ws[1]]
    assert headers == ["source", "calories", "protein_g", "carbs_g", "fat_g"]


def test_source_totals_row_count(sample_entries):
    wb = entries_to_pivot_chart_workbook(sample_entries)
    ws = wb["Source Totals"]
    # 1 header + 2 sources
    assert ws.max_row == 3


def test_empty_entries_does_not_raise():
    result = entries_to_pivot_chart_bytes([])
