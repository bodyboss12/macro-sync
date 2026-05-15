"""Simple protobuf-like binary exporter using struct packing.

Since adding a full protobuf dependency is heavy, this exporter uses
a lightweight custom binary format that is length-prefixed and field-tagged,
making it easy to parse without a schema file.

Format per record:
  [1 byte: field count]
  per field:
    [1 byte: field tag]
    [2 bytes: value length (big-endian uint16)]
    [N bytes: UTF-8 encoded value]
"""

from __future__ import annotations

import struct
from typing import List

from macro_sync.schema import DailySummary, NutritionEntry

# Field tags for NutritionEntry
_ENTRY_TAGS = {
    "date": 1,
    "source": 2,
    "calories": 3,
    "protein_g": 4,
    "carbs_g": 5,
    "fat_g": 6,
    "fiber_g": 7,
    "sugar_g": 8,
    "sodium_mg": 9,
    "notes": 10,
}

# Field tags for DailySummary
_SUMMARY_TAGS = {
    "date": 1,
    "total_calories": 2,
    "total_protein_g": 3,
    "total_carbs_g": 4,
    "total_fat_g": 5,
    "total_fiber_g": 6,
    "total_sugar_g": 7,
    "total_sodium_mg": 8,
    "entry_count": 9,
}


def _encode_record(tags: dict, data: dict) -> bytes:
    fields = []
    for name, tag in tags.items():
        value = data.get(name)
        if value is None:
            continue
        encoded = str(value).encode("utf-8")
        fields.append(struct.pack(">BH", tag, len(encoded)) + encoded)
    header = struct.pack(">B", len(fields))
    return header + b"".join(fields)


def _decode_record(data: bytes, offset: int) -> tuple[dict, int]:
    field_count = struct.unpack_from(">B", data, offset)[0]
    offset += 1
    record: dict = {}
    for _ in range(field_count):
        tag, length = struct.unpack_from(">BH", data, offset)
        offset += 3
        value = data[offset : offset + length].decode("utf-8")
        offset += length
        record[tag] = value
    return record, offset


def entries_to_protobuf_bytes(entries: List[NutritionEntry]) -> bytes:
    """Encode a list of NutritionEntry objects to custom binary format."""
    chunks = [struct.pack(">I", len(entries))]
    for entry in entries:
        d = {
            "date": entry.date.isoformat(),
            "source": entry.source,
            "calories": entry.calories,
            "protein_g": entry.protein_g,
            "carbs_g": entry.carbs_g,
            "fat_g": entry.fat_g,
            "fiber_g": entry.fiber_g,
            "sugar_g": entry.sugar_g,
            "sodium_mg": entry.sodium_mg,
            "notes": entry.notes,
        }
        chunks.append(_encode_record(_ENTRY_TAGS, d))
    return b"".join(chunks)


def summaries_to_protobuf_bytes(summaries: List[DailySummary]) -> bytes:
    """Encode a list of DailySummary objects to custom binary format."""
    chunks = [struct.pack(">I", len(summaries))]
    for s in summaries:
        d = {
            "date": s.date.isoformat(),
            "total_calories": s.total_calories,
            "total_protein_g": s.total_protein_g,
            "total_carbs_g": s.total_carbs_g,
            "total_fat_g": s.total_fat_g,
            "total_fiber_g": s.total_fiber_g,
            "total_sugar_g": s.total_sugar_g,
            "total_sodium_mg": s.total_sodium_mg,
            "entry_count": s.entry_count,
        }
        chunks.append(_encode_record(_SUMMARY_TAGS, d))
    return b"".join(chunks)
