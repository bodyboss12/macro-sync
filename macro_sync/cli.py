"""Command-line interface for macro-sync."""
from __future__ import annotations

import argparse
import sys
from typing import List, Union

from macro_sync.aggregator import aggregate
from macro_sync.exporters import (
    entries_to_arrow_bytes,
    entries_to_csv_str,
    entries_to_excel_bytes,
    entries_to_feather_bytes,
    entries_to_html_str,
    entries_to_json_str,
    entries_to_jsonl_str,
    entries_to_markdown_str,
    entries_to_msgpack_bytes,
    entries_to_ndjson_str,
    entries_to_ods_bytes,
    entries_to_parquet_bytes,
    entries_to_pdf_bytes,
    entries_to_sqlite_bytes,
    entries_to_toml_str,
    entries_to_tsv_str,
    entries_to_xml_str,
    entries_to_yaml_str,
    summaries_to_arrow_bytes,
    summaries_to_csv_str,
    summaries_to_excel_bytes,
    summaries_to_feather_bytes,
    summaries_to_html_str,
    summaries_to_json_str,
    summaries_to_jsonl_str,
    summaries_to_markdown_str,
    summaries_to_msgpack_bytes,
    summaries_to_ndjson_str,
    summaries_to_ods_bytes,
    summaries_to_parquet_bytes,
    summaries_to_pdf_bytes,
    summaries_to_sqlite_bytes,
    summaries_to_toml_str,
    summaries_to_tsv_str,
    summaries_to_xml_str,
    summaries_to_yaml_str,
)
from macro_sync.parsers import cronometer, myfitnesspal
from macro_sync.schema import DailySummary, NutritionEntry

FORMATS_TEXT = {"json", "csv", "tsv", "markdown", "html", "xml", "yaml", "toml", "ndjson", "jsonl"}
FORMATS_BINARY = {"excel", "parquet", "sqlite", "msgpack", "pdf", "ods", "arrow", "feather"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="macro-sync",
        description="Aggregate nutrition data from MyFitnessPal and Cronometer.",
    )
    parser.add_argument("--mfp", metavar="FILE", help="MyFitnessPal CSV export")
    parser.add_argument("--crono", metavar="FILE", help="Cronometer CSV export")
    parser.add_argument(
        "--format",
        default="json",
        choices=sorted(FORMATS_TEXT | FORMATS_BINARY),
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="Output daily summaries instead of raw entries",
    )
    parser.add_argument("--output", "-o", metavar="FILE", help="Write output to FILE")
    return parser


def render_table(
    data: List[Union[NutritionEntry, DailySummary]],
    fmt: str,
    summarize: bool,
) -> Union[str, bytes]:
    is_summary = summarize
    dispatch_text = {
        "json": (entries_to_json_str, summaries_to_json_str),
        "csv": (entries_to_csv_str, summaries_to_csv_str),
        "tsv": (entries_to_tsv_str, summaries_to_tsv_str),
        "markdown": (entries_to_markdown_str, summaries_to_markdown_str),
        "html": (entries_to_html_str, summaries_to_html_str),
        "xml": (entries_to_xml_str, summaries_to_xml_str),
        "yaml": (entries_to_yaml_str, summaries_to_yaml_str),
        "toml": (entries_to_toml_str, summaries_to_toml_str),
        "ndjson": (entries_to_ndjson_str, summaries_to_ndjson_str),
        "jsonl": (entries_to_jsonl_str, summaries_to_jsonl_str),
    }
    dispatch_binary = {
        "excel": (entries_to_excel_bytes, summaries_to_excel_bytes),
        "parquet": (entries_to_parquet_bytes, summaries_to_parquet_bytes),
        "sqlite": (entries_to_sqlite_bytes, summaries_to_sqlite_bytes),
        "msgpack": (entries_to_msgpack_bytes, summaries_to_msgpack_bytes),
        "pdf": (entries_to_pdf_bytes, summaries_to_pdf_bytes),
        "ods": (entries_to_ods_bytes, summaries_to_ods_bytes),
        "arrow": (entries_to_arrow_bytes, summaries_to_arrow_bytes),
        "feather": (entries_to_feather_bytes, summaries_to_feather_bytes),
    }
    if fmt in dispatch_text:
        fn = dispatch_text[fmt][1 if is_summary else 0]
        return fn(data)  # type: ignore[arg-type]
    fn = dispatch_binary[fmt][1 if is_summary else 0]
    return fn(data)  # type: ignore[arg-type]


def _write_text(content: str, output: str | None) -> None:
    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(content)
    else:
        sys.stdout.write(content)


def _write_binary(content: bytes, output: str | None) -> None:
    if output:
        with open(output, "wb") as fh:
            fh.write(content)
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
    data = summaries if args.summarize else entries

    result = render_table(data, args.format, args.summarize)
    if isinstance(result, bytes):
        _write_binary(result, args.output)
    else:
        _write_text(result, args.output)


if __name__ == "__main__":
    main()
