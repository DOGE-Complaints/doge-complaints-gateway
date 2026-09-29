"""Named demo life-sim profiles (GW-REQ11-02): local + uus-veerenni.

Selectable via DEMO_LIFE_SIM_PROFILE / load_profile(id). Profile JSON holds
URL defaults and env *names* only — never secret values.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

PROFILES_DIR = Path(__file__).resolve().parent
INDEX_PATH = PROFILES_DIR / "index.json"
SELECTION_ENV = "DEMO_LIFE_SIM_PROFILE"

# Substrings that must never appear as literal secret values in profile JSON.
_FORBIDDEN_SECRET_MARKERS = (
    "sk-",
    "eyJ",  # JWT-ish
    "Bearer ",
    "your-service-token-here",  # example placeholder ok only in .env.test.example, not profiles
)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Profile JSON root must be object: {path}")
    return data


def load_index() -> dict[str, Any]:
    """Load profiles registry (index.json)."""
    return _read_json(INDEX_PATH)


def list_profile_ids() -> list[str]:
    """Return selectable profile ids in registry order."""
    index = load_index()
    return [str(p["id"]) for p in index["profiles"]]


def _entry_for(profile_id: str) -> dict[str, Any]:
    index = load_index()
    for entry in index["profiles"]:
        if str(entry["id"]) == profile_id:
            return entry
    known = ", ".join(list_profile_ids())
    raise KeyError(f"Unknown profile_id={profile_id!r}; known: {known}")


def load_profile(profile_id: str) -> dict[str, Any]:
    """Load a named profile document by id."""
    entry = _entry_for(profile_id)
    path = PROFILES_DIR / str(entry["path"])
    if not path.is_file():
        raise FileNotFoundError(path)
    doc = _read_json(path)
    if str(doc.get("profile_id")) != profile_id:
        raise RuntimeError(
            f"profile_id mismatch: file={doc.get('profile_id')!r} expected={profile_id!r}"
        )
    return doc


def select_profile(profile_id: str | None = None, environ: dict[str, str] | None = None) -> dict[str, Any]:
    """Select profile by explicit id or DEMO_LIFE_SIM_PROFILE / index default."""
    env = environ if environ is not None else dict(os.environ)
    index = load_index()
    chosen = (profile_id or env.get(SELECTION_ENV) or index.get("default_profile_id") or "").strip()
    if not chosen:
        raise RuntimeError("No profile selected: pass profile_id or set DEMO_LIFE_SIM_PROFILE")
    return load_profile(chosen)


def collect_env_ref_names(profile: dict[str, Any]) -> set[str]:
    """Collect all *_env field values (env variable names) from a profile doc."""
    names: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key.endswith("_env") and isinstance(value, str) and value:
                    names.add(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(profile)
    return names


def assert_no_secret_literals(profile: dict[str, Any]) -> None:
    """Fail if profile JSON text contains forbidden secret-like literals."""
    raw = json.dumps(profile, ensure_ascii=False)
    for marker in _FORBIDDEN_SECRET_MARKERS:
        if marker in raw:
            raise AssertionError(f"Forbidden secret-like marker in profile: {marker!r}")
    # api_token / password must only appear as env *names*, not as value fields.
    for key in ("api_token", "password", "anon_key", "secret"):
        if key in profile:
            raise AssertionError(f"Literal secret field {key!r} not allowed in profile root")
