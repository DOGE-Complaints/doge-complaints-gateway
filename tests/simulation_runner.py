"""Remote simulation runner for DOGEstonia intake API."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SRC = _REPO_ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.intake import INTAKE_SCHEMA_VERSION

from simulation_intake_http import (
    format_submit_failure,
    post_stash_and_submit_http,
    resolve_user_bearer_token,
)


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
        description_i18n[lang_key] = dv.strip() if isinstance(dv, str) and dv.strip() else original_text

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


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run remote simulation canvas.")
    parser.add_argument("--max", dest="max_stories", type=int, default=None)
    parser.add_argument("--groups", type=str, default=None)
    return parser.parse_args()


def main() -> int:
    _load_env()
    args = _parse_args()

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
