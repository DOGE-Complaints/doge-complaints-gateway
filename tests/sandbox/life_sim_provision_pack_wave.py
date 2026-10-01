#!/usr/bin/env python3
"""GW-REQ11-08 — operator pack-wave provision CLI (clean entry).

Reads pack users.json (LIFE_SIM_PACK_DIR); never writes provision status there.
Wave-state JSON under pack/waves/<wave_id>/state.json.
Modes: skip (default) | wipe-fixture-users (+ confirm).
Reuse REQ11-05 auth path (file OTP only). Never invent GET /dev/last-otp.
Never commit .secrets/.

Usage (from doge-complaints-gateway/):
  LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<id> \\
    .venv/bin/python tests/sandbox/life_sim_provision_pack_wave.py --limit 2
  make life-sim-provision-pack-wave LIMIT=2 PACK_DIR=...
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

_SANDBOX = Path(__file__).resolve().parent
_TESTS = _SANDBOX.parent
_GATEWAY_ROOT = _TESTS.parent

if str(_SANDBOX) not in sys.path:
    sys.path.insert(0, str(_SANDBOX))
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

import life_sim_provision_config as cfg  # noqa: E402
import life_sim_provision_lib as lib  # noqa: E402
import life_sim_provision_users as provision  # noqa: E402
import life_sim_replay_lib as life_sim  # noqa: E402
from life_sim_wave_store import WaveStore  # noqa: E402

# File-mode default pace (P3 lock): not required to be 65s (Telnyx cooldown).
DEFAULT_FILE_PACE_S = 5.0


def _resolve_pack_dir(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_absolute():
            path = (_GATEWAY_ROOT / path).resolve()
        else:
            path = path.resolve()
    else:
        pack = life_sim.resolve_life_sim_pack_dir()
        if pack is None:
            raise SystemExit(
                "LIFE_SIM_PACK_DIR not set (or pass --pack-dir). "
                "Pack users.json is the SSOT input."
            )
        path = pack
    users = path / "users.json"
    if not users.is_file():
        raise SystemExit(f"pack users.json missing: {users}")
    return path


def _load_pack_users(pack_dir: Path) -> list[dict[str, Any]]:
    """Read-only load of pack users.json (never write back)."""
    return life_sim.load_life_sim_users(pack_dir / "users.json")


def _assert_never_write_users_json(pack_dir: Path, before_mtime: float | None) -> None:
    users = pack_dir / "users.json"
    if before_mtime is None:
        return
    after = users.stat().st_mtime if users.is_file() else None
    if after is not None and after != before_mtime:
        raise RuntimeError(
            f"REFUSAL: pack users.json mtime changed during run ({users}). "
            "Provision must never write fixture status into users.json."
        )


def _admin_list_users(*, supabase_url: str, service_role: str) -> list[dict[str, Any]]:
    headers = {
        "apikey": service_role,
        "Authorization": f"Bearer {service_role}",
    }
    users: list[dict[str, Any]] = []
    page = 1
    while page <= 50:
        list_url = (
            f"{supabase_url.rstrip('/')}/auth/v1/admin/users?"
            f"{urlencode({'page': str(page), 'per_page': '200'})}"
        )
        status, listed = provision._http_json("GET", list_url, headers=headers)
        if status != 200:
            raise RuntimeError(f"admin list users HTTP {status}: {listed!r}"[:400])
        batch: list[Any] = []
        if isinstance(listed, dict):
            raw = listed.get("users")
            if isinstance(raw, list):
                batch = raw
        if not batch:
            break
        for item in batch:
            if isinstance(item, dict):
                users.append(item)
        if len(batch) < 200:
            break
        page += 1
    return users


def wipe_fixture_auth_users(
    fixture_users: list[dict[str, Any]],
    *,
    supabase_url: str,
    service_role: str,
    dry_run: bool,
) -> dict[str, Any]:
    """Delete only Auth users whose email/phone derive from this fixture pack.

    Does NOT wipe gateway content (REQ11-06). Does NOT delete non-fixture admins.
    """
    allowed_emails = {
        lib.derive_email(str(u["fixture_user_id"])).lower() for u in fixture_users
    }
    allowed_phones = {
        lib.derive_phone_e164(str(u["fixture_user_id"])) for u in fixture_users
    }
    listed = _admin_list_users(supabase_url=supabase_url, service_role=service_role)
    targets: list[tuple[str, str]] = []
    for item in listed:
        email = str(item.get("email") or "").lower()
        phone = str(item.get("phone") or "")
        uid = str(item.get("id") or "").strip()
        if not uid:
            continue
        if email in allowed_emails or (phone and phone in allowed_phones):
            targets.append((uid, email or phone))

    report: dict[str, Any] = {
        "listed": len(listed),
        "matched_fixture": len(targets),
        "deleted": 0,
        "dry_run": dry_run,
        "emails_sample": [e for _, e in targets[:5]],
    }
    if dry_run:
        return report

    headers = {
        "apikey": service_role,
        "Authorization": f"Bearer {service_role}",
    }
    for uid, _label in targets:
        status, payload = provision._http_json(
            "DELETE",
            f"{supabase_url.rstrip('/')}/auth/v1/admin/users/{uid}",
            headers=headers,
        )
        if status not in (200, 204):
            raise RuntimeError(
                f"admin delete user {uid} HTTP {status}: {payload!r}"[:400]
            )
        report["deleted"] += 1
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Pack-wave provision life-sim users (REQ11-08)"
    )
    parser.add_argument(
        "--pack-dir",
        type=str,
        default=None,
        help="Pack root with users.json (else LIFE_SIM_PACK_DIR)",
    )
    parser.add_argument(
        "--wave-id",
        type=str,
        default=None,
        help="Wave id under pack/waves/<id>/state.json (default: UTC compact)",
    )
    parser.add_argument("--limit", type=int, default=None, help="First N users only")
    parser.add_argument(
        "--mode",
        choices=("skip", "wipe-fixture-users"),
        default=os.getenv("LIFE_SIM_PACK_WAVE_MODE", "skip") or "skip",
        help="skip (default) or wipe-fixture-users before provision",
    )
    parser.add_argument(
        "--confirm-wipe-fixture-users",
        action="store_true",
        help="Required with --mode wipe-fixture-users (or LIFE_SIM_WIPE_FIXTURE_USERS=1)",
    )
    parser.add_argument(
        "--pace-s",
        type=float,
        default=float(
            os.getenv("LIFE_SIM_PROVISION_PACE_S", str(DEFAULT_FILE_PACE_S))
            or str(DEFAULT_FILE_PACE_S)
        ),
        help=f"Sleep after live phone OTP (default file-mode {DEFAULT_FILE_PACE_S}s)",
    )
    parser.add_argument("--otp-wait-s", type=float, default=5.0)
    parser.add_argument(
        "--generation-id",
        type=str,
        default=None,
        help="Secrets generation id under .secrets/ (gitignored)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Derive + wave checkpoint only (no Auth HTTP); still fail-closed on config if checked",
    )
    parser.add_argument(
        "--skip-config-check",
        action="store_true",
        help=argparse.SUPPRESS,  # tests only
    )
    args = parser.parse_args(argv)

    pack_dir = _resolve_pack_dir(args.pack_dir)
    os.environ["LIFE_SIM_PACK_DIR"] = str(pack_dir)
    users_path = pack_dir / "users.json"
    users_mtime = users_path.stat().st_mtime

    users = _load_pack_users(pack_dir)
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be >= 1")
        users = users[: args.limit]

    live = not args.dry_run
    pack_cfg: cfg.PackWaveConfig | None = None
    if not args.skip_config_check:
        cfg.assert_email_domain(cfg.EMAIL_DOMAIN)
        if live:
            pack_cfg = cfg.resolve_pack_wave_config(skip_live_auth=False)
        else:
            # Dry-run: domain only (no Auth/OTP). Live always fail-closed on file SMS.
            cfg.load_gateway_and_identity_env()

    wave_id = args.wave_id or lib.new_generation_id()
    fixture_ids = [str(u["fixture_user_id"]) for u in users]
    wave = WaveStore.load_or_create(pack_dir, wave_id, fixture_user_ids=fixture_ids)

    wipe_confirmed = args.confirm_wipe_fixture_users or (
        os.getenv("LIFE_SIM_WIPE_FIXTURE_USERS", "").strip() == "1"
    )
    if args.mode == "wipe-fixture-users":
        if not wipe_confirmed:
            print(
                "REFUSAL: --mode wipe-fixture-users requires "
                "--confirm-wipe-fixture-users or LIFE_SIM_WIPE_FIXTURE_USERS=1. "
                "Wipes only fixture-derived Auth users (not REQ11-06 content).",
                file=sys.stderr,
            )
            return 2
        if live:
            assert pack_cfg is not None
            print("Wipe fixture Auth users (Identity Supabase only)…")
            report = wipe_fixture_auth_users(
                users,
                supabase_url=pack_cfg.supabase_url,
                service_role=pack_cfg.service_role,
                dry_run=False,
            )
            print(
                f"  listed={report['listed']} matched={report['matched_fixture']} "
                f"deleted={report['deleted']}"
            )
            # Reset wave entries for this cohort so resume re-provisions.
            for fid in fixture_ids:
                wave.set_status(fid, "pending", checkpoint=False)
            wave.checkpoint()
        else:
            print("Dry-run: would wipe fixture Auth users (skipped HTTP)")

    generation_id = args.generation_id or lib.new_generation_id()
    out_path = lib.secrets_path_for_generation(generation_id)

    existing_by_id: dict[str, dict[str, Any]] = {}
    latest = lib.discover_latest_creds_path()
    if latest is not None:
        try:
            existing_by_id = lib.index_creds_by_fixture_user_id(lib.load_users_creds(latest))
        except (OSError, RuntimeError, ValueError):
            existing_by_id = {}

    work_ids = set(wave.users_needing_work(fixture_ids))
    print("DOGEstonia life-sim pack-wave provision (REQ11-08)")
    print(f"Pack: {pack_dir}")
    print(f"Users in scope: {len(users)} (resume skip verified → work {len(work_ids)})")
    print(f"Wave: {wave_id} → {wave.path}")
    print(f"Mode: {args.mode}")
    print(f"Secrets out: {out_path} (gitignored)")
    print(f"Email domain: @{cfg.EMAIL_DOMAIN}")
    if pack_cfg:
        print(f"Identity: {pack_cfg.identity_url}")
        host = pack_cfg.supabase_url.split('//', 1)[-1].split('/', 1)[0]
        print(f"Auth Supabase host (Identity): {host}")
        print(f"SMS_PROVIDER={pack_cfg.sms_provider} outbox={pack_cfg.outbox_dir}")
    print(f"Pace: {args.pace_s}s after file OTP")
    if args.dry_run:
        print("Mode: DRY-RUN (no Auth HTTP)")
    print()

    entries: list[dict[str, Any]] = []
    # Preserve prior verified secrets when doing a live partial refresh.
    if live and existing_by_id:
        for fid, ent in existing_by_id.items():
            if fid not in work_ids and ent.get("phone_verified") is True:
                entries.append(ent)

    failures: list[str] = []
    for i, user in enumerate(users):
        fid = str(user["fixture_user_id"])
        if wave.is_verified(fid) and args.mode == "skip":
            print(f"[{i+1:>4}/{len(users)}] {fid} skip (wave=verified)")
            continue

        did_phone_otp = False
        try:
            if args.dry_run:
                email = lib.derive_email(fid)
                phone = lib.derive_phone_e164(fid)
                entry = {
                    "fixture_user_id": fid,
                    "email": email,
                    "phone_e164": phone,
                    "created_at_utc": lib.utc_now_iso(),
                    "status": "dry-run",
                    "generation_id": generation_id,
                }
                wave.set_status(fid, "created")
                print(
                    f"[{i+1:>4}/{len(users)}] {fid} dry-run "
                    f"email={email} phone={phone}"
                )
            else:
                assert pack_cfg is not None
                # Identity reachability once
                if i == 0:
                    st, _ = provision._http_json(
                        "GET", f"{pack_cfg.identity_url}/ready", timeout=5.0
                    )
                    if st != 200:
                        st, _ = provision._http_json(
                            "GET", f"{pack_cfg.identity_url}/health", timeout=5.0
                        )
                    if st != 200:
                        print(
                            f"OPERATOR BLOCKER: Identity unreachable "
                            f"{pack_cfg.identity_url} HTTP {st}",
                            file=sys.stderr,
                        )
                        return 2

                entry = provision.provision_one(
                    user,
                    supabase_url=pack_cfg.supabase_url,
                    anon_key=pack_cfg.anon_key,
                    service_role=pack_cfg.service_role,
                    identity_url=pack_cfg.identity_url,
                    outbox_dir=pack_cfg.outbox_dir,
                    existing=existing_by_id.get(fid),
                    dry_run=False,
                    otp_wait_s=args.otp_wait_s,
                )
                entry["generation_id"] = generation_id
                if entry.get("phone_verified") is True:
                    wave.set_status(fid, "verified")
                else:
                    wave.set_status(fid, "created")
                entries.append(entry)
                doc = lib.build_creds_document(
                    generation_id=generation_id, entries=entries
                )
                lib.write_creds_document(out_path, doc)
                did_phone_otp = entry.get("verify") == "file_otp_confirmed"
                print(
                    f"[{i+1:>4}/{len(users)}] {fid} "
                    f"email={entry['email']} phone={entry['phone_e164']} "
                    f"verified={entry.get('phone_verified')} "
                    f"via={entry.get('verify', 'ok')} wave={wave.get_status(fid)}"
                )
        except Exception as exc:  # noqa: BLE001
            failures.append(fid)
            wave.set_status(fid, "failed", error=str(exc)[:400])
            print(f"[{i+1:>4}/{len(users)}] {fid} -> ERROR {exc}", file=sys.stderr)

        if (
            i + 1 < len(users)
            and live
            and args.pace_s > 0
            and did_phone_otp
        ):
            time.sleep(args.pace_s)

    if live and entries:
        doc = lib.build_creds_document(generation_id=generation_id, entries=entries)
        lib.write_creds_document(out_path, doc)
        print()
        print(f"Wrote {len(entries)} secret entries → {out_path}")

    _assert_never_write_users_json(pack_dir, users_mtime)
    print(f"Wave state → {wave.path}")
    print(f"Failed: {len(failures)}")
    if failures:
        print("Failed IDs: " + ", ".join(failures[:20]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
