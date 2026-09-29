"""Remote simulation runner for DOGEstonia intake API.

Modes:
  (default) canvas scenarios from SIMULATION_CANVAS_PATH
  --life-sim  REQ11-03 profiled life-sim fixtures + pool M=20 multi-Bearer
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"
_TESTS = Path(__file__).resolve().parent
_SANDBOX = _TESTS / "sandbox"
_PROFILES = _SANDBOX / "profiles"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
if str(_PROFILES) not in sys.path:
    sys.path.insert(0, str(_PROFILES))
if str(_SANDBOX) not in sys.path:
    sys.path.insert(0, str(_SANDBOX))
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

from core.intake import INTAKE_SCHEMA_VERSION

from simulation_intake_http import (
    format_submit_failure,
    post_stash_and_submit_http,
    resolve_pool_slot_bearer_token,
    resolve_user_bearer_token,
)

import demo_life_sim_profiles as profiles  # noqa: E402
import life_sim_replay_lib as life_sim  # noqa: E402


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_env_file(Path(".env.test"))
    _load_env_file(Path(".env"))


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env variable: {name}")
    return value


def _parse_groups(raw: str | None) -> set[str] | None:
    if not raw:
        return None
    groups = {item.strip() for item in raw.split(",") if item.strip()}
    return groups or None


def _scenario_to_payload(scenario: dict[str, Any]) -> dict[str, Any]:
    cp = scenario["normalized_issue_payload"]["canonical_payload"]
    meta = scenario["normalized_issue_payload"]["normalization_metadata"]
    lang = str(meta["session_language"]).strip()

    title_map = cp.get("title", {}) if isinstance(cp.get("title"), dict) else {}
    summary_map = cp.get("summary", {}) if isinstance(cp.get("summary"), dict) else {}
    original_text = summary_map.get(lang) or summary_map.get("en", "")
    description_map = (
        cp.get("description", {}) if isinstance(cp.get("description"), dict) else {}
    )
    title_i18n: dict[str, str] = {}
    description_i18n: dict[str, str] = {}
    for lang_key in ("et", "ru", "en"):
        tv = title_map.get(lang_key)
        title_i18n[lang_key] = (
            tv.strip() if isinstance(tv, str) and tv.strip() else title_map.get("en", "") or ""
        )
        dv = description_map.get(lang_key) or summary_map.get(lang_key)
        description_i18n[lang_key] = (
            dv.strip() if isinstance(dv, str) and dv.strip() else original_text
        )

    summary_obj: dict[str, str] = {}
    for lang_key in ("et", "ru", "en"):
        sv = summary_map.get(lang_key)
        if isinstance(sv, str) and sv.strip():
            summary_obj[lang_key] = sv.strip()
    if summary_obj:
        narrative_summary = summary_obj
    else:
        narrative_summary = None

    narrative: dict[str, Any] = {
        "original_text": original_text,
        "language": lang,
        "session_language": lang,
        "title": title_i18n,
        "description": description_i18n,
        "canonical_type": cp.get("type"),
        "canonical_labels": cp.get("labels", []),
    }
    if narrative_summary is not None:
        narrative["summary"] = narrative_summary

    payload: dict[str, Any] = {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "narrative": narrative,
        "origin": {
            "source": "simulation",
            "conversation_id": scenario["simulation_id"],
        },
    }

    location_query = scenario.get("resident_input", {}).get("location_query")
    if isinstance(location_query, str) and location_query.strip():
        payload["narrative"]["location_query"] = location_query.strip()
    from gw_ssr_16_node_schema import active_node_schema_binding

    payload["schema_binding"] = active_node_schema_binding()
    return payload


def run_scenario_stash_submit(
    *,
    gateway_url: str,
    service_token: str,
    user_token: str,
    scenario: dict[str, Any],
) -> tuple[bool, int, str, str, str]:
    """Returns ok, status_code, detail, draft_id, story_id."""
    payload = _scenario_to_payload(scenario)
    status_code, response_text, draft_id, story_id = post_stash_and_submit_http(
        gateway_url=gateway_url,
        service_token=service_token,
        user_token=user_token,
        payload=payload,
    )
    if status_code == 202:
        return True, status_code, response_text, draft_id, story_id
    detail = format_submit_failure(status_code, response_text.strip())
    return False, status_code, detail, draft_id, story_id


def run_life_sim_payload_stash_submit(
    *,
    gateway_url: str,
    service_token: str,
    user_token: str,
    payload: dict[str, Any],
) -> tuple[bool, int, str, str, str]:
    """stash→submit one life-sim intake payload (same HTTP helpers as canvas)."""
    status_code, response_text, draft_id, story_id = post_stash_and_submit_http(
        gateway_url=gateway_url,
        service_token=service_token,
        user_token=user_token,
        payload=payload,
    )
    if status_code == 202:
        return True, status_code, response_text, draft_id, story_id
    detail = format_submit_failure(status_code, response_text.strip())
    return False, status_code, detail, draft_id, story_id


def _gateway_url_from_profile(profile: dict[str, Any]) -> str:
    """Resolve gateway base URL: env override (profile url_env) then profile default."""
    gw = profile.get("services", {}).get("gateway", {})
    url_env = str(gw.get("url_env") or "GATEWAY_URL")
    env_url = os.getenv(url_env, "").strip()
    if env_url:
        return env_url.rstrip("/")
    base = str(gw.get("base_url") or "").strip()
    if base:
        return base.rstrip("/")
    return _required_env("GATEWAY_URL").rstrip("/")


def _service_token_from_profile(profile: dict[str, Any]) -> str:
    gw = profile.get("services", {}).get("gateway", {})
    token_env = str(gw.get("api_token_env") or "GATEWAY_API_TOKEN")
    return _required_env(token_env)


def main_life_sim(args: argparse.Namespace) -> int:
    """Wipe/zero → profiled life-sim replay (operator wipe precondition)."""
    profile = profiles.select_profile(args.profile)
    life_sim.assert_fixture_scale()
    users = life_sim.load_life_sim_users()
    stories = life_sim.load_life_sim_stories()
    life_sim.load_pool_manifest()
    life_sim.load_fixture_to_pool_map()

    wipe_ok = args.wipe_confirmed or os.getenv("LIFE_SIM_WIPE_CONFIRMED", "").strip() == "1"
    if not wipe_ok:
        raise RuntimeError(
            "Wipe/zero precondition not confirmed. Operator must wipe the connected "
            "demo DB first, then re-run with --wipe-confirmed or LIFE_SIM_WIPE_CONFIRMED=1. "
            "No wipe HTTP API is invented here — see docs/analysis/note-gw-req11-03-*"
        )

    ready_slots = life_sim.count_pool_slots_with_credentials()
    if ready_slots < life_sim.POOL_SIZE and not args.dry_run:
        raise RuntimeError(
            f"Pool M={life_sim.POOL_SIZE} incomplete: {ready_slots}/{life_sim.POOL_SIZE} "
            "slots have LIFE_SIM_POOL_NN_EMAIL+PASSWORD. Admin-bootstrap remaining slots "
            "(env refs in tests/sandbox/life_sim_pool_m20.json). Use --dry-run for offline."
        )

    gateway_url = _gateway_url_from_profile(profile)
    service_token = _service_token_from_profile(profile)
    location_query = (
        args.location_query or os.getenv("LIFE_SIM_LOCATION_QUERY", "")
    ).strip() or None

    from gw_ssr_16_node_schema import active_node_schema_binding

    schema_binding = active_node_schema_binding()
    max_stories = args.max_stories
    selected = stories if max_stories is None else stories[:max_stories]

    print("DOGEstonia Life-Sim Replay Runner (REQ11-03)")
    print(f"Profile: {profile['profile_id']}")
    print(f"Fixtures: {len(users)} users / {len(stories)} stories (selected {len(selected)})")
    print(f"Pool: M={life_sim.POOL_SIZE} (ready_env_slots={ready_slots})")
    print(f"Target: {gateway_url}")
    print("Flow: POST /story-drafts (stash) -> POST /story-drafts/{{id}}/submit")
    print("Auth: multi-Bearer via pool map (no SPA resident login)")
    if args.dry_run:
        print("Mode: DRY-RUN (no HTTP)")
    print()

    successes = 0
    failures: list[str] = []
    slot_token_cache_hits: dict[int, int] = {}

    for index, story in enumerate(selected, start=1):
        fixture_story_id = str(story.get("fixture_story_id", f"idx-{index}"))
        fixture_user_id = str(story["fixture_user_id"])
        pool_slot = life_sim.map_fixture_user_to_pool_slot(fixture_user_id)
        try:
            payload = life_sim.life_sim_story_to_intake_payload(
                story,
                intake_schema_version=INTAKE_SCHEMA_VERSION,
                schema_binding=schema_binding,
                location_query=location_query,
            )
            if args.dry_run:
                print(
                    f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                    f"user={fixture_user_id} slot={pool_slot:02d} -> DRY-RUN ok"
                )
                successes += 1
                continue
            user_token = resolve_pool_slot_bearer_token(pool_slot)
            slot_token_cache_hits[pool_slot] = slot_token_cache_hits.get(pool_slot, 0) + 1
            ok, status_code, detail, draft_id, story_id = run_life_sim_payload_stash_submit(
                gateway_url=gateway_url,
                service_token=service_token,
                user_token=user_token,
                payload=payload,
            )
            if ok:
                print(
                    f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                    f"slot={pool_slot:02d} -> 201 stash draft_id={draft_id} "
                    f"-> 202 submit story_id={story_id}"
                )
                successes += 1
            else:
                print(
                    f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                    f"slot={pool_slot:02d} -> {status_code} ERROR detail={detail}"
                )
                failures.append(fixture_story_id)
        except Exception as exc:  # noqa: BLE001
            print(f"[{index:>4}/{len(selected)}] {fixture_story_id} -> EXCEPTION {exc}")
            failures.append(fixture_story_id)

    print()
    print("Summary:")
    print(f"  Total:   {len(selected)}")
    print(f"  Success: {successes}")
    print(f"  Failed:  {len(failures)}")
    slots_note: Any = len(slot_token_cache_hits) if slot_token_cache_hits else (
        "dry-run" if args.dry_run else 0
    )
    print(f"  Slots used: {slots_note}")
    if failures:
        preview = ", ".join(failures[:20])
        suffix = "..." if len(failures) > 20 else ""
        print(f"  Failed IDs: {preview}{suffix}")
        return 1
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run remote simulation / life-sim replay.")
    parser.add_argument("--max", dest="max_stories", type=int, default=None)
    parser.add_argument("--groups", type=str, default=None)
    parser.add_argument(
        "--life-sim",
        action="store_true",
        help="REQ11-03: profiled life-sim fixtures + pool M=20 multi-Bearer replay",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="DEMO_LIFE_SIM_PROFILE id (default: env or index default)",
    )
    parser.add_argument(
        "--wipe-confirmed",
        action="store_true",
        help="Confirm operator wiped/zeroed the target demo DB before replay",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build payloads + map slots only; no HTTP (offline contract check)",
    )
    parser.add_argument(
        "--location-query",
        type=str,
        default=None,
        help="Optional narrative.location_query for all life-sim stories",
    )
    return parser.parse_args()


def main() -> int:
    _load_env()
    args = _parse_args()

    if args.life_sim:
        return main_life_sim(args)

    gateway_url = _required_env("GATEWAY_URL").rstrip("/")
    gateway_api_token = _required_env("GATEWAY_API_TOKEN")
    gateway_user_token = resolve_user_bearer_token()
    canvas_path_raw = _required_env("SIMULATION_CANVAS_PATH")
    canvas_path = Path(canvas_path_raw)
    if not canvas_path.exists():
        raise RuntimeError(f"Canvas file does not exist: {canvas_path}")

    env_groups = _parse_groups(os.getenv("SIMULATION_GROUPS"))
    arg_groups = _parse_groups(args.groups)
    groups_filter = arg_groups if arg_groups is not None else env_groups

    env_max_raw = os.getenv("SIMULATION_MAX_STORIES", "").strip()
    env_max = int(env_max_raw) if env_max_raw else None
    max_stories = args.max_stories if args.max_stories is not None else env_max
    if max_stories is not None and max_stories < 1:
        raise RuntimeError("--max and SIMULATION_MAX_STORIES must be >= 1")

    scenarios = json.loads(canvas_path.read_text(encoding="utf-8"))
    if not isinstance(scenarios, list):
        raise RuntimeError("Canvas root must be a JSON array")

    filtered: list[dict[str, Any]] = []
    for scenario in scenarios:
        if groups_filter and scenario.get("scenario_group") not in groups_filter:
            continue
        filtered.append(scenario)
    if max_stories is not None:
        filtered = filtered[:max_stories]

    print("DOGEstonia Simulation Runner")
    print(f"Canvas: {canvas_path} ({len(filtered)} scenarios selected)")
    print(f"Target: {gateway_url}")
    print("Flow: POST /story-drafts (stash) -> POST /story-drafts/{{id}}/submit")
    print()

    successes = 0
    failures: list[str] = []
    for index, scenario in enumerate(filtered, start=1):
        simulation_id = str(scenario.get("simulation_id", f"idx-{index}"))
        try:
            ok, status_code, detail, draft_id, story_id = run_scenario_stash_submit(
                gateway_url=gateway_url,
                service_token=gateway_api_token,
                user_token=gateway_user_token,
                scenario=scenario,
            )
            if ok:
                print(
                    f"[{index:>3}/{len(filtered)}] {simulation_id} -> "
                    f"201 stash draft_id={draft_id} -> 202 submit story_id={story_id}"
                )
                successes += 1
            else:
                print(
                    f"[{index:>3}/{len(filtered)}] {simulation_id} -> "
                    f"{status_code} ERROR detail={detail}"
                )
                failures.append(simulation_id)
        except Exception as exc:  # noqa: BLE001
            print(f"[{index:>3}/{len(filtered)}] {simulation_id} -> EXCEPTION {exc}")
            failures.append(simulation_id)

    print()
    print("Summary:")
    print(f"  Total:   {len(filtered)}")
    print(f"  Success: {successes}")
    print(f"  Failed:  {len(failures)}")
    if failures:
        print(f"  Failed IDs: {', '.join(failures)}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
