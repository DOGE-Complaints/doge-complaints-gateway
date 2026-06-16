#!/usr/bin/env python3
"""Fetch ranked label translation misses for taxonomy cycle TC1."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.taxonomy.cycle_lib import utc_now_iso  # noqa: E402

_GATEWAY_ROOT = Path(__file__).resolve().parents[1]
_DOTENV_PATH = _GATEWAY_ROOT / ".env"


def _strip_env_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] in "\"'":
        return value[1:-1]
    return value


def _parse_dotenv(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    result: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("export "):
            stripped = stripped.removeprefix("export ").strip()
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", stripped)
        if not match:
            continue
        result[match.group(1)] = _strip_env_value(match.group(2))
    return result


def _fetch_sqlite(database_url: str) -> list[dict[str, Any]]:
    if database_url.startswith("sqlite:///"):
        db_path = database_url.removeprefix("sqlite:///")
    else:
        db_path = database_url.removeprefix("sqlite://")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute(
            """
            SELECT label_key, locale, miss_count, last_seen_at
            FROM label_translation_misses
            ORDER BY miss_count DESC, last_seen_at DESC
            """
        ).fetchall()
        return [
            {
                "label_key": str(row["label_key"]),
                "locale": str(row["locale"]),
                "miss_count": int(row["miss_count"]),
                "last_seen_at": str(row["last_seen_at"]),
            }
            for row in rows
        ]
    finally:
        conn.close()


def _fetch_supabase(supabase_url: str, service_role: str) -> list[dict[str, Any]]:
    try:
        import httpx  # pyright: ignore[reportMissingImports]
    except ImportError as exc:
        raise SystemExit("Supabase fetch requires httpx.") from exc
    headers = {
        "apikey": service_role,
        "Authorization": f"Bearer {service_role}",
    }
    params = {
        "select": "label_key,locale,miss_count,last_seen_at",
        "order": "miss_count.desc,last_seen_at.desc",
    }
    url = supabase_url.rstrip("/") + "/rest/v1/label_translation_misses"
    with httpx.Client(timeout=15.0) as client:
        response = client.get(url, headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()
    if not isinstance(payload, list):
        raise SystemExit(f"Unexpected Supabase response: {payload!r}")
    return [
        {
            "label_key": str(row["label_key"]),
            "locale": str(row["locale"]),
            "miss_count": int(row["miss_count"]),
            "last_seen_at": str(row["last_seen_at"]),
        }
        for row in payload
    ]


def fetch_misses() -> list[dict[str, Any]]:
    env = _parse_dotenv(_DOTENV_PATH)
    db_backend = (env.get("DB_BACKEND") or "").strip().lower()
    supabase_url = (env.get("SUPABASE_URL") or "").strip()
    service_role = (env.get("SUPABASE_SERVICE_ROLE") or "").strip()
    database_url = (env.get("DATABASE_URL") or "").strip()

    if supabase_url and service_role and db_backend != "sqlite":
        return _fetch_supabase(supabase_url, service_role)
    if database_url.startswith("sqlite"):
        return _fetch_sqlite(database_url)
    if supabase_url and service_role:
        return _fetch_supabase(supabase_url, service_role)
    raise SystemExit(
        "Cannot fetch misses: configure SUPABASE_URL + SUPABASE_SERVICE_ROLE or sqlite DATABASE_URL in .env"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch label translation misses (taxonomy TC1).")
    parser.add_argument(
        "--out",
        required=True,
        type=Path,
        help="Output JSON path (e.g. run-reports/taxonomy-cycles/cycle-YYYYMMDD/misses-ranked.json)",
    )
    args = parser.parse_args()
    rows = fetch_misses()
    payload = {"fetched_at": utc_now_iso(), "rows": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} rows → {args.out}")


if __name__ == "__main__":
    main()
