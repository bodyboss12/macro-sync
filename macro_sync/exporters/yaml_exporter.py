"""YAML exporter for NutritionEntry and DailySummary objects."""
from __future__ import annotations

from typing import IO, List

import yaml

from macro_sync.schema import DailySummary, NutritionEntry


def _prepare_entry(entry: NutritionEntry) -> dict:
    d = entry.to_dict()
    # yaml can handle date objects natively, but stringify for consistency
    d["date"] = str(d["date"])
    return d


def _prepare_summary(summary: DailySummary) -> dict:
    d = summary.to_dict()
    d["date"] = str(d["date"])
    return d


def entries_to_yaml_str(entries: List[NutritionEntry]) -> str:
    """Serialise a list of NutritionEntry objects to a YAML string."""
    payload = [_prepare_entry(e) for e in entries]
    return yaml.dump(payload, sort_keys=False, allow_unicode=True)


def summaries_to_yaml_str(summaries: List[DailySummary]) -> str:
    """Serialise a list of DailySummary objects to a YAML string."""
    payload = [_prepare_summary(s) for s in summaries]
    return yaml.dump(payload, sort_keys=False, allow_unicode=True)


def entries_to_yaml(entries: List[NutritionEntry], fp: IO[str]) -> None:
    """Write entries as YAML to a file-like object."""
    fp.write(entries_to_yaml_str(entries))


def summaries_to_yaml(summaries: List[DailySummary], fp: IO[str]) -> None:
    """Write summaries as YAML to a file-like object."""
    fp.write(summaries_to_yaml_str(summaries))
