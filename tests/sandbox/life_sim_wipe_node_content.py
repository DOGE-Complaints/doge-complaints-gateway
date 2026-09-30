#!/usr/bin/env python3
"""GW-REQ11-06 — wipe node content (stories + derivatives + threads).

Usage (from doge-complaints-gateway/):
  .venv/bin/python tests/sandbox/life_sim_wipe_node_content.py --dry-run
  .venv/bin/python tests/sandbox/life_sim_wipe_node_content.py --confirm-wipe
  LIFE_SIM_WIPE_CONFIRMED=1 make life-sim-wipe-node-content

Requires: SUPABASE_URL + SUPABASE_SERVICE_ROLE (gateway).
Optional: THREADS_SUPABASE_URL + THREADS_SUPABASE_SERVICE_ROLE (else same as gateway).

Does NOT delete Identity auth.users / admin.
Does NOT invent wipe HTTP API. Does NOT DROP schema.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib import error, parse, request

_SANDBOX = Path(__file__).resolve().parent
_TESTS = _SANDBOX.parent
_GATEWAY_ROOT = _TESTS.parent
_REPO_MONOREPO = _GATEWAY_ROOT.parent

if str(_SANDBOX) not in sys.path:
    sys.path.insert(0, str(_SANDBOX))

import life_sim_wipe_lib as wipe  # noqa: E402


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if " #" in line:
            line = line.split(" #", 1)[0].rstrip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_env_file(_GATEWAY_ROOT / ".env.test")
    _load_env_file(_GATEWAY_ROOT / ".env")
    _load_env_file(_REPO_MONOREPO / "doge-threads" / ".env")


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env variable: {name}")
    return value


def _gateway_creds() -> tuple[str, str]:
    return _required_env("SUPABASE_URL").rstrip("/"), _required_env(
        "SUPABASE_SERVICE_ROLE"
    )


def _threads_creds() -> tuple[str, str]:
    url = os.getenv("THREADS_SUPABASE_URL", "").strip()
    role = os.getenv("THREADS_SUPABASE_SERVICE_ROLE", "").strip()
    if url and role:
        return url.rstrip("/"), role
    return _gateway_creds()


def _delete_all_rows(
    *,
    base_url: str,
    service_role: str,
    table: str,
    filter_column: str,
    dry_run: bool,
) -> dict[str, Any]:
    """DELETE via PostgREST: filter column not.is.null (all non-null PK rows)."""
    path = f"/rest/v1/{table}"
    query = parse.urlencode({filter_column: "not.is.null"})
    url = f"{base_url}{path}?{query}"
    if dry_run:
        return {
            "table": table,
            "dry_run": True,
            "method": "DELETE",
            "url": url,
            "status": "planned",
        }
    req = request.Request(
        url,
        method="DELETE",
        headers={
            "apikey": service_role,
            "Authorization": f"Bearer {service_role}",
            "Prefer": "return=minimal",
        },
    )
    try:
        with request.urlopen(req, timeout=120) as resp:
            status = getattr(resp, "status", 200)
            return {"table": table, "dry_run": False, "status": status, "ok": True}
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        return {
            "table": table,
            "dry_run": False,
            "status": exc.code,
            "ok": False,
            "error": body,
        }
    except error.URLError as exc:
        return {
            "table": table,
            "dry_run": False,
            "status": None,
            "ok": False,
            "error": str(exc.reason),
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Wipe gateway story stack + threads content (not Identity)."
    )
    parser.add_argument(
        "--confirm-wipe",
        action="store_true",
        help="Required for destructive DELETE (or LIFE_SIM_WIPE_CONFIRMED=1).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List planned deletes; no DELETE. Confirm not required.",
    )
    parser.add_argument(
        "--gateway-only",
        action="store_true",
        help="Skip threads tables.",
    )
    parser.add_argument(
        "--threads-only",
        action="store_true",
        help="Skip gateway readiness tables.",
    )
    args = parser.parse_args(argv)

    if args.gateway_only and args.threads_only:
        print("ERROR: --gateway-only and --threads-only are mutually exclusive", file=sys.stderr)
        return 2

    plan = wipe.full_wipe_plan()
    if args.gateway_only:
        plan = [p for p in plan if p[0] == "gateway"]
    elif args.threads_only:
        plan = [p for p in plan if p[0] == "threads"]

    if args.dry_run:
        print("DRY-RUN wipe plan (no DELETE):")
        for scope, table, col in plan:
            print(f"  [{scope}] DELETE {table} WHERE {col} IS NOT NULL")
        print(
            "Confirm for live: --confirm-wipe or LIFE_SIM_WIPE_CONFIRMED=1. "
            "Never deletes Identity auth.users."
        )
        return 0

    if not wipe.wipe_confirmed(cli_confirm=args.confirm_wipe):
        print(
            "REFUSED: wipe requires --confirm-wipe or LIFE_SIM_WIPE_CONFIRMED=1. "
            "Use --dry-run to preview.",
            file=sys.stderr,
        )
        return 2

    _load_env()
    results: list[dict[str, Any]] = []
    failed = False

    need_gateway = any(s == "gateway" for s, _, _ in plan)
    need_threads = any(s == "threads" for s, _, _ in plan)
    gw_url = gw_role = thr_url = thr_role = ""
    try:
        if need_gateway:
            gw_url, gw_role = _gateway_creds()
        if need_threads:
            thr_url, thr_role = _threads_creds()
    except RuntimeError as exc:
        print(f"BLOCKER env: {exc}", file=sys.stderr)
        return 3

    for scope, table, col in plan:
        base, role = (gw_url, gw_role) if scope == "gateway" else (thr_url, thr_role)
        result = _delete_all_rows(
            base_url=base,
            service_role=role,
            table=table,
            filter_column=col,
            dry_run=False,
        )
        result["scope"] = scope
        results.append(result)
        if not result.get("ok"):
            failed = True
            print(
                f"FAIL [{scope}] {table}: status={result.get('status')} "
                f"error={result.get('error')}",
                file=sys.stderr,
            )
        else:
            print(f"OK [{scope}] {table}: HTTP {result.get('status')}")

    print(json.dumps({"ok": not failed, "results": results}, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
