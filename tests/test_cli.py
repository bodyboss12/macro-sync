"""Tests for the CLI module, including the new ndjson format."""

from __future__ import annotations

import json
from datetime import date
from unittest.mock import patch

import pytest

from macro_sync.cli import build_parser, render_table
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry():
    return NutritionEntry(
        date=date(2024, 3, 10),
        source="mfp",
        food_name="Banana",
        calories=89.0,
        protein=1.1,
        carbs=23.0,
        fat=0.3,
    )


@pytest.fixture
def sample_summary():
    return DailySummary(
        date=date(2024, 3, 10),
        total_calories=2000.0,
        total_protein=150.0,
        total_carbs=220.0,
        total_fat=70.0,
        entry_count=8,
    )


def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.format == "csv"
    assert args.mode == "summaries"
    assert args.output is None


def test_build_parser_ndjson_format():
    parser = build_parser()
    args = parser.parse_args(["--format", "ndjson"])
    assert args.format == "ndjson"


def test_render_table_ndjson_entries(sample_entry):
    result = render_table([sample_entry], [], "ndjson", "entries")
    assert isinstance(result, str)
    data = json.loads(result.splitlines()[0])
    assert data["food_name"] == "Banana"


def test_render_table_ndjson_summaries(sample_summary):
    result = render_table([], [sample_summary], "ndjson", "summaries")
    assert isinstance(result, str)
    data = json.loads(result.splitlines()[0])
    assert data["total_calories"] == 2000.0


def test_render_table_csv_entries(sample_entry):
    result = render_table([sample_entry], [], "csv", "entries")
    assert isinstance(result, str)
    assert "Banana" in result


def test_render_table_json_summaries(sample_summary):
    result = render_table([], [sample_summary], "json", "summaries")
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert isinstance(parsed, list)
    assert parsed[0]["entry_count"] == 8


def test_render_table_excel_returns_bytes(sample_entry):
    result = render_table([sample_entry], [], "excel", "entries")
    assert isinstance(result, bytes)


def test_render_table_msgpack_returns_bytes(sample_entry):
    result = render_table([sample_entry], [], "msgpack", "entries")
    assert isinstance(result, bytes)
