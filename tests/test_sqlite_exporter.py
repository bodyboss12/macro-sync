"""Tests for the SQLite exporter."""

import sqlite3
from datetime import date

import pytest

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.exporters.sqlite_exporter import (
    entries_to_connection,
    summaries_to_connection,
    entries_to_sqlite_bytes,
    summaries_to_sqlite_bytes,
)


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 15),
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
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=2000.0,
        total_protein=120.0,
        total_carbs=240.0,
        total_fat=60.0,
        total_fiber=20.0,
        total_sugar=40.0,
        total_sodium=3200.0,
        entry_count=4,
    )


def test_entries_to_connection_creates_table(sample_entry):
    conn = sqlite3.connect(":memory:")
    entries_to_connection([sample_entry], conn)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    assert "entries" in table_names
    conn.close()


def test_entries_to_connection_row_count(sample_entry):
    conn = sqlite3.connect(":memory:")
    entries_to_connection([sample_entry, sample_entry], conn)
    count = conn.execute("SELECT COUNT(*) FROM entries").fetchone()[0]
    assert count == 2
    conn.close()


def test_entries_to_connection_values(sample_entry):
    conn = sqlite3.connect(":memory:")
    entries_to_connection([sample_entry], conn)
    row = conn.execute("SELECT date, source, calories, protein FROM entries").fetchone()
    assert row[0] == "2024-03-15"
    assert row[1] == "myfitnesspal"
    assert row[2] == 500.0
    assert row[3] == 30.0
    conn.close()


def test_summaries_to_connection_creates_table(sample_summary):
    conn = sqlite3.connect(":memory:")
    summaries_to_connection([sample_summary], conn)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    assert "summaries" in table_names
    conn.close()


def test_summaries_to_connection_values(sample_summary):
    conn = sqlite3.connect(":memory:")
    summaries_to_connection([sample_summary], conn)
    row = conn.execute("SELECT date, total_calories, entry_count FROM summaries").fetchone()
    assert row[0] == "2024-03-15"
    assert row[1] == 2000.0
    assert row[2] == 4
    conn.close()


def test_summaries_upsert_on_duplicate(sample_summary):
    conn = sqlite3.connect(":memory:")
    summaries_to_connection([sample_summary], conn)
    updated = DailySummary(
        date=date(2024, 3, 15),
        total_calories=9999.0,
        total_protein=0.0,
        total_carbs=0.0,
        total_fat=0.0,
        total_fiber=0.0,
        total_sugar=0.0,
        total_sodium=0.0,
        entry_count=1,
    )
    summaries_to_connection([updated], conn)
    count = conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0]
    assert count == 1
    cal = conn.execute("SELECT total_calories FROM summaries").fetchone()[0]
    assert cal == 9999.0
    conn.close()


def test_entries_to_sqlite_bytes_returns_bytes(sample_entry):
    result = entries_to_sqlite_bytes([sample_entry])
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_entries_to_sqlite_bytes_contains_insert(sample_entry):
    result = entries_to_sqlite_bytes([sample_entry])
    assert b"INSERT" in result


def test_summaries_to_sqlite_bytes_returns_bytes(sample_summary):
    result = summaries_to_sqlite_bytes([sample_summary])
    assert isinstance(result, bytes)
    assert b"INSERT" in result
