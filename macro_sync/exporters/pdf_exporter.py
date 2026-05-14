"""PDF exporter for NutritionEntry and DailySummary lists.

Uses reportlab to generate simple table-based PDF reports.
"""
from __future__ import annotations

import io
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from macro_sync.schema import NutritionEntry, DailySummary

_ENTRY_HEADERS = ["date", "source", "food", "calories", "protein_g", "carbs_g", "fat_g", "fiber_g"]
_SUMMARY_HEADERS = ["date", "total_calories", "total_protein_g", "total_carbs_g", "total_fat_g", "total_fiber_g", "entry_count"]


def _entry_row(e: NutritionEntry) -> list:
    return [
        str(e.date),
        e.source or "",
        e.food_name or "",
        f"{e.calories:.1f}" if e.calories is not None else "",
        f"{e.protein_g:.1f}" if e.protein_g is not None else "",
        f"{e.carbs_g:.1f}" if e.carbs_g is not None else "",
        f"{e.fat_g:.1f}" if e.fat_g is not None else "",
        f"{e.fiber_g:.1f}" if e.fiber_g is not None else "",
    ]


def _summary_row(s: DailySummary) -> list:
    return [
        str(s.date),
        f"{s.total_calories:.1f}",
        f"{s.total_protein_g:.1f}",
        f"{s.total_carbs_g:.1f}",
        f"{s.total_fat_g:.1f}",
        f"{s.total_fiber_g:.1f}",
        str(s.entry_count),
    ]


def _build_table_style() -> TableStyle:
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#DCE6F1")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ])


def _to_pdf_bytes(title: str, headers: list, rows: list) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=landscape(letter), title=title)
    styles = getSampleStyleSheet()
    elements = [Paragraph(title, styles["Title"]), Table([headers] + rows, style=_build_table_style())]
    doc.build(elements)
    return buf.getvalue()


def entries_to_pdf_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialize a list of NutritionEntry objects to PDF bytes."""
    rows = [_entry_row(e) for e in entries]
    return _to_pdf_bytes("Nutrition Entries", _ENTRY_HEADERS, rows)


def summaries_to_pdf_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialize a list of DailySummary objects to PDF bytes."""
    rows = [_summary_row(s) for s in summaries]
    return _to_pdf_bytes("Daily Summaries", _SUMMARY_HEADERS, rows)
