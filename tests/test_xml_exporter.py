"""Tests for the XML exporter."""

import xml.etree.ElementTree as ET
from datetime import date

import pytest

from macro_sync.exporters.xml_exporter import (
    entries_to_xml,
    entries_to_xml_str,
    summaries_to_xml,
    summaries_to_xml_str,
)
from macro_sync.schema import DailySummary, NutritionEntry


@pytest.fixture
def sample_entry() -> NutritionEntry:
    return NutritionEntry(
        date=date(2024, 3, 15),
        source="myfitnesspal",
        food_name="Oatmeal",
        calories=300.0,
        protein_g=10.0,
        carbs_g=55.0,
        fat_g=5.0,
        fiber_g=4.0,
        sugar_g=None,
        sodium_mg=120.0,
    )


@pytest.fixture
def sample_summary() -> DailySummary:
    return DailySummary(
        date=date(2024, 3, 15),
        total_calories=1800.0,
        total_protein_g=90.0,
        total_carbs_g=220.0,
        total_fat_g=60.0,
        total_fiber_g=25.0,
        total_sugar_g=None,
        total_sodium_mg=2000.0,
        entry_count=5,
    )


def test_entries_xml_root_tag(sample_entry):
    root = entries_to_xml([sample_entry])
    assert root.tag == "entries"


def test_entries_xml_child_count(sample_entry):
    root = entries_to_xml([sample_entry, sample_entry])
    assert len(root) == 2


def test_entries_xml_date_format(sample_entry):
    root = entries_to_xml([sample_entry])
    date_text = root.find("entry/date").text
    assert date_text == "2024-03-15"


def test_entries_xml_none_field_is_empty_string(sample_entry):
    root = entries_to_xml([sample_entry])
    sugar_text = root.find("entry/sugar_g").text
    assert sugar_text == ""


def test_entries_xml_str_is_parseable(sample_entry):
    xml_str = entries_to_xml_str([sample_entry])
    parsed = ET.fromstring(xml_str)
    assert parsed.tag == "entries"


def test_entries_xml_str_contains_food_name(sample_entry):
    xml_str = entries_to_xml_str([sample_entry])
    assert "Oatmeal" in xml_str


def test_summaries_xml_root_tag(sample_summary):
    root = summaries_to_xml([sample_summary])
    assert root.tag == "summaries"


def test_summaries_xml_entry_count_field(sample_summary):
    root = summaries_to_xml([sample_summary])
    count_text = root.find("summary/entry_count").text
    assert count_text == "5"


def test_summaries_xml_str_is_parseable(sample_summary):
    xml_str = summaries_to_xml_str([sample_summary])
    parsed = ET.fromstring(xml_str)
    assert parsed.tag == "summaries"


def test_summaries_xml_none_field_is_empty_string(sample_summary):
    root = summaries_to_xml([sample_summary])
    sugar_text = root.find("summary/total_sugar_g").text
    assert sugar_text == ""
