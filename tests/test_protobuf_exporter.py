import struct
from datetime import date

import pytest

from macro_sync.schema import DailySummary, NutritionEntry
from macro_sync.exporters.protobuf_exporter import (
    _decode_record,
    _ENTRY_TAGS,
    _SUMMARY_TAGS,
    entries_to_protobuf_bytes,
    summaries_to_protobuf_bytes,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="mfp",
        calories=500.0,
        protein_g=30.0,
        carbs_g=60.0,
        fat_g=15.0,
        fiber_g=8.0,
        sugar_g=10.0,
        sodium_mg=400.0,
        notes="lunch",
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein_g=120.0,
        total_carbs_g=240.0,
        total_fat_g=60.0,
        total_fiber_g=30.0,
        total_sugar_g=40.0,
        total_sodium_mg=1600.0,
        entry_count=4,
    )


def test_entries_to_protobuf_bytes_returns_bytes(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry])
    assert isinstance(result, bytes)


def test_entries_to_protobuf_bytes_nonempty(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry])
    assert len(result) > 0


def test_entries_record_count_header(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry, sample_entry])
    count = struct.unpack_from(">I", result, 0)[0]
    assert count == 2


def test_entries_empty_list():
    result = entries_to_protobuf_bytes([])
    count = struct.unpack_from(">I", result, 0)[0]
    assert count == 0
    assert len(result) == 4  # just the 4-byte count header


def test_entries_date_field_encoded(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry])
    # skip 4-byte record count, then decode first record
    record, _ = _decode_record(result, 4)
    date_tag = _ENTRY_TAGS["date"]
    assert record[date_tag] == "2024-03-15"


def test_entries_source_field_encoded(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry])
    record, _ = _decode_record(result, 4)
    assert record[_ENTRY_TAGS["source"]] == "mfp"


def test_entries_calories_field_encoded(sample_entry):
    result = entries_to_protobuf_bytes([sample_entry])
    record, _ = _decode_record(result, 4)
    assert float(record[_ENTRY_TAGS["calories"]]) == pytest.approx(500.0)


def test_summaries_to_protobuf_bytes_returns_bytes(sample_summary):
    result = summaries_to_protobuf_bytes([sample_summary])
    assert isinstance(result, bytes)


def test_summaries_record_count_header(sample_summary):
    result = summaries_to_protobuf_bytes([sample_summary])
    count = struct.unpack_from(">I", result, 0)[0]
    assert count == 1


def test_summaries_date_field_encoded(sample_summary):
    result = summaries_to_protobuf_bytes([sample_summary])
    record, _ = _decode_record(result, 4)
    assert record[_SUMMARY_TAGS["date"]] == "2024-03-15"


def test_summaries_entry_count_field(sample_summary):
    result = summaries_to_protobuf_bytes([sample_summary])
    record, _ = _decode_record(result, 4)
    assert int(record[_SUMMARY_TAGS["entry_count"]]) == 4


def test_entries_optional_none_field_omitted():
    entry = NutritionEntry(
        date=date(2024, 1, 1),
        source="cronometer",
        calories=300.0,
        protein_g=20.0,
        carbs_g=40.0,
        fat_g=10.0,
    )
    result = entries_to_protobuf_bytes([entry])
    record, _ = _decode_record(result, 4)
    # notes tag should not be present since notes is None
    assert _ENTRY_TAGS["notes"] not in record
