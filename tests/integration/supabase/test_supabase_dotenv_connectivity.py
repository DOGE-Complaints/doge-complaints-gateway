from __future__ import annotations

import os
import re
import warnings
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]

from core.infrastructure.db_supabase import SupabaseDatabase

_PACKAGE_ROOT = Path(__file__).resolve().parents[3]
_DOTENV_PATH = _PACKAGE_ROOT / ".env"


def _strip_env_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1]
    return value


def _parse_dotenv_file(path: Path) -> dict[str, str]:
    """Parse KEY=value lines without loading into os.environ."""
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
        key, raw_val = match.group(1), match.group(2)
        result[key] = _strip_env_value(raw_val)
    return result


def _require_supabase_creds_from_dotenv() -> tuple[str, str, dict[str, str]]:
    if not _DOTENV_PATH.is_file():
        pytest.skip(f"No {_DOTENV_PATH} file; cannot read SUPABASE_URL / SUPABASE_SERVICE_ROLE.")
    data = _parse_dotenv_file(_DOTENV_PATH)
    url = data.get("SUPABASE_URL", "").strip()
    key = data.get("SUPABASE_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip(
            ".env exists but SUPABASE_URL and/or SUPABASE_SERVICE_ROLE are missing or empty; "
            "skipping live Supabase check (typical for DB_BACKEND=in_memory-only setups)."
        )
    return url, key, data


def _diagnostic_report(*, dotenv_data: dict[str, str]) -> str:
    db_backend_file = (dotenv_data.get("DB_BACKEND") or "").strip().lower() or None
    db_backend_process = (os.environ.get("DB_BACKEND") or "").strip().lower() or None
    lines = [
        "Supabase .env connectivity: HTTP + schema checks passed.",
        f"  DB_BACKEND in .env file: {db_backend_file or '(not set in file)'}",
        f"  DB_BACKEND in process env: {db_backend_process or '(not set)'}",
    ]
    effective = db_backend_process or db_backend_file
    if effective == "in_memory":
        lines.append(
            "  InMemoryStoryRepository: successful POST /story-drafts (stash-only) does not "
            "write stories to Supabase; an empty `stories` table in the project DB is expected, not a REST failure."
        )
    elif effective == "supabase":
        lines.append(
            "  App config targets Supabase persistence. If server logs still show "
            "backend=in_memory, restart uvicorn with the same .env (or export DB_BACKEND=supabase)."
        )
    else:
        lines.append(
            "  Set DB_BACKEND explicitly in .env to align persistence with where you inspect data "
            "(in_memory vs supabase)."
        )
    return "\n".join(lines)


def test_supabase_connectivity_from_dotenv_credentials() -> None:
    supabase_url, service_role_key, dotenv_data = _require_supabase_creds_from_dotenv()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    assert db.healthcheck() is True, "GET /rest/v1/ should succeed with service role"
    assert db.required_tables_ready() is True, "Required PostgREST tables missing or inaccessible"
    if not db.required_columns_ready():
        pytest.skip(
            "Required stories/geo/narrative or embedding columns are missing on remote (PostgREST select probe "
            "failed). Apply doge-complaints-gateway/supabase/bootstrap and migrations to the Supabase project "
            "referenced by this .env."
        )
    if not db.required_stories_narrative_extension_columns_ready():
        pytest.skip(
            "Stories table missing STORY-M2-02-06 narrative extension columns; apply migration "
            "doge-complaints-gateway/supabase/migrations/20260511_1200_m2_02_stories_narrative_extensions.sql "
            "on this Supabase project. Until then, SupabaseStoryRepository GET uses columns not present remotely."
        )

    warnings.warn(_diagnostic_report(dotenv_data=dotenv_data), UserWarning, stacklevel=1)
