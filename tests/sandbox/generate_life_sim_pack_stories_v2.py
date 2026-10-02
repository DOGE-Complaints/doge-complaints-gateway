#!/usr/bin/env python3
"""CLI: write life-sim pack stories.json v2 under life_sim_packs/<pack_id>/.

Successor path for REQ11-12 (does not treat flat *_v0_1 sandbox JSON as SSOT).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from life_sim_stories_v2_lib import (
    SEED,
    default_params_snapshot,
    load_params,
    write_pack,
)

ROOT = Path(__file__).resolve().parent
PACKS_ROOT = ROOT / "life_sim_packs"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate life-sim pack v2 stories")
    parser.add_argument(
        "--pack-id",
        required=True,
        help="Pack folder name under tests/sandbox/life_sim_packs/",
    )
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument(
        "--params",
        type=Path,
        default=None,
        help="Optional params.json path (default: pack params or civic defaults)",
    )
    parser.add_argument(
        "--defaults",
        action="store_true",
        help="Force civic default params snapshot (ignore existing pack params)",
    )
    args = parser.parse_args(argv)

    pack_dir = PACKS_ROOT / args.pack_id
    if args.defaults:
        params = default_params_snapshot(seed=args.seed)
    elif args.params is not None:
        params = load_params(args.params)
        if not params:
            params = default_params_snapshot(seed=args.seed)
    elif (pack_dir / "params.json").is_file():
        params = load_params(pack_dir / "params.json")
    else:
        params = default_params_snapshot(seed=args.seed)

    meta = write_pack(
        pack_dir,
        seed=args.seed,
        params=params,
        pack_id=args.pack_id,
        write_params=True,
    )
    print(json.dumps(meta.get("counts"), indent=2))
    print(json.dumps(meta.get("diversity"), indent=2))
    print(f"wrote {pack_dir / 'stories.json'}")
    print(f"wrote {pack_dir / 'users.json'}")
    print(f"wrote {pack_dir / 'meta.json'}")
    print(f"wrote {pack_dir / 'params.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
