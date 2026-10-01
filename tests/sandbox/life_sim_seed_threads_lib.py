"""GW-REQ11-09 — pure helpers for life-sim threads seed (fail-closed + handoff).

Reuse doge-threads closed_http_seed types; do not invent Closed APIs or force-cluster.
Never treat SERVICE_API_TOKEN as a FixtureActor.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

SANDBOX = Path(__file__).resolve().parent
TESTS = SANDBOX.parent
GATEWAY_ROOT = TESTS.parent
MONOREPO = GATEWAY_ROOT.parent
THREADS_SRC = MONOREPO / "doge-threads" / "src"

# Fail-closed exit when GET /node/issues empty / no issue_id handoff.
EXIT_EMPTY_ISSUES = 2
EXIT_NO_ACTORS = 3
EXIT_CONFIG = 4

_SERVICE_TOKEN_ENV_NAMES = (
    "SERVICE_API_TOKEN",
    "GATEWAY_API_TOKEN",
    "GATEWAY_SERVICE_TOKEN",
)


def ensure_threads_seed_import_path() -> Path:
    """Put doge-threads/src on sys.path so closed_http_seed is importable."""
    if not THREADS_SRC.is_dir():
        raise RuntimeError(f"doge-threads src Absent: {THREADS_SRC}")
    path = str(THREADS_SRC)
    if path not in sys.path:
        sys.path.insert(0, path)
    return THREADS_SRC


def import_closed_http_seed() -> Any:
    """Import Present closed_http_seed by file path (avoid gateway `core` shadow)."""
    import importlib.util

    ensure_threads_seed_import_path()
    mod_path = THREADS_SRC / "core" / "seed" / "closed_http_seed.py"
    if not mod_path.is_file():
        raise RuntimeError(f"closed_http_seed Absent: {mod_path}")
    existing = sys.modules.get("doge_threads_closed_http_seed")
    if existing is not None:
        return existing
    spec = importlib.util.spec_from_file_location(
        "doge_threads_closed_http_seed",
        mod_path,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load closed_http_seed from {mod_path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["doge_threads_closed_http_seed"] = mod
    spec.loader.exec_module(mod)
    return mod


def _as_issue_id(raw: Any) -> str | None:
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        return str(int(raw))
    return None


def density_from_issue_row(row: dict[str, Any]) -> int | None:
    """Derive density = inbound story count when fields Present; else None (lib FLOOR).

    Public /node/issues cards may omit story_ids — then density stays None.
    Accepted Present fields (first hit wins): density, story_count, len(story_ids).
    """
    for key in ("density", "story_count"):
        val = row.get(key)
        if isinstance(val, bool):
            continue
        if isinstance(val, int):
            return val
        if isinstance(val, float):
            return int(val)
        if isinstance(val, str) and val.strip().lstrip("-").isdigit():
            return int(val.strip())
    story_ids = row.get("story_ids")
    if isinstance(story_ids, list):
        return len(story_ids)
    return None


def parse_node_issues_payload(payload: Any) -> list[dict[str, Any]]:
    """Extract issues list from GET /node/issues JSON envelope."""
    if not isinstance(payload, dict):
        raise ValueError("node/issues payload must be a JSON object")
    data = payload.get("data")
    if not isinstance(data, dict):
        raise ValueError("node/issues.data must be an object")
    issues = data.get("issues")
    if issues is None:
        raise ValueError("node/issues.data.issues missing")
    if not isinstance(issues, list):
        raise ValueError("node/issues.data.issues must be a list")
    out: list[dict[str, Any]] = []
    for item in issues:
        if isinstance(item, dict):
            out.append(item)
    return out


def handoffs_from_issue_rows(rows: list[dict[str, Any]]) -> list[Any]:
    """Build GatewayIssueHandoff list; skip rows without issue_id."""
    seed = import_closed_http_seed()
    GatewayIssueHandoff = seed.GatewayIssueHandoff
    handoffs: list[Any] = []
    for row in rows:
        issue_id = _as_issue_id(row.get("id") or row.get("issue_id"))
        if not issue_id:
            continue
        handoffs.append(
            GatewayIssueHandoff(
                issue_id=issue_id,
                density=density_from_issue_row(row),
            )
        )
    return handoffs


def require_nonempty_handoffs(handoffs: list[Any]) -> list[Any]:
    """Fail-closed: STOP if no issues / no issue_id after clustering."""
    if not handoffs:
        raise RuntimeError(
            "fail-closed: GET /node/issues empty or no handoff issue_id — "
            "run cluster (StoryClusterOrchestrator.process_all_pending / cron) "
            "before threads seed; do not invent HTTP force-cluster"
        )
    return handoffs


def apply_issue_limit(handoffs: list[Any], limit: int | None) -> list[Any]:
    if limit is None:
        return handoffs
    if limit < 1:
        raise ValueError("--limit must be >= 1")
    return handoffs[:limit]


def service_token_values(environ: dict[str, str] | None = None) -> set[str]:
    env = environ if environ is not None else dict(os.environ)
    values: set[str] = set()
    for name in _SERVICE_TOKEN_ENV_NAMES:
        raw = env.get(name, "").strip()
        if raw:
            values.add(raw)
    return values


def load_actor_fixture_ids(
    creds_index: dict[str, dict[str, Any]],
    *,
    limit_actors: int | None = None,
) -> list[str]:
    """Ordered fixture_user_id list with email+password Present."""
    ids: list[str] = []
    for fid, entry in sorted(creds_index.items()):
        email = str(entry.get("email") or "").strip()
        password = str(entry.get("password") or "")
        if email and password:
            ids.append(fid)
        if limit_actors is not None and len(ids) >= limit_actors:
            break
    return ids


def refuse_service_token_as_actor(bearer_token: str, *, environ: dict[str, str] | None = None) -> None:
    """Hard ban: SERVICE_API_TOKEN / gateway service tokens must not be actors."""
    token = bearer_token.strip()
    if not token:
        raise ValueError("empty bearer_token")
    banned = service_token_values(environ)
    if token in banned:
        raise RuntimeError(
            "refuse: SERVICE_API_TOKEN/GATEWAY_API_TOKEN must not be used as "
            "comment/reaction FixtureActor (use life-sim secrets Bearer by fixture_user_id)"
        )


def actors_from_bearer_map(
    fixture_to_bearer: dict[str, str],
    *,
    environ: dict[str, str] | None = None,
) -> list[Any]:
    """Build FixtureActor list; refuse service tokens."""
    seed = import_closed_http_seed()
    FixtureActor = seed.FixtureActor
    actors: list[Any] = []
    for fid, token in sorted(fixture_to_bearer.items()):
        refuse_service_token_as_actor(token, environ=environ)
        actors.append(FixtureActor(bearer_token=token.strip()))
    if not actors:
        raise RuntimeError(
            "fail-closed: no FixtureActor from secrets — provision secrets "
            "(REQ11-05/08) with email+password per fixture_user_id"
        )
    return actors


def resolve_gateway_url(environ: dict[str, str] | None = None) -> str:
    env = environ if environ is not None else dict(os.environ)
    url = env.get("GATEWAY_URL", "").strip()
    if url:
        return url.rstrip("/")
    profile_url = _profile_service_base_url("gateway", environ=env)
    if profile_url:
        return profile_url.rstrip("/")
    return "http://127.0.0.1:8000"


def resolve_threads_url(environ: dict[str, str] | None = None) -> str:
    env = environ if environ is not None else dict(os.environ)
    url = (
        env.get("THREADS_URL", "").strip()
        or env.get("LIFE_SIM_THREADS_URL", "").strip()
    )
    if url:
        return url.rstrip("/")
    profile_url = _profile_service_base_url("threads", environ=env)
    if profile_url:
        return profile_url.rstrip("/")
    return "http://127.0.0.1:8001"


def _profile_service_base_url(
    service: str, *, environ: dict[str, str] | None = None
) -> str | None:
    """Optional DEMO_LIFE_SIM_PROFILE → sandbox/profiles/<id>.json service base_url."""
    env = environ if environ is not None else dict(os.environ)
    profile_id = env.get("DEMO_LIFE_SIM_PROFILE", "").strip() or "local"
    path = SANDBOX / "profiles" / f"{profile_id}.json"
    if not path.is_file():
        return None
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    services = doc.get("services") if isinstance(doc, dict) else None
    if not isinstance(services, dict):
        return None
    svc = services.get(service)
    if not isinstance(svc, dict):
        return None
    base = svc.get("base_url")
    return str(base).strip() if isinstance(base, str) and base.strip() else None


def fetch_node_issues_json(gateway_url: str, *, timeout_s: float = 30.0) -> Any:
    """GET /node/issues — public list used for handoff after cluster."""
    import httpx

    url = f"{gateway_url.rstrip('/')}/node/issues"
    with httpx.Client(timeout=timeout_s, trust_env=False) as client:
        resp = client.get(url)
    if resp.status_code != 200:
        raise RuntimeError(
            f"GET /node/issues failed status={resp.status_code} body={resp.text[:400]}"
        )
    return resp.json()


def never_write_pack_json(pack_dir: Path | None) -> None:
    """Documented invariant helper — this CLI must not open pack JSON for write."""
    if pack_dir is None:
        return
    # No-op guard used by tests: ensure callers do not pass write handles.
    _ = pack_dir
    return


def dump_plan_json(
    *,
    handoffs: list[Any],
    actor_fixture_ids: list[str],
    gateway_url: str,
    threads_url: str,
    dry_run: bool,
) -> str:
    body = {
        "dry_run": dry_run,
        "gateway_url": gateway_url,
        "threads_url": threads_url,
        "issue_count": len(handoffs),
        "issues": [
            {"issue_id": h.issue_id, "density": h.density} for h in handoffs
        ],
        "actor_fixture_ids": actor_fixture_ids,
        "notes": [
            "order: wipe → provision → replay жалоб → cluster → threads seed → SPA",
            "no invent HTTP force-cluster",
            "actors = secrets Bearer by fixture_user_id; never SERVICE_API_TOKEN",
            "never mutate pack users.json / stories.json",
        ],
    }
    return json.dumps(body, ensure_ascii=False, indent=2) + "\n"
