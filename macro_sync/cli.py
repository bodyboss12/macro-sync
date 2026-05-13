"""Simple CLI entry point for macro-sync."""

import argparse
import json
import sys
from typing import List

from macro_sync.parsers import cronometer, myfitnesspal
from macro_sync.aggregator import aggregate
from macro_sync.schema import DailySummary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="macro-sync",
        description="Aggregate nutrition data from MyFitnessPal and Cronometer CSV exports.",
    )
    parser.add_argument("--mfp", metavar="FILE", help="Path to MyFitnessPal CSV export")
    parser.add_argument("--cronometer", metavar="FILE", help="Path to Cronometer CSV export")
    parser.add_argument(
        "--output",
        choices=["json", "table"],
        default="json",
        help="Output format (default: json)",
    )
    return parser


def render_table(summaries: List[DailySummary]) -> None:
    header = f"{'Date':<12} {'Calories':>10} {'Protein':>10} {'Carbs':>10} {'Fat':>10}"
    print(header)
    print("-" * len(header))
    for s in summaries:
        print(
            f"{str(s.date):<12} {s.total_calories:>10.1f} "
            f"{s.total_protein:>10.1f} {s.total_carbs:>10.1f} {s.total_fat:>10.1f}"
        )


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.mfp and not args.cronometer:
        parser.print_help()
        return 1

    entry_lists = []

    if args.mfp:
        with open(args.mfp, newline="", encoding="utf-8") as fh:
            entry_lists.append(myfitnesspal.parse_csv(fh))

    if args.cronometer:
        with open(args.cronometer, newline="", encoding="utf-8") as fh:
            entry_lists.append(cronometer.parse_csv(fh))

    summaries = aggregate(entry_lists)

    if args.output == "json":
        print(json.dumps([s.to_dict() for s in summaries], indent=2, default=str))
    else:
        render_table(summaries)

    return 0


if __name__ == "__main__":
    sys.exit(main())
