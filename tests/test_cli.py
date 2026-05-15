"""Tests for the CLI module."""
from __future__ import annotations

import json
from datetime import date

import pytest

from macro_sync.cli import build_parser, render_table
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 2, 10),
        source="myfitnesspal",
        calories=600.0,
        protein_g=40.0,
        carbs_g=70.0,
        fat_g=20.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 2, 10),
        total_calories=1800.0,
        total_protein_g=100.0,
        total_carbs_g=220.0,
        total_fat_g=60.0,
        entry_count=3,
    )


def test_build_parser_defaults():
    parser = build_parser()
    args = parser.parse_args([])
    assert args.format == "json"
    assert args.summarize is False
    assert args.output is None


def test_build_parser_ndjson_format():
    parser = build_parser()
    args = parser.parse_args(["--format", "ndjson"])
    assert args.format == "ndjson"


def test_build_parser_feather_format():
    parser = build_parser()
    args = parser.parse_args(["--format", "feather"])
    assert args.format == "feather"


def test_render_table_ndjson_entries(sample_entry):
    result = render_table([sample_entry], "ndjson", summarize=False)
    assert isinstance(result, str)
    parsed = json.loads(result.strip())
    assert parsed["source"] == "myfitnesspal"


def test_render_table_feather_entries_returns_bytes(sample_entry):
    result = render_table([sample_entry], "feather", summarize=False)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_table_feather_summaries_returns_bytes(sample_summary):
    result = render_table([sample_summary], "feather", summarize=True)
    assert isinstance(result, bytes)
    assert len(result) > 0


def test_render_table_json_entries(sample_entry):
    result = render_table([sample_entry], "json", summarize=False)
    assert isinstance(result, str)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["calories"] == 600.0


def test_render_table_markdown_entries(sample_entry):
    result = render_table([sample_entry], "markdown", summarize=False)
    assert isinstance(result, str)
    assert "|" in result
