"""Command-line entry points for reproducible Collatz experiments."""

from __future__ import annotations

import argparse

from collatz_core import (
    compare_mersenne_cohort,
    feature_row,
    l_harbor_rows,
    write_rows,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    single = subparsers.add_parser("single", help="measure one starting value")
    single.add_argument("number", type=int)
    single.add_argument("--base", type=int, default=4)
    single.add_argument("--max-steps", type=int, default=100_000)

    cohort = subparsers.add_parser(
        "cohort", help="measure every value with a given bit length"
    )
    cohort.add_argument("bit_length", type=int)
    cohort.add_argument("output", help="output .csv or .json path")
    cohort.add_argument("--max-steps", type=int, default=100_000)

    family = subparsers.add_parser("l-family", help="export exact L-family records")
    family.add_argument("max_k", type=int)
    family.add_argument("output", help="output .csv or .json path")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "single":
        import json

        print(json.dumps(
            feature_row(args.number, base=args.base, max_steps=args.max_steps),
            indent=2,
        ))
    elif args.command == "cohort":
        write_rows(
            compare_mersenne_cohort(args.bit_length, max_steps=args.max_steps),
            args.output,
        )
    else:
        write_rows(l_harbor_rows(args.max_k), args.output)


if __name__ == "__main__":
    main()
