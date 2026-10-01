"""GW-REQ11-03/05 — life-sim fixtures + profile + auth helpers (tooling).

REQ11-05: prefer 1:1 secrets file Bearer (gitignored). Pool M=20 deprecated for
new Pass (kept for LIFE_SIM_USE_POOL_M20=1 emergency). Does not invent public
resident login APIs.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

SANDBOX = Path(__file__).resolve().parent
# Legacy flat sample paths (Absent after 2026-09-30 cleanup). Prefer LIFE_SIM_PACK_DIR.
USERS_PATH = SANDBOX / "dogestonia_life_sim_users_v0_1.json"
STORIES_PATH = SANDBOX / "dogestonia_life_sim_stories_v0_1.json"
META_PATH = SANDBOX / "dogestonia_life_sim_fixtures_v0_1_meta.json"
POOL_MANIFEST_PATH = SANDBOX / "life_sim_pool_m20.json"
MAP_PATH = SANDBOX / "life_sim_fixture_to_pool_map_v0_1.json"
SECRETS_DIR = SANDBOX / ".secrets"

POOL_SIZE = 20
EXPECTED_USERS = 200
EXPECTED_STORIES_MIN = 1600  # REQ11-01 scale lock (~1661)

# Env name patterns for pool slots 00..19 (admin-bootstrapped; values never in git).
POOL_EMAIL_ENV_TMPL = "LIFE_SIM_POOL_{slot:02d}_EMAIL"
POOL_PASSWORD_ENV_TMPL = "LIFE_SIM_POOL_{slot:02d}_PASSWORD"


def resolve_life_sim_pack_dir() -> Path | None:
    """Optional pack root: LIFE_SIM_PACK_DIR → users.json / stories.json / meta.json."""
    raw = os.getenv("LIFE_SIM_PACK_DIR", "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    return path


def life_sim_users_path() -> Path:
    pack = resolve_life_sim_pack_dir()
    if pack is not None:
        return pack / "users.json"
    return USERS_PATH


def life_sim_stories_path() -> Path:
    pack = resolve_life_sim_pack_dir()
    if pack is not None:
        return pack / "stories.json"
    return STORIES_PATH


def life_sim_meta_path() -> Path:
    pack = resolve_life_sim_pack_dir()
    if pack is not None:
        return pack / "meta.json"
    return META_PATH


def load_life_sim_users(path: Path | None = None) -> list[dict[str, Any]]:
    """Load REQ11-01 fixture users (no regeneration)."""
    data = json.loads((path or life_sim_users_path()).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("life-sim users root must be a JSON array")
    return data


def load_life_sim_stories(path: Path | None = None) -> list[dict[str, Any]]:
    """Load REQ11-01 fixture stories (no regeneration)."""
    data = json.loads((path or life_sim_stories_path()).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise RuntimeError("life-sim stories root must be a JSON array")
    return data


def load_life_sim_meta(path: Path | None = None) -> dict[str, Any]:
    """Load REQ11-01 fixture meta (scale lock)."""
    data = json.loads((path or life_sim_meta_path()).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("life-sim meta root must be a JSON object")
    return data


def assert_fixture_scale(
    users: list[dict[str, Any]] | None = None,
    stories: list[dict[str, Any]] | None = None,
    meta: dict[str, Any] | None = None,
) -> None:
    """Fail closed if on-disk scale does not match REQ11-01 operator lock."""
    users = users if users is not None else load_life_sim_users()
    stories = stories if stories is not None else load_life_sim_stories()
    meta = meta if meta is not None else load_life_sim_meta()
    if len(users) != EXPECTED_USERS:
        raise AssertionError(f"expected {EXPECTED_USERS} users, got {len(users)}")
    if len(stories) < EXPECTED_STORIES_MIN:
        raise AssertionError(
            f"expected >= {EXPECTED_STORIES_MIN} stories, got {len(stories)}"
        )
    counts = meta.get("counts") if isinstance(meta.get("counts"), dict) else {}
    if int(counts.get("users", -1)) != EXPECTED_USERS:
        raise AssertionError(f"meta.counts.users != {EXPECTED_USERS}")
    lock = meta.get("operator_lock") if isinstance(meta.get("operator_lock"), dict) else {}
    if int(lock.get("n_users", -1)) != EXPECTED_USERS:
        raise AssertionError(f"meta.operator_lock.n_users != {EXPECTED_USERS}")


def fixture_user_index(fixture_user_id: str) -> int:
    """Parse life-sim-user-NNNN → zero-based index."""
    prefix = "life-sim-user-"
    if not fixture_user_id.startswith(prefix):
        raise ValueError(f"unexpected fixture_user_id={fixture_user_id!r}")
    n = int(fixture_user_id[len(prefix) :])
    if n < 1:
        raise ValueError(f"fixture_user_id index must be >= 1: {fixture_user_id!r}")
    return n - 1


def map_fixture_user_to_pool_slot(
    fixture_user_id: str,
    *,
    pool_size: int = POOL_SIZE,
) -> int:
    """Deterministic map: fixture index % pool_size → slot 0..pool_size-1."""
    if pool_size != POOL_SIZE:
        raise ValueError(f"operator lock pool_size={POOL_SIZE}; got {pool_size}")
    return fixture_user_index(fixture_user_id) % pool_size


def build_fixture_to_pool_map(
    users: list[dict[str, Any]] | None = None,
    *,
    pool_size: int = POOL_SIZE,
) -> dict[str, Any]:
    """Build on-disk map artifact body (200 → M=20)."""
    users = users if users is not None else load_life_sim_users()
    entries: list[dict[str, Any]] = []
    for user in users:
        fid = str(user["fixture_user_id"])
        slot = map_fixture_user_to_pool_slot(fid, pool_size=pool_size)
        entries.append(
            {
                "fixture_user_id": fid,
                "pool_slot": slot,
                "email_env": POOL_EMAIL_ENV_TMPL.format(slot=slot),
                "password_env": POOL_PASSWORD_ENV_TMPL.format(slot=slot),
            }
        )
    return {
        "schema_note": "on-disk life-sim → pool map; not a public API contract",
        "pool_size": pool_size,
        "fixture_user_count": len(users),
        "mapping_rule": f"fixture_user_index % {pool_size}",
        "entries": entries,
    }


def write_fixture_to_pool_map(path: Path | None = None) -> Path:
    """Write deterministic map JSON under sandbox (idempotent content)."""
    out = path or MAP_PATH
    doc = build_fixture_to_pool_map()
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def load_fixture_to_pool_map(path: Path | None = None) -> dict[str, Any]:
    """Load map artifact; fail if pool_size / count lock violated."""
    doc = json.loads((path or MAP_PATH).read_text(encoding="utf-8"))
    if int(doc.get("pool_size", -1)) != POOL_SIZE:
        raise RuntimeError(f"map pool_size must be {POOL_SIZE}")
    if int(doc.get("fixture_user_count", -1)) != EXPECTED_USERS:
        raise RuntimeError(f"map fixture_user_count must be {EXPECTED_USERS}")
    entries = doc.get("entries")
    if not isinstance(entries, list) or len(entries) != EXPECTED_USERS:
        raise RuntimeError(f"map entries must have length {EXPECTED_USERS}")
    return doc


def build_pool_manifest(*, pool_size: int = POOL_SIZE) -> dict[str, Any]:
    """Admin-bootstrap pool template: env *names* only (M=20)."""
    if pool_size != POOL_SIZE:
        raise ValueError(f"operator lock pool_size={POOL_SIZE}; got {pool_size}")
    slots: list[dict[str, Any]] = []
    for slot in range(pool_size):
        slots.append(
            {
                "pool_slot": slot,
                "email_env": POOL_EMAIL_ENV_TMPL.format(slot=slot),
                "password_env": POOL_PASSWORD_ENV_TMPL.format(slot=slot),
                "phone_verified_required": True,
                "notes": "Admin-bootstrap verified user; fill env; never commit secrets.",
            }
        )
    return {
        "schema_note": "life-sim submitter pool M=20; env refs only; not a public API",
        "pool_size": pool_size,
        "auth_path": "supabase_password_grant",
        "supabase_url_env": "SUPABASE_URL",
        "supabase_anon_key_env": "SUPABASE_ANON_KEY",
        "slots": slots,
        "operator_steps": [
            "Admin-create M=20 phone_verified demo users (Identity/Supabase ops; not SPA per-run).",
            "Set LIFE_SIM_POOL_00_EMAIL/PASSWORD … LIFE_SIM_POOL_19_* in .env.test (gitignored).",
            "Replay resolves access_token per slot via existing password-grant helper — no new public APIs.",
        ],
    }


def write_pool_manifest(path: Path | None = None) -> Path:
    """Write pool M=20 manifest under sandbox."""
    out = path or POOL_MANIFEST_PATH
    out.write_text(
        json.dumps(build_pool_manifest(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return out


def load_pool_manifest(path: Path | None = None) -> dict[str, Any]:
    """Load pool manifest; enforce M=20."""
    doc = json.loads((path or POOL_MANIFEST_PATH).read_text(encoding="utf-8"))
    if int(doc.get("pool_size", -1)) != POOL_SIZE:
        raise RuntimeError(f"pool_size must be {POOL_SIZE}")
    slots = doc.get("slots")
    if not isinstance(slots, list) or len(slots) != POOL_SIZE:
        raise RuntimeError(f"slots must have length {POOL_SIZE}")
    return doc


def count_pool_slots_with_credentials(environ: dict[str, str] | None = None) -> int:
    """How many of M=20 slots have both email+password set (no values returned)."""
    import os

    env = environ if environ is not None else dict(os.environ)
    ready = 0
    for slot in range(POOL_SIZE):
        email = env.get(POOL_EMAIL_ENV_TMPL.format(slot=slot), "").strip()
        password = env.get(POOL_PASSWORD_ENV_TMPL.format(slot=slot), "").strip()
        if email and password:
            ready += 1
    return ready


def use_pool_m20_legacy() -> bool:
    """Emergency legacy: LIFE_SIM_USE_POOL_M20=1 forces deprecated pool path."""
    return os.getenv("LIFE_SIM_USE_POOL_M20", "").strip() == "1"


def resolve_users_creds_path() -> Path | None:
    """Resolve secrets JSON: LIFE_SIM_USERS_CREDS env, else newest under .secrets/."""
    import life_sim_provision_lib as provision

    explicit = os.getenv("LIFE_SIM_USERS_CREDS", "").strip()
    if explicit:
        path = Path(explicit)
        provision.assert_secrets_path_hygiene(path)
        return path
    return provision.discover_latest_creds_path()


def load_users_creds_index(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load fixture_user_id → {email,password,…} from gitignored secrets."""
    import life_sim_provision_lib as provision

    creds_path = path or resolve_users_creds_path()
    if creds_path is None:
        raise RuntimeError(
            "No life-sim users secrets file. Run "
            "`make life-sim-provision-users` (or set LIFE_SIM_USERS_CREDS). "
            "Pool M=20 is deprecated for new Pass (override LIFE_SIM_USE_POOL_M20=1 only)."
        )
    doc = provision.load_users_creds(creds_path)
    return provision.index_creds_by_fixture_user_id(doc)


def count_secrets_users_ready(path: Path | None = None) -> int:
    """How many secrets entries have email+password (no values returned)."""
    try:
        index = load_users_creds_index(path)
    except (RuntimeError, ValueError, OSError):
        return 0
    ready = 0
    for entry in index.values():
        if str(entry.get("email") or "").strip() and str(entry.get("password") or ""):
            ready += 1
    return ready


def life_sim_story_to_intake_payload(
    story: dict[str, Any],
    *,
    intake_schema_version: str,
    schema_binding: dict[str, Any],
    location_query: str | None = None,
) -> dict[str, Any]:
    """Convert one life-sim story fixture into gateway intake stash payload shape.

    Uses the same narrative/origin fields as simulation_runner canvas path —
    does not invent product APIs.
    """
    lang = str(story.get("language") or "en").strip() or "en"
    title = str(story.get("title") or "").strip()
    body = str(story.get("body") or "").strip()
    if not body:
        raise ValueError(f"story {story.get('fixture_story_id')!r} missing body")
    title_i18n = {k: (title if k == lang else title) for k in ("et", "ru", "en")}
    description_i18n = {k: (body if k == lang else body) for k in ("et", "ru", "en")}
    narrative: dict[str, Any] = {
        "original_text": body,
        "language": lang,
        "session_language": lang,
        "title": title_i18n,
        "description": description_i18n,
        "summary": {lang: body},
        "canonical_type": "complaint",
        "canonical_labels": [],
    }
    if location_query and location_query.strip():
        narrative["location_query"] = location_query.strip()
    fixture_story_id = str(story.get("fixture_story_id") or "unknown")
    return {
        "schema_version": intake_schema_version,
        "schema_binding": schema_binding,
        "narrative": narrative,
        "origin": {
            "source": "simulation",
            "conversation_id": fixture_story_id,
        },
    }
