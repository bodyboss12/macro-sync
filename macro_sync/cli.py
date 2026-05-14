"""Command-line interface for macro-sync."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from macro_sync.aggregator import aggregate
from macro_sync.exporters import (
    entries_to_csv_str, summaries_to_csv_str,
    entries_to_json_str, summaries_to_json_str,
    entries_to_markdown_str, summaries_to_markdown_str,
    entries_to_ndjson_str, summaries_to_ndjson_str,
    entries_to_tsv_str, summaries_to_tsv_str,
    entries_to_yaml_str, summaries_to_yaml_str,
    entries_to_toml_str, summaries_to_toml_str,
    entries_to_html_str, summaries_to_html_str,
    entries_to_xml_str, summaries_to_xml_str,
    entries_to_excel_bytes, summaries_to_excel_bytes,
    entries_to_parquet_bytes, summaries_to_parquet_bytes,
    entries_to_sqlite_bytes, summaries_to_sqlite_bytes,
    entries_to_pdf_bytes, summaries_to_pdf_bytes,
    entries_to_msgpack_bytes, summaries_to_msgpack_bytes,
)
from macro_sync.parsers import cronometer, myfitnesspal
from macro_sync.schema import DailySummary, NutritionEntry

TEXT_FORMATS = {"csv", "json", "ndjson", "markdown", "tsv", "yaml", "toml", "html", "xml"}
BINARY_FORMATS = {"excel", "parquet", "sqlite", "pdf", "msgpack"}
ALL_FORMATS = TEXT_FORMATS | BINARY_FORMATS


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="macro-sync",
        description="Aggregate nutrition data from MyFitnessPal and Cronometer.",
    )
    p.add_argument("--mfp", metavar="FILE", help="MyFitnessPal CSV export")
    p.add_argument("--crono", metavar="FILE", help="Cronometer CSV export")
    p.add_argument(
        "--format",
        choices=sorted(ALL_FORMATS),
        default="csv",
        help="Output format (default: csv)",
    )
    p.add_argument(
        "--mode",
        choices=["entries", "summaries"],
        default="summaries",
        help="Output entries or daily summaries (default: summaries)",
    )
    p.add_argument("--output", "-o", metavar="FILE", help="Write output to FILE instead of stdout")
    return p


def render_table(entries: List[NutritionEntry], summaries: List[DailySummary], fmt: str, mode: str) -> str | bytes:
    """Dispatch to the correct exporter and return the rendered output."""
    use_entries = mode == "entries"
    dispatch_text = {
        "csv": (entries_to_csv_str, summaries_to_csv_str),
        "json": (entries_to_json_str, summaries_to_json_str),
        "ndjson": (entries_to_ndjson_str, summaries_to_ndjson_str),
        "markdown": (entries_to_markdown_str, summaries_to_markdown_str),
        "tsv": (entries_to_tsv_str, summaries_to_tsv_str),
        "yaml": (entries_to_yaml_str, summaries_to_yaml_str),
        "toml": (entries_to_toml_str, summaries_to_toml_str),
        "html": (entries_to_html_str, summaries_to_html_str),
        "xml": (entries_to_xml_str, summaries_to_xml_str),
    }
    dispatch_binary = {
        "excel": (entries_to_excel_bytes, summaries_to_excel_bytes),
        "parquet": (entries_to_parquet_bytes, summaries_to_parquet_bytes),
        "sqlite": (entries_to_sqlite_bytes, summaries_to_sqlite_bytes),
        "pdf": (entries_to_pdf_bytes, summaries_to_pdf_bytes),
        "msgpack": (entries_to_msgpack_bytes, summaries_to_msgpack_bytes),
    }
    if fmt in dispatch_text:
        fn_entries, fn_summaries = dispatch_text[fmt]
        return fn_entries(entries) if use_entries else fn_summaries(summaries)
    fn_entries, fn_summaries = dispatch_binary[fmt]
    return fn_entries(entries) if use_entries else fn_summaries(summaries)


def _write_text(content: str, output: str | None) -> None:
    if output:
        Path(output).write_text(content, encoding="utf-8")
    else:
        sys.stdout.write(content)


def _write_binary(content: bytes, output: str | None) -> None:
    if output:
        Path(output).write_bytes(content)
    else:
        sys.stdout.buffer.write(content)


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    entries: List[NutritionEntry] = []
    if args.mfp:
        with open(args.mfp, newline="", encoding="utf-8") as fh:
            entries.extend(myfitnesspal.parse_csv(fh))
    if args.crono:
        with open(args.crono, newline="", encoding="utf-8") as fh:
            entries.extend(cronometer.parse_csv(fh))

    summaries = aggregate(entries)
    result = render_table(entries, summaries, args.format, args.mode)

    if isinstance(result, bytes):
        _write_binary(result, args.output)
    else:
        _write_text(result, args.output)


if __name__ == "__main__":  # pragma: no cover
    main()
