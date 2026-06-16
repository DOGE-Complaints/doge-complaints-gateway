#!/usr/bin/env python3
"""Classify miss candidates into taxonomy-decisions.yaml draft (taxonomy TC2)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.taxonomy.cycle_lib import (  # noqa: E402
    DEFAULT_MIN_MISS_COUNT,
    aggregate_miss_rows,
    classify_all,
    load_canonical_snapshot,
    write_decisions_yaml,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Classify taxonomy miss candidates (TC2).")
    parser.add_argument("--in", dest="input_path", required=True, type=Path, help="misses-ranked.json")
    parser.add_argument("--out", required=True, type=Path, help="taxonomy-decisions.yaml output")
    parser.add_argument("--cycle-id", required=True, help="YYYYMMDD cycle identifier")
    parser.add_argument(
        "--min-miss-count",
        type=int,
        default=DEFAULT_MIN_MISS_COUNT,
        help=f"Ignore keys below this threshold (default {DEFAULT_MIN_MISS_COUNT})",
    )
    args = parser.parse_args()
    payload = json.loads(args.input_path.read_text(encoding="utf-8"))
    rows = payload.get("rows") or []
    aggregates = aggregate_miss_rows(rows, min_miss_count=args.min_miss_count)
    snapshot = load_canonical_snapshot()
    decisions = classify_all(aggregates, snapshot=snapshot, min_miss_count=args.min_miss_count)
    write_decisions_yaml(
        args.out,
        cycle_id=args.cycle_id,
        decisions=decisions,
        min_miss_count=args.min_miss_count,
    )
    pending = sum(1 for d in decisions if d.action == "pending")
    print(f"Wrote {len(decisions)} decisions ({pending} pending) → {args.out}")


if __name__ == "__main__":
    main()
