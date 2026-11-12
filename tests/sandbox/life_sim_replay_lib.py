"""GW-REQ11-03/05 — life-sim fixtures + profile + auth helpers (tooling).

REQ11-05: prefer 1:1 secrets file Bearer (gitignored). Pool M=20 deprecated for
new Pass (kept for LIFE_SIM_USE_POOL_M20=1 emergency). Does not invent public
resident login APIs.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

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

# Theme label → uus_veerenni_civic/v3 exact-lens signals (taxonomy canonical_keys).
# Without service_object + facility_or_service_need, pack lenses skip (missing_value_policy).
_THEME_TO_V3_SIGNALS: dict[str, dict[str, str]] = {
    "waste": {
        "civic_domain": "cleanliness_waste",
        "failure_pattern": "capacity_shortage",
        "service_object": "waste_bin",
        "facility_or_service_need": "household_service",
    },
    "lighting": {
        "civic_domain": "safety",
        "failure_pattern": "broken_infrastructure",
        "service_object": "street_lighting",
        "facility_or_service_need": "community_space",
    },
    "pothole": {
        "civic_domain": "infrastructure_maintenance",
        "failure_pattern": "broken_infrastructure",
        "service_object": "pedestrian_route",
        "facility_or_service_need": "household_service",
    },
    "construction": {
        "civic_domain": "environment_comfort",
        "failure_pattern": "recurring_friction",
        "service_object": "community_space",
        "facility_or_service_need": "community_space",
    },
    "crossing": {
        "civic_domain": "mobility_access",
        "failure_pattern": "unsafe_condition",
        "service_object": "crossing",
        "facility_or_service_need": "household_service",
    },
    "noise": {
        "civic_domain": "environment_comfort",
        "failure_pattern": "recurring_friction",
        "service_object": "community_space",
        "facility_or_service_need": "community_space",
    },
    "parking": {
        "civic_domain": "mobility_access",
        "failure_pattern": "access_blocked",
        "service_object": "car_parking",
        "facility_or_service_need": "household_service",
    },
    "playground": {
        "civic_domain": "children_families",
        "failure_pattern": "maintenance_gap",
        "service_object": "playground",
        "facility_or_service_need": "children_indoor_space",
    },
    "greenery": {
        "civic_domain": "public_space",
        "failure_pattern": "maintenance_gap",
        "service_object": "green_space",
        "facility_or_service_need": "community_space",
    },
    "drainage": {
        "civic_domain": "infrastructure_maintenance",
        "failure_pattern": "broken_infrastructure",
        "service_object": "pedestrian_route",
        "facility_or_service_need": "household_service",
    },
}
_DEFAULT_V3_SIGNALS: dict[str, str] = {
    "civic_domain": "public_space",
    "failure_pattern": "recurring_friction",
    "service_object": "community_space",
    "facility_or_service_need": "community_space",
}


def v3_signals_from_canonical_labels(labels: list[str] | tuple[str, ...] | None) -> dict[str, str]:
    """Map life-sim theme labels to pack exact-lens signal tokens."""
    for label in labels or ():
        key = str(label).strip().lower()
        if key in _THEME_TO_V3_SIGNALS:
            return dict(_THEME_TO_V3_SIGNALS[key])
    return dict(_DEFAULT_V3_SIGNALS)


def enrich_schema_binding_for_life_sim_story(
    schema_binding: Mapping[str, Any],
    story: Mapping[str, Any],
) -> dict[str, Any]:
    """Copy binding and fill structured_payload.signals from story canonical_labels."""
    binding = dict(schema_binding)
    raw_payload = binding.get("structured_payload")
    payload: dict[str, Any] = dict(raw_payload) if isinstance(raw_payload, Mapping) else {}
    raw_signals = payload.get("signals")
    signals: dict[str, Any] = dict(raw_signals) if isinstance(raw_signals, Mapping) else {}
    labels_raw = story.get("canonical_labels")
    labels = (
        [str(x) for x in labels_raw if str(x).strip()]
        if isinstance(labels_raw, list)
        else []
    )
    signals.update(v3_signals_from_canonical_labels(labels))
    canonical_type = str(story.get("canonical_type") or "").strip()
    if canonical_type:
        signals.setdefault("canonical_type", canonical_type)
    payload["signals"] = signals
    binding["structured_payload"] = payload
    return binding


def resolve_life_sim_pack_dir() -> Path | None:
    """Optional pack root: LIFE_SIM_PACK_DIR → users.json / stories.json / meta.json."""
    raw = os.getenv("LIFE_SIM_PACK_DIR", "").strip() or os.getenv("PACK_DIR", "").strip()
    if not raw:
        return None
    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    return path


def require_life_sim_pack_dir(*, require_stories: bool = True) -> Path:
    """Fail-closed pack root for REQ11-10 replay (LIFE_SIM_PACK_DIR / PACK_DIR)."""
    path = resolve_life_sim_pack_dir()
    if path is None:
        raise RuntimeError(
            "LIFE_SIM_PACK_DIR (or PACK_DIR) is required for pack-wave replay"
        )
    if require_stories and not (path / "stories.json").is_file():
        raise RuntimeError(f"stories.json missing under pack: {path}")
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


def _i18n_triplet(
    primary: Mapping[str, Any] | None,
    *,
    fallback: str,
    langs: tuple[str, ...] = ("et", "ru", "en"),
) -> dict[str, str]:
    """Build et/ru/en map from optional i18n object; fill gaps from fallback."""
    src = primary if isinstance(primary, Mapping) else {}
    out: dict[str, str] = {}
    for lang in langs:
        raw = src.get(lang)
        text = str(raw).strip() if raw is not None else ""
        out[lang] = text or fallback
    return out


def life_sim_story_to_intake_payload(
    story: dict[str, Any],
    *,
    intake_schema_version: str,
    schema_binding: dict[str, Any],
    location_query: str | None = None,
) -> dict[str, Any]:
    """Convert one life-sim story fixture into gateway intake stash payload shape.

    v2 packs: prefer title_i18n / summary_i18n / description_i18n / session_language /
    location_query / canonical_* (REQ11-12). Thin 6-key packs fall back to title/body.
    """
    lang = str(
        story.get("session_language") or story.get("language") or "en"
    ).strip() or "en"
    title = str(story.get("title") or "").strip()
    body = str(story.get("body") or "").strip()
    if not body:
        # Prefer description/summary of session language when body absent.
        desc = story.get("description_i18n")
        if isinstance(desc, Mapping) and desc.get(lang):
            body = str(desc.get(lang)).strip()
        elif isinstance(desc, Mapping):
            body = str(next((desc[k] for k in ("et", "ru", "en") if desc.get(k)), "")).strip()
    if not body:
        raise ValueError(f"story {story.get('fixture_story_id')!r} missing body")

    title_i18n = _i18n_triplet(story.get("title_i18n"), fallback=title or body)
    description_i18n = _i18n_triplet(story.get("description_i18n"), fallback=body)
    summary_src = story.get("summary_i18n")
    if isinstance(summary_src, Mapping) and any(
        str(summary_src.get(k) or "").strip() for k in ("et", "ru", "en")
    ):
        summary_i18n = _i18n_triplet(summary_src, fallback=body)
    else:
        # 6-key / thin: gateway requires narrative.summary.et (and peers).
        summary_i18n = {k: body for k in ("et", "ru", "en")}

    canonical_type = str(story.get("canonical_type") or "complaint").strip() or "complaint"
    labels_raw = story.get("canonical_labels")
    canonical_labels = (
        [str(x) for x in labels_raw if str(x).strip()]
        if isinstance(labels_raw, list)
        else []
    )

    narrative: dict[str, Any] = {
        "original_text": body,
        "language": lang,
        "session_language": lang,
        "title": title_i18n,
        "description": description_i18n,
        "summary": summary_i18n,
        "canonical_type": canonical_type,
        "canonical_labels": canonical_labels,
    }
    loc = (location_query or str(story.get("location_query") or "")).strip()
    if loc:
        narrative["location_query"] = loc
    inst = story.get("institution_i18n")
    if isinstance(inst, Mapping) and any(str(inst.get(k) or "").strip() for k in ("et", "ru", "en")):
        narrative["institution"] = _i18n_triplet(inst, fallback="")

    fixture_story_id = str(story.get("fixture_story_id") or "unknown")
    return {
        "schema_version": intake_schema_version,
        "schema_binding": enrich_schema_binding_for_life_sim_story(schema_binding, story),
        "narrative": narrative,
        "origin": {
            "source": "simulation",
            "conversation_id": fixture_story_id,
        },
    }
