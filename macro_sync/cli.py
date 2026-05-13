"""CLI entry point for macro-sync."""

import argparse
import sys
from datetime import date
from typing import List

from macro_sync.schema import NutritionEntry, DailySummary
from macro_sync.aggregator import aggregate
from macro_sync import exporters


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="macro-sync",
        description="Aggregate nutrition data from MyFitnessPal and Cronometer.",
    )
    parser.add_argument("--mfp", metavar="FILE", help="MyFitnessPal CSV export file")
    parser.add_argument("--crono", metavar="FILE", help="Cronometer CSV export file")
    parser.add_argument(
        "--format",
        choices=["table", "json", "csv", "markdown", "excel", "sqlite"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--output", metavar="FILE", help="Write output to file instead of stdout"
    )
    parser.add_argument(
        "--entries",
        action="store_true",
        help="Export raw entries instead of daily summaries",
    )
    return parser


def render_table(summaries: List[DailySummary]) -> str:
    header = f"{'Date':<12} {'Calories':>9} {'Protein':>8} {'Carbs':>8} {'Fat':>8} {'Entries':>8}"
    sep = "-" * len(header)
    rows = [
        f"{str(s.date):<12} {s.total_calories:>9.1f} {s.total_protein:>8.1f} "
        f"{s.total_carbs:>8.1f} {s.total_fat:>8.1f} {s.entry_count:>8}"
        for s in summaries
    ]
    return "\n".join([header, sep] + rows)


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    entries: List[NutritionEntry] = []

    if args.mfp:
        from macro_sync.parsers.myfitnesspal import parse_csv as mfp_parse
        with open(args.mfp, newline="", encoding="utf-8") as f:
            entries.extend(mfp_parse(f))

    if args.crono:
        from macro_sync.parsers.cronometer import parse_csv as crono_parse
        with open(args.crono, newline="", encoding="utf-8") as f:
            entries.extend(crono_parse(f))

    if not entries:
        print("No input files provided. Use --mfp and/or --crono.", file=sys.stderr)
        return 1

    summaries = aggregate(entries)
    binary_formats = {"excel", "sqlite"}
    fmt = args.format

    if fmt == "table":
        output = render_table(summaries)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output)
        else:
            print(output)
    elif fmt == "json":
        fn = exporters.entries_to_json_str if args.entries else exporters.summaries_to_json_str
        data = fn(entries if args.entries else summaries)
        _write_text(data, args.output)
    elif fmt == "csv":
        fn = exporters.entries_to_csv_str if args.entries else exporters.summaries_to_csv_str
        data = fn(entries if args.entries else summaries)
        _write_text(data, args.output)
    elif fmt == "markdown":
        fn = exporters.entries_to_markdown_str if args.entries else exporters.summaries_to_markdown_str
        data = fn(entries if args.entries else summaries)
        _write_text(data, args.output)
    elif fmt == "excel":
        fn = exporters.entries_to_excel_bytes if args.entries else exporters.summaries_to_excel_bytes
        data = fn(entries if args.entries else summaries)
        _write_binary(data, args.output)
    elif fmt == "sqlite":
        fn = exporters.entries_to_sqlite_bytes if args.entries else exporters.summaries_to_sqlite_bytes
        data = fn(entries if args.entries else summaries)
        _write_binary(data, args.output)

    return 0


def _write_text(data: str, path) -> None:
    if path:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        print(data)


def _write_binary(data: bytes, path) -> None:
    if path:
        with open(path, "wb") as f:
            f.write(data)
    else:
        sys.stdout.buffer.write(data)


if __name__ == "__main__":
    sys.exit(main())
