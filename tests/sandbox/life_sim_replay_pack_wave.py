#!/usr/bin/env python3
"""GW-REQ11-10 — operator pack-wave replay жалоб CLI.

Reads pack stories.json (LIFE_SIM_PACK_DIR required); never writes status there.
Wave-state JSON under pack/waves/<wave_id>/replay_state.json.
Reuses life_sim_replay_lib + simulation_runner stash→submit path.
Actors = secrets Bearer by fixture_user_id; fail-closed if missing.
No invent intake APIs / force-cluster.

Usage (from doge-complaints-gateway/):
  LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<id> \\
    .venv/bin/python tests/sandbox/life_sim_replay_pack_wave.py --limit 2
  make life-sim-replay-pack-wave LIMIT=2
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

_SANDBOX = Path(__file__).resolve().parent
_TESTS = _SANDBOX.parent
_GATEWAY_ROOT = _TESTS.parent
_PROFILES = _SANDBOX / "profiles"
_SRC = _GATEWAY_ROOT / "src"

if str(_SANDBOX) not in sys.path:
    sys.path.insert(0, str(_SANDBOX))
if str(_PROFILES) not in sys.path:
    sys.path.insert(0, str(_PROFILES))
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import demo_life_sim_profiles as profiles  # noqa: E402
import life_sim_replay_lib as life_sim  # noqa: E402
from life_sim_replay_wave_store import ReplayWaveStore  # noqa: E402


def _resolve_pack_dir(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_absolute():
            path = (_GATEWAY_ROOT / path).resolve()
        else:
            path = path.resolve()
        stories = path / "stories.json"
        if not stories.is_file():
            raise SystemExit(2)
        return path
    try:
        return life_sim.require_life_sim_pack_dir(require_stories=True)
    except RuntimeError as exc:
        raise SystemExit(2) from exc


def _assert_never_write_stories_json(pack_dir: Path, before_mtime: float | None) -> None:
    stories = pack_dir / "stories.json"
    if before_mtime is None:
        return
    after = stories.stat().st_mtime if stories.is_file() else None
    if after is not None and after != before_mtime:
        raise RuntimeError(
            f"REFUSAL: pack stories.json mtime changed during run ({stories}). "
            "Replay must never write fixture status into stories.json."
        )


def _load_env() -> None:
    """Load gateway .env / .env.test like simulation_runner (no secrets committed)."""
    for name in (".env", ".env.test"):
        path = _GATEWAY_ROOT / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            raw = line.strip()
            if not raw or raw.startswith("#") or "=" not in raw:
                continue
            key, _, value = raw.partition("=")
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env {name}")
    return value


def _gateway_url_from_profile(profile: dict[str, Any]) -> str:
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
    token = os.getenv(token_env, "").strip()
    if token:
        return token
    # Local .env often uses SERVICE_API_TOKEN for service-auth stash.
    fallback = os.getenv("SERVICE_API_TOKEN", "").strip()
    if fallback:
        return fallback
    return _required_env(token_env)


def _preflight_missing_creds(
    stories: list[dict[str, Any]],
    creds_index: dict[str, dict[str, Any]],
) -> None:
    missing: list[str] = []
    for story in stories:
        fid = str(story.get("fixture_user_id") or "").strip()
        if not fid:
            raise RuntimeError(
                f"story {story.get('fixture_story_id')!r} missing fixture_user_id"
            )
        entry = creds_index.get(fid)
        if entry is None or not str(entry.get("email") or "").strip() or not str(
            entry.get("password") or ""
        ):
            if fid not in missing:
                missing.append(fid)
    if missing:
        preview = ", ".join(missing[:20])
        suffix = "..." if len(missing) > 20 else ""
        raise SystemExit(
            f"Fail-closed: missing secrets for {len(missing)} fixture_user_id(s): "
            f"{preview}{suffix}. Run make life-sim-provision-pack-wave first."
        )


def run_wave(args: argparse.Namespace) -> int:
    pack_dir = _resolve_pack_dir(args.pack_dir)
    os.environ["LIFE_SIM_PACK_DIR"] = str(pack_dir)

    stories_path = pack_dir / "stories.json"
    before_mtime = stories_path.stat().st_mtime
    stories = life_sim.load_life_sim_stories(stories_path)
    # Scale assert when meta present (pack-wave SSOT); soft if meta Absent.
    meta_path = pack_dir / "meta.json"
    if meta_path.is_file() and (pack_dir / "users.json").is_file():
        life_sim.assert_fixture_scale(
            users=life_sim.load_life_sim_users(pack_dir / "users.json"),
            stories=stories,
            meta=life_sim.load_life_sim_meta(meta_path),
        )

    story_ids = [str(s.get("fixture_story_id") or f"idx-{i}") for i, s in enumerate(stories, 1)]
    wave_id = (args.wave_id or os.getenv("WAVE_ID", "") or "replay-default").strip()
    wave = ReplayWaveStore.load_or_create(
        pack_dir, wave_id, fixture_story_ids=story_ids
    )

    by_id = {
        str(s.get("fixture_story_id") or f"idx-{i}"): s
        for i, s in enumerate(stories, 1)
    }
    need_ids = wave.stories_needing_work(story_ids)
    selected_ids = need_ids if args.limit is None else need_ids[: max(0, args.limit)]
    selected = [by_id[sid] for sid in selected_ids if sid in by_id]

    profile = profiles.select_profile(args.profile)
    dry_run = bool(args.dry_run)

    creds_index: dict[str, dict[str, Any]] = {}
    if not dry_run:
        try:
            creds_index = life_sim.load_users_creds_index()
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc
        _preflight_missing_creds(selected, creds_index)

    print("DOGEstonia Life-Sim Pack-Wave Replay (REQ11-10)")
    print(f"Pack: {pack_dir}")
    print(f"Wave: {wave_id} → {wave.path}")
    print(f"Stories on disk: {len(stories)}; needing work: {len(need_ids)}; selected: {len(selected)}")
    print(f"Profile: {profile['profile_id']}")
    if dry_run:
        print("Mode: DRY-RUN (no HTTP; no wave submitted marks)")
    print()

    if not selected:
        print("Nothing to do (all selected already submitted or limit=0).")
        _assert_never_write_stories_json(pack_dir, before_mtime)
        return 0

    # Reuse simulation_runner HTTP helpers (Present REQ11-03 path).
    import simulation_runner as runner  # noqa: WPS433

    if not dry_run:
        runner._force_identity_supabase_auth_env()  # noqa: SLF001
        if not os.getenv("GATEWAY_API_TOKEN", "").strip() and os.getenv(
            "SERVICE_API_TOKEN", ""
        ).strip():
            os.environ["GATEWAY_API_TOKEN"] = os.environ["SERVICE_API_TOKEN"]

    from gw_ssr_16_node_schema import active_node_schema_binding

    schema_binding = active_node_schema_binding()
    gateway_url = _gateway_url_from_profile(profile)
    service_token = "" if dry_run else _service_token_from_profile(profile)
    location_query = (
        args.location_query or os.getenv("LIFE_SIM_LOCATION_QUERY", "")
    ).strip() or None

    successes = 0
    failures: list[str] = []

    for index, story in enumerate(selected, start=1):
        fixture_story_id = str(story.get("fixture_story_id") or f"idx-{index}")
        fixture_user_id = str(story["fixture_user_id"])
        fixture_created_at = str(story.get("created_at") or "").strip()
        try:
            payload = life_sim.life_sim_story_to_intake_payload(
                story,
                intake_schema_version=runner.INTAKE_SCHEMA_VERSION,
                schema_binding=schema_binding,
                location_query=location_query,
            )
            if dry_run:
                print(
                    f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                    f"user={fixture_user_id} -> DRY-RUN ok"
                )
                successes += 1
                continue

            entry = creds_index.get(fixture_user_id)
            if entry is None:
                raise RuntimeError(f"No secrets entry for {fixture_user_id}")
            user_token = runner.resolve_fixture_user_bearer_token(
                fixture_user_id,
                email=str(entry["email"]),
                password=str(entry["password"]),
            )
            ok, status_code, detail, draft_id, story_id = (
                runner.run_life_sim_payload_stash_submit(
                    gateway_url=gateway_url,
                    service_token=service_token,
                    user_token=user_token,
                    payload=payload,
                )
            )
            if not ok:
                wave.set_status(
                    fixture_story_id,
                    "failed",
                    error=f"submit {status_code}: {detail}"[:400],
                )
                print(
                    f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                    f"-> {status_code} ERROR detail={detail}"
                )
                failures.append(fixture_story_id)
                continue

            backdate_note = "skip-no-fixture-created_at"
            if fixture_created_at and story_id and story_id != "n/a":
                bd_status, bd_text = runner.patch_story_created_at_http(
                    gateway_url=gateway_url,
                    service_token=service_token,
                    story_id=story_id,
                    created_at=fixture_created_at,
                )
                if bd_status == 200:
                    backdate_note = f"backdate=200 created_at={fixture_created_at}"
                else:
                    wave.set_status(
                        fixture_story_id,
                        "failed",
                        error=f"backdate {bd_status}: {bd_text.strip()[:200]}",
                        gateway_story_id=story_id,
                    )
                    failures.append(fixture_story_id)
                    print(
                        f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                        f"-> submit ok story_id={story_id} "
                        f"-> PATCH created-at {bd_status} ERROR"
                    )
                    continue

            wave.set_status(
                fixture_story_id,
                "submitted",
                gateway_story_id=story_id if story_id != "n/a" else None,
            )
            print(
                f"[{index:>4}/{len(selected)}] {fixture_story_id} "
                f"-> draft={draft_id} story={story_id} -> {backdate_note} -> wave=submitted"
            )
            successes += 1
        except Exception as exc:  # noqa: BLE001
            wave.set_status(fixture_story_id, "failed", error=str(exc)[:400])
            print(f"[{index:>4}/{len(selected)}] {fixture_story_id} -> EXCEPTION {exc}")
            failures.append(fixture_story_id)

    _assert_never_write_stories_json(pack_dir, before_mtime)

    print()
    print("Summary:")
    print(f"  Selected: {len(selected)}")
    print(f"  Success:  {successes}")
    print(f"  Failed:   {len(failures)}")
    print(f"  Wave:     {wave.path}")
    if failures:
        preview = ", ".join(failures[:20])
        suffix = "..." if len(failures) > 20 else ""
        print(f"  Failed IDs: {preview}{suffix}")
        return 1
    return 0


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="REQ11-10 pack-wave replay жалоб (fail-closed LIFE_SIM_PACK_DIR)."
    )
    parser.add_argument(
        "--pack-dir",
        type=str,
        default=None,
        help="Pack root with stories.json (else LIFE_SIM_PACK_DIR / PACK_DIR)",
    )
    parser.add_argument(
        "--wave-id",
        type=str,
        default=None,
        help="Wave id under pack/waves/<id>/replay_state.json (default: WAVE_ID or replay-default)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Max complaints to process this run (after resume filter)",
    )
    parser.add_argument(
        "--profile",
        type=str,
        default=None,
        help="DEMO_LIFE_SIM_PROFILE id",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build payloads only; no HTTP; do not mark submitted",
    )
    parser.add_argument(
        "--location-query",
        type=str,
        default=None,
        help="Optional narrative.location_query for all stories",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _load_env()
    args = _parse_args(argv)
    try:
        return run_wave(args)
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        if isinstance(code, int):
            return code
        print(str(code), file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"FATAL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
