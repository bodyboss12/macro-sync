"""SQLite exporter for NutritionEntry and DailySummary objects."""

import sqlite3
import io
from datetime import date
from typing import List, Union

from macro_sync.schema import NutritionEntry, DailySummary


ENTRIES_TABLE = """
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    source TEXT NOT NULL,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    fiber REAL,
    sugar REAL,
    sodium REAL
)
"""

SUMMARIES_TABLE = """
CREATE TABLE IF NOT EXISTS summaries (
    date TEXT PRIMARY KEY,
    total_calories REAL,
    total_protein REAL,
    total_carbs REAL,
    total_fat REAL,
    total_fiber REAL,
    total_sugar REAL,
    total_sodium REAL,
    entry_count INTEGER
)
"""


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute(ENTRIES_TABLE)
    conn.execute(SUMMARIES_TABLE)
    conn.commit()


def entries_to_connection(entries: List[NutritionEntry], conn: sqlite3.Connection) -> None:
    _init_db(conn)
    rows = [
        (
            e.date.isoformat(),
            e.source,
            e.calories,
            e.protein,
            e.carbs,
            e.fat,
            e.fiber,
            e.sugar,
            e.sodium,
        )
        for e in entries
    ]
    conn.executemany(
        "INSERT INTO entries (date, source, calories, protein, carbs, fat, fiber, sugar, sodium) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()


def summaries_to_connection(summaries: List[DailySummary], conn: sqlite3.Connection) -> None:
    _init_db(conn)
    rows = [
        (
            s.date.isoformat(),
            s.total_calories,
            s.total_protein,
            s.total_carbs,
            s.total_fat,
            s.total_fiber,
            s.total_sugar,
            s.total_sodium,
            s.entry_count,
        )
        for s in summaries
    ]
    conn.executemany(
        "INSERT OR REPLACE INTO summaries "
        "(date, total_calories, total_protein, total_carbs, total_fat, total_fiber, total_sugar, total_sodium, entry_count) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        rows,
    )
    conn.commit()


def entries_to_sqlite_bytes(entries: List[NutritionEntry]) -> bytes:
    conn = sqlite3.connect(":memory:")
    entries_to_connection(entries, conn)
    buf = io.BytesIO()
    for chunk in conn.iterdump():
        buf.write((chunk + "\n").encode("utf-8"))
    conn.close()
    return buf.getvalue()


def summaries_to_sqlite_bytes(summaries: List[DailySummary]) -> bytes:
    conn = sqlite3.connect(":memory:")
    summaries_to_connection(summaries, conn)
    buf = io.BytesIO()
    for chunk in conn.iterdump():
        buf.write((chunk + "\n").encode("utf-8"))
    conn.close()
    return buf.getvalue()
