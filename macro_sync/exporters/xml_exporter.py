"""XML exporter for NutritionEntry and DailySummary objects."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from datetime import date
from typing import List

from macro_sync.schema import DailySummary, NutritionEntry


def _set_text(parent: ET.Element, tag: str, value) -> None:
    """Append a child element with a text value, skipping None values."""
    child = ET.SubElement(parent, tag)
    if value is None:
        child.text = ""
    elif isinstance(value, date):
        child.text = value.isoformat()
    else:
        child.text = str(value)


def entries_to_xml(entries: List[NutritionEntry]) -> ET.Element:
    """Build an ElementTree root element from a list of NutritionEntry objects."""
    root = ET.Element("entries")
    for entry in entries:
        elem = ET.SubElement(root, "entry")
        _set_text(elem, "date", entry.date)
        _set_text(elem, "source", entry.source)
        _set_text(elem, "food_name", entry.food_name)
        _set_text(elem, "calories", entry.calories)
        _set_text(elem, "protein_g", entry.protein_g)
        _set_text(elem, "carbs_g", entry.carbs_g)
        _set_text(elem, "fat_g", entry.fat_g)
        _set_text(elem, "fiber_g", entry.fiber_g)
        _set_text(elem, "sugar_g", entry.sugar_g)
        _set_text(elem, "sodium_mg", entry.sodium_mg)
    return root


def summaries_to_xml(summaries: List[DailySummary]) -> ET.Element:
    """Build an ElementTree root element from a list of DailySummary objects."""
    root = ET.Element("summaries")
    for summary in summaries:
        elem = ET.SubElement(root, "summary")
        _set_text(elem, "date", summary.date)
        _set_text(elem, "total_calories", summary.total_calories)
        _set_text(elem, "total_protein_g", summary.total_protein_g)
        _set_text(elem, "total_carbs_g", summary.total_carbs_g)
        _set_text(elem, "total_fat_g", summary.total_fat_g)
        _set_text(elem, "total_fiber_g", summary.total_fiber_g)
        _set_text(elem, "total_sugar_g", summary.total_sugar_g)
        _set_text(elem, "total_sodium_mg", summary.total_sodium_mg)
        _set_text(elem, "entry_count", summary.entry_count)
    return root


def entries_to_xml_str(entries: List[NutritionEntry], indent: int = 2) -> str:
    """Serialize NutritionEntry list to an indented XML string."""
    root = entries_to_xml(entries)
    ET.indent(root, space=" " * indent)
    return ET.tostring(root, encoding="unicode", xml_declaration=False)


def summaries_to_xml_str(summaries: List[DailySummary], indent: int = 2) -> str:
    """Serialize DailySummary list to an indented XML string."""
    root = summaries_to_xml(summaries)
    ET.indent(root, space=" " * indent)
    return ET.tostring(root, encoding="unicode", xml_declaration=False)
