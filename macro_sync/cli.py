"""Command-line interface for macro-sync."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from macro_sync.aggregator import aggregate
from macro_sync.parsers import cronometer, myfitnesspal
from macro_sync import exporters

FORMATS = [
    "json", "csv", "tsv", "markdown", "html", "xml",
    "yaml", "toml", "excel", "sqlite", "parquet", "msgpack", "pdf",
]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="macro-sync",
        description="Aggregate nutrition data from MyFitnessPal and Cronometer.",
    )
    p.add_argument("--mfp", metavar="FILE", help="MyFitnessPal CSV export")
    p.add_argument("--crono", metavar="FILE", help="Cronometer CSV export")
    p.add_argument(
        "--format", choices=FORMATS, default="json",
        help="Output format (default: json)",
    )
    p.add_argument("--output", metavar="FILE", help="Write output to FILE instead of stdout")
    p.add_argument(
        "--summaries", action="store_true",
        help="Export daily summaries instead of individual entries",
    )
    return p


def render_table(entries, summaries_mode: bool, fmt: str) -> bytes | str:
    if summaries_mode:
        daily = aggregate(entries)
        fn_map = {
            "json": exporters.summaries_to_json_str,
            "csv": exporters.summaries_to_csv_str,
            "tsv": exporters.summaries_to_tsv_str,
            "markdown": exporters.summaries_to_markdown_str,
            "html": exporters.summaries_to_html_str,
            "xml": exporters.summaries_to_xml_str,
            "yaml": exporters.summaries_to_yaml_str,
            "toml": exporters.summaries_to_toml_str,
            "excel": exporters.summaries_to_excel_bytes,
            "sqlite": exporters.summaries_to_sqlite_bytes,
            "parquet": exporters.summaries_to_parquet_bytes,
            "msgpack": exporters.summaries_to_msgpack_bytes,
            "pdf": exporters.summaries_to_pdf_bytes,
        }
        return fn_map[fmt](daily)
    else:
        fn_map = {
            "json": exporters.entries_to_json_str,
            "csv": exporters.entries_to_csv_str,
            "tsv": exporters.entries_to_tsv_str,
            "markdown": exporters.entries_to_markdown_str,
            "html": exporters.entries_to_html_str,
            "xml": exporters.entries_to_xml_str,
            "yaml": exporters.entries_to_yaml_str,
            "toml": exporters.entries_to_toml_str,
            "excel": exporters.entries_to_excel_bytes,
            "sqlite": exporters.entries_to_sqlite_bytes,
            "parquet": exporters.entries_to_parquet_bytes,
            "msgpack": exporters.entries_to_msgpack_bytes,
            "pdf": exporters.entries_to_pdf_bytes,
        }
        return fn_map[fmt](entries)


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


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    entries = []
    if args.mfp:
        with open(args.mfp, newline="", encoding="utf-8") as fh:
            entries.extend(myfitnesspal.parse_csv(fh))
    if args.crono:
        with open(args.crono, newline="", encoding="utf-8") as fh:
            entries.extend(cronometer.parse_csv(fh))

    if not entries:
        parser.error("Provide at least one of --mfp or --crono.")

    result = render_table(entries, args.summaries, args.format)
    binary_formats = {"excel", "sqlite", "parquet", "msgpack", "pdf"}
    if args.format in binary_formats:
        _write_binary(result, args.output)
    else:
        _write_text(result, args.output)


if __name__ == "__main__":
    main()
