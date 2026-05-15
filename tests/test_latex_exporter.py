"""Tests for the LaTeX exporter."""
import datetime
import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.latex_exporter import (
    entries_to_latex,
    entries_to_latex_str,
    summaries_to_latex,
    summaries_to_latex_str,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=datetime.date(2024, 1, 15),
        source="myfitnesspal",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=datetime.date(2024, 1, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=55.0,
        entry_count=3,
    )


def test_entries_latex_str_returns_string(sample_entry):
    result = entries_to_latex_str([sample_entry])
    assert isinstance(result, str)


def test_entries_latex_has_tabular(sample_entry):
    result = entries_to_latex_str([sample_entry])
    assert r"\begin{tabular}" in result
    assert r"\end{tabular}" in result


def test_entries_latex_has_hline(sample_entry):
    result = entries_to_latex_str([sample_entry])
    assert r"\hline" in result


def test_entries_latex_has_header_columns(sample_entry):
    result = entries_to_latex_str([sample_entry])
    assert "date" in result
    assert "calories" in result
    assert "protein" in result


def test_entries_latex_has_data(sample_entry):
    result = entries_to_latex_str([sample_entry])
    assert "2024-01-15" in result
    assert "myfitnesspal" in result
    assert "500.0" in result


def test_entries_latex_row_count(sample_entry):
    entries = [sample_entry, sample_entry]
    result = entries_to_latex_str(entries)
    # Each data row ends with \\
    data_rows = [line for line in result.splitlines() if r"\\" in line and "hline" not in line and "tabular" not in line]
    # header row + 2 data rows
    assert len(data_rows) == 3


def test_entries_to_latex_returns_bytes(sample_entry):
    result = entries_to_latex([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_latex_bytes_decodable(sample_entry):
    result = entries_to_latex([sample_entry])
    decoded = result.decode("utf-8")
    assert r"\begin{tabular}" in decoded


def test_summaries_latex_str_returns_string(sample_summary):
    result = summaries_to_latex_str([sample_summary])
    assert isinstance(result, str)


def test_summaries_latex_has_summary_columns(sample_summary):
    result = summaries_to_latex_str([sample_summary])
    assert "total" in result
    assert "entry" in result


def test_summaries_latex_has_data(sample_summary):
    result = summaries_to_latex_str([sample_summary])
    assert "1800.0" in result
    assert "2024-01-15" in result


def test_summaries_to_latex_returns_bytes(sample_summary):
    result = summaries_to_latex([sample_summary])
    assert isinstance(result, bytes)


def test_latex_escapes_underscore():
    from macro_sync.exporters.latex_exporter import _escape
    assert r"\_" in _escape("hello_world")


def test_empty_entries_latex_str():
    result = entries_to_latex_str([])
    assert r"\begin{tabular}" in result
    assert r"\end{tabular}" in result
