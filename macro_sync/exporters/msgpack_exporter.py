"""MessagePack exporter for NutritionEntry and DailySummary objects."""

from __future__ import annotations

from typing import List

import msgpack

from macro_sync.schema import DailySummary, NutritionEntry


def _prepare_entry(entry: NutritionEntry) -> dict:
    """Convert a NutritionEntry to a msgpack-serialisable dict."""
    d = entry.to_dict()
    # msgpack has no native date type — encode as ISO string
    if d.get("date") is not None:
        d["date"] = d["date"].isoformat()
    return d


def _prepare_summary(summary: DailySummary) -> dict:
    """Convert a DailySummary to a msgpack-serialisable dict."""
    d = summary.to_dict()
    if d.get("date") is not None:
        d["date"] = d["date"].isoformat()
    return d


def entries_to_msgpack_bytes(entries: List[NutritionEntry]) -> bytes:
    """Serialise a list of NutritionEntry objects to MessagePack bytes."""
    payload = [_prepare_entry(e) for e in entries]
    return msgpack.packb(payload, use_bin_type=True)


def summaries_to_msgpack_bytes(summaries: List[DailySummary]) -> bytes:
    """Serialise a list of DailySummary objects to MessagePack bytes."""
    payload = [_prepare_summary(s) for s in summaries]
    return msgpack.packb(payload, use_bin_type=True)


def entries_from_msgpack_bytes(data: bytes) -> List[dict]:
    """Deserialise MessagePack bytes back to a list of plain dicts."""
    return msgpack.unpackb(data, raw=False)


def summaries_from_msgpack_bytes(data: bytes) -> List[dict]:
    """Deserialise MessagePack bytes back to a list of plain dicts."""
    return msgpack.unpackb(data, raw=False)
