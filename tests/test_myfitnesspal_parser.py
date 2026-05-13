import io
from datetime import date

import pytest

from macro_sync.parsers.myfitnesspal import parse_csv


MFP_CSV = """Date,Meal,Calories,Carbohydrates (g),Fat (g),Protein (g),Fiber (g),Sugar (g),Sodium (mg)
2024-03-01,Breakfast,450,55,12,30,6,8,320
2024-03-01,Lunch,620,70,18,40,4,10,580
2024-03-02,Dinner,530,60,15,35,5,,410
"""


@pytest.fixture
def sample_stream():
    return io.StringIO(MFP_CSV)


def test_parse_csv_returns_correct_count(sample_stream):
    entries = parse_csv(sample_stream)
    assert len(entries) == 3


def test_parse_csv_source_field(sample_stream):
    entries = parse_csv(sample_stream)
    for entry in entries:
        assert entry.source == "myfitnesspal"


def test_parse_csv_date_parsing(sample_stream):
    entries = parse_csv(sample_stream)
    assert entries[0].date == date(2024, 3, 1)
    assert entries[2].date == date(2024, 3, 2)


def test_parse_csv_macros(sample_stream):
    entries = parse_csv(sample_stream)
    first = entries[0]
    assert first.calories == 450.0
    assert first.protein_g == 30.0
    assert first.carbs_g == 55.0
    assert first.fat_g == 12.0


def test_parse_csv_optional_fields_present(sample_stream):
    entries = parse_csv(sample_stream)
    first = entries[0]
    assert first.fiber_g == 6.0
    assert first.sugar_g == 8.0
    assert first.sodium_mg == 320.0


def test_parse_csv_optional_fields_missing():
    """Empty optional fields should be None, not 0.0."""
    stream = io.StringIO(MFP_CSV)
    entries = parse_csv(stream)
    # Third row has empty Sugar (g)
    third = entries[2]
    assert third.sugar_g is None


def test_parse_csv_multiple_dates(sample_stream):
    entries = parse_csv(sample_stream)
    dates = {e.date for e in entries}
    assert dates == {date(2024, 3, 1), date(2024, 3, 2)}
