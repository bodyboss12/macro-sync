"""Tests for the PDF exporter."""
import datetime
import pytest

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.pdf_exporter import entries_to_pdf_bytes, summaries_to_pdf_bytes


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=datetime.date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=54.0,
        fat_g=5.0,
        fiber_g=4.0,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=datetime.date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=120.0,
        total_carbs_g=200.0,
        total_fat_g=60.0,
        total_fiber_g=25.0,
        entry_count=5,
    )


def test_entries_to_pdf_bytes_returns_bytes(sample_entry):
    result = entries_to_pdf_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_pdf_bytes_nonempty(sample_entry):
    result = entries_to_pdf_bytes([sample_entry])
    assert len(result) > 0


def test_entries_to_pdf_bytes_pdf_magic(sample_entry):
    """PDF files start with the %PDF magic bytes."""
    result = entries_to_pdf_bytes([sample_entry])
    assert result[:4] == b"%PDF"


def test_entries_to_pdf_bytes_empty_list():
    result = entries_to_pdf_bytes([])
    assert isinstance(result, bytes)
    assert result[:4] == b"%PDF"


def test_summaries_to_pdf_bytes_returns_bytes(sample_summary):
    result = summaries_to_pdf_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_to_pdf_bytes_pdf_magic(sample_summary):
    result = summaries_to_pdf_bytes([sample_summary])
    assert result[:4] == b"%PDF"


def test_summaries_to_pdf_bytes_nonempty(sample_summary):
    result = summaries_to_pdf_bytes([sample_summary])
    assert len(result) > 0


def test_entries_multiple_rows():
    entries = [
        NutritionEntry(
            date=datetime.date(2024, 3, i),
            source="cronometer",
            food_name=f"Food {i}",
            calories=float(100 * i),
            protein_g=float(10 * i),
            carbs_g=float(20 * i),
            fat_g=float(5 * i),
            fiber_g=float(2 * i),
        )
        for i in range(1, 6)
    ]
    result = entries_to_pdf_bytes(entries)
    assert isinstance(result, bytes)
    assert result[:4] == b"%PDF"
