"""Tests for the Cronometer CSV parser."""

import io
from datetime import date

import pytest

from macro_sync.parsers.cronometer import parse_csv

SAMPLE_CSV = """Date,Energy (kcal),Protein (g),Carbohydrates (g),Fat (g),Fiber (g),Sugar (g),Sodium (mg)
2024-01-15,2100.5,155.0,230.0,70.0,28.0,45.0,1800.0
2024-01-16,1850.0,140.0,200.0,65.0,22.0,38.0,1600.0
"""

SAMPLE_CSV_MISSING_OPTIONAL = """Date,Energy (kcal),Protein (g),Carbohydrates (g),Fat (g),Fiber (g),Sugar (g),Sodium (mg)
2024-01-17,1950.0,145.0,210.0,68.0,,,
"""


@pytest.fixture
def sample_stream():
    return io.StringIO(SAMPLE_CSV)


def test_parse_csv_returns_correct_count(sample_stream):
    entries = parse_csv(sample_stream)
    assert len(entries) == 2


def test_parse_csv_source_field(sample_stream):
    entries = parse_csv(sample_stream)
    for entry in entries:
        assert entry.source == "cronometer"


def test_parse_csv_date_parsing(sample_stream):
    entries = parse_csv(sample_stream)
    assert entries[0].date == date(2024, 1, 15)
    assert entries[1].date == date(2024, 1, 16)


def test_parse_csv_macros(sample_stream):
    entries = parse_csv(sample_stream)
    first = entries[0]
    assert first.calories == 2100.5
    assert first.protein_g == 155.0
    assert first.carbs_g == 230.0
    assert first.fat_g == 70.0


def test_parse_csv_optional_fields_present(sample_stream):
    entries = parse_csv(sample_stream)
    first = entries[0]
    assert first.fiber_g == 28.0
    assert first.sugar_g == 45.0
    assert first.sodium_mg == 1800.0


def test_parse_csv_optional_fields_missing():
    stream = io.StringIO(SAMPLE_CSV_MISSING_OPTIONAL)
    entries = parse_csv(stream)
    assert len(entries) == 1
    entry = entries[0]
    assert entry.fiber_g is None
    assert entry.sugar_g is None
    assert entry.sodium_mg is None


def test_parse_csv_second_entry_values(sample_stream):
    entries = parse_csv(sample_stream)
    second = entries[1]
    assert second.calories == 1850.0
    assert second.protein_g == 140.0
    assert second.date == date(2024, 1, 16)
