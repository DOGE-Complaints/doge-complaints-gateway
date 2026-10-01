#!/usr/bin/env python3
"""GW-REQ11-09 — operator CLI: seed threads comments/reactions after clustering.

Thin wrapper over doge-threads closed_http_seed.seed_representative_issues.
Fail-closed if GET /node/issues empty / no issue_id. Actors from life-sim
secrets by fixture_user_id (never SERVICE_API_TOKEN). Never mutates pack JSON.
Does not invent HTTP force-cluster or Closed APIs.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

SANDBOX = Path(__file__).resolve().parent
TESTS = SANDBOX.parent
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_replay_lib as replay  # noqa: E402
import life_sim_seed_threads_lib as seed_lib  # noqa: E402


def _load_dotenv_files() -> None:
    """Best-effort load gateway + threads .env (no secrets into argv)."""
    for path in (
        SANDBOX.parent.parent / ".env",
        SANDBOX.parent.parent / ".env.test",
        seed_lib.MONOREPO / "doge-threads" / ".env",
    ):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, _, val = raw.partition("=")
            key = key.strip()
            val = val.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = val


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Life-sim threads seed after cluster. "
            "Fail-closed without non-empty GET /node/issues."
        )
    )
    p.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Seed at most N issues (smoke).",
    )
    p.add_argument(
        "--limit-actors",
        type=int,
        default=None,
        help="Password-grant at most N fixture actors from secrets.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse handoffs + list actor ids; do not password-grant or seed HTTP.",
    )
    p.add_argument(
        "--gateway-url",
        default=None,
        help="Override GATEWAY_URL (default profile local :8000).",
    )
    p.add_argument(
        "--threads-url",
        default=None,
        help="Override THREADS_URL / LIFE_SIM_THREADS_URL (default :8001).",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    _load_dotenv_files()

    gateway_url = (args.gateway_url or seed_lib.resolve_gateway_url()).rstrip("/")
    threads_url = (args.threads_url or seed_lib.resolve_threads_url()).rstrip("/")

    # Never write pack JSON (invariant).
    seed_lib.never_write_pack_json(replay.resolve_life_sim_pack_dir())

    try:
        payload = seed_lib.fetch_node_issues_json(gateway_url)
        rows = seed_lib.parse_node_issues_payload(payload)
        handoffs = seed_lib.handoffs_from_issue_rows(rows)
        seed_lib.require_nonempty_handoffs(handoffs)
        handoffs = seed_lib.apply_issue_limit(handoffs, args.limit)
        if not handoffs:
            raise RuntimeError(
                "fail-closed: --limit left zero issues after non-empty node/issues"
            )

        creds_index = replay.load_users_creds_index()
        actor_ids = seed_lib.load_actor_fixture_ids(
            creds_index, limit_actors=args.limit_actors
        )
        if not actor_ids:
            print(
                "ERROR: no secrets actors with email+password "
                "(LIFE_SIM_USERS_CREDS / .secrets/life_sim_users_creds_*)",
                file=sys.stderr,
            )
            return seed_lib.EXIT_NO_ACTORS

        print(
            seed_lib.dump_plan_json(
                handoffs=handoffs,
                actor_fixture_ids=actor_ids,
                gateway_url=gateway_url,
                threads_url=threads_url,
                dry_run=bool(args.dry_run),
            ),
            end="",
        )

        if args.dry_run:
            print(
                "dry-run: skip password-grant + seed_representative_issues",
                file=sys.stderr,
            )
            return 0

        # Live: resolve user Bearer per fixture_user_id (never service token).
        from simulation_intake_http import resolve_fixture_user_bearer_token

        bearer_map: dict[str, str] = {}
        for fid in actor_ids:
            entry = creds_index[fid]
            token = resolve_fixture_user_bearer_token(
                fid,
                email=str(entry.get("email") or ""),
                password=str(entry.get("password") or ""),
            )
            seed_lib.refuse_service_token_as_actor(token)
            bearer_map[fid] = token

        actors = seed_lib.actors_from_bearer_map(bearer_map)
        closed = seed_lib.import_closed_http_seed()

        import httpx

        with httpx.Client(
            base_url=threads_url, timeout=60.0, trust_env=False
        ) as transport:
            report = closed.seed_representative_issues(transport, handoffs, actors)

        import json

        print(
            json.dumps(
                {
                    "comments": len(report.comments),
                    "reactions": len(report.reactions),
                    "issues_seeded": len(handoffs),
                    "actors": len(actors),
                },
                ensure_ascii=False,
            )
        )
        return 0

    except RuntimeError as exc:
        msg = str(exc)
        print(f"ERROR: {msg}", file=sys.stderr)
        if "fail-closed" in msg and "issue" in msg:
            return seed_lib.EXIT_EMPTY_ISSUES
        if "FixtureActor" in msg or "no secrets actors" in msg:
            return seed_lib.EXIT_NO_ACTORS
        return seed_lib.EXIT_CONFIG
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return seed_lib.EXIT_CONFIG
    except Exception as exc:  # noqa: BLE001 — operator CLI last resort
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
