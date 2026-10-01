#!/usr/bin/env python3
"""GW-REQ11-05 — provision 200 life-sim fixture users (Supabase + Identity file OTP).

Usage (from doge-complaints-gateway/):
  .venv/bin/python tests/sandbox/life_sim_provision_users.py --limit 2
  make life-sim-provision-users LIMIT=2

Preconditions:
  - SUPABASE_URL + SUPABASE_ANON_KEY
  - Identity up with SMS_PROVIDER=file (APP_PROFILE ≠ pilot)
  - FILE_SMS_OUTBOX_DIR / LIFE_SIM_FILE_SMS_OUTBOX_DIR readable
Never invent GET /dev/last-otp. Never commit .secrets/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request

_SANDBOX = Path(__file__).resolve().parent
_TESTS = _SANDBOX.parent
_GATEWAY_ROOT = _TESTS.parent
_REPO_MONOREPO = _GATEWAY_ROOT.parent

if str(_SANDBOX) not in sys.path:
    sys.path.insert(0, str(_SANDBOX))
if str(_TESTS) not in sys.path:
    sys.path.insert(0, str(_TESTS))

import life_sim_provision_lib as lib  # noqa: E402
import life_sim_replay_lib as life_sim  # noqa: E402


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        # Strip inline comments for simple KEY=value # comment forms.
        if " #" in line:
            line = line.split(" #", 1)[0].rstrip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def _load_env() -> None:
    _load_env_file(_GATEWAY_ROOT / ".env.test")
    _load_env_file(_GATEWAY_ROOT / ".env")
    _load_env_file(_REPO_MONOREPO / "doge-identity-service" / ".env")


def _force_identity_supabase_auth_env() -> None:
    """Auth users must live in Identity's Supabase (JWT iss/JWKS), not gateway content DB.

    Gateway `.env` often points at a different project; load-order keeps gateway first.
    Re-apply Identity SUPABASE_* so signup/login tokens validate on GET /me.
    """
    path = _REPO_MONOREPO / "doge-identity-service" / ".env"
    if not path.is_file():
        return
    wanted = (
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE",
        "SUPABASE_JWT_SECRET",
        "SUPABASE_JWKS_URL",
    )
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if " #" in line:
            line = line.split(" #", 1)[0].rstrip()
        key, value = line.split("=", 1)
        key = key.strip()
        if key not in wanted:
            continue
        value = value.strip().strip('"').strip("'")
        if value:
            os.environ[key] = value


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env variable: {name}")
    return value


def _identity_base_url() -> str:
    explicit = os.getenv("LIFE_SIM_IDENTITY_URL", "").strip() or os.getenv(
        "IDENTITY_URL", ""
    ).strip()
    if explicit:
        return explicit.rstrip("/")
    # Profile local default (REQ11-02).
    return "http://127.0.0.1:8100"


def _outbox_dir() -> Path:
    raw = (
        os.getenv("LIFE_SIM_FILE_SMS_OUTBOX_DIR", "").strip()
        or os.getenv("FILE_SMS_OUTBOX_DIR", "").strip()
    )
    if raw:
        # Strip leftover inline comment if env loader left it.
        if " #" in raw:
            raw = raw.split(" #", 1)[0].strip()
        p = Path(raw)
        if not p.is_absolute():
            p = (_REPO_MONOREPO / "doge-identity-service" / p).resolve()
        return p
    return (_REPO_MONOREPO / "doge-identity-service" / "var" / "sms-outbox").resolve()


def _http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    body: dict[str, Any] | None = None,
    timeout: float = 45.0,
) -> tuple[int, dict[str, Any] | list[Any] | str]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    hdrs = {"Content-Type": "application/json", **(headers or {})}
    req = request.Request(url=url, data=data, method=method, headers=hdrs)
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            status = int(resp.status)
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8") if exc.fp else str(exc)
        status = int(exc.code)
    except error.URLError as exc:
        raise RuntimeError(f"HTTP {method} {url} failed: {exc.reason}") from exc
    if not raw.strip():
        return status, {}
    try:
        parsed: dict[str, Any] | list[Any] = json.loads(raw)
        return status, parsed
    except json.JSONDecodeError:
        return status, raw


def supabase_signup(*, email: str, password: str, supabase_url: str, anon_key: str) -> str | None:
    """Sign up; return access_token if present (confirm-email may omit it)."""
    base = supabase_url.rstrip("/")
    url = f"{base}/auth/v1/signup"
    status, payload = _http_json(
        "POST",
        url,
        headers={"apikey": anon_key},
        body={"email": email, "password": password},
    )
    if status not in (200, 201):
        detail = payload if isinstance(payload, str) else json.dumps(payload)[:300]
        # User already registered — caller may password-grant.
        if status == 422 or (
            isinstance(payload, dict)
            and "already" in json.dumps(payload).lower()
        ):
            return None
        if status == 429:
            raise RuntimeError(
                f"Supabase signup rate-limited (HTTP 429): {detail}. "
                "Operator blocker — wait and retry; do not invent OTP HTTP."
            )
        raise RuntimeError(f"Supabase signup HTTP {status}: {detail}")
    if isinstance(payload, dict):
        token = payload.get("access_token")
        if isinstance(token, str) and token.strip():
            return token.strip()
        # Nested session (newer GoTrue shapes)
        session = payload.get("session")
        if isinstance(session, dict):
            token2 = session.get("access_token")
            if isinstance(token2, str) and token2.strip():
                return token2.strip()
    return None


def supabase_password_grant(
    *, email: str, password: str, supabase_url: str, anon_key: str
) -> str:
    from simulation_intake_http import fetch_supabase_access_token

    return fetch_supabase_access_token(
        email=email,
        password=password,
        supabase_url=supabase_url,
        anon_key=anon_key,
    )


def supabase_admin_ensure_confirmed(
    *,
    email: str,
    password: str,
    supabase_url: str,
    service_role: str,
) -> str:
    """Create or update Auth user with email_confirm=true (demo automation).

    Prefer confirm-email off in Supabase; this path unblocks email_not_confirmed
    without inventing OTP HTTP. Uses SUPABASE_SERVICE_ROLE only.
    """
    from urllib.parse import urlencode

    base = supabase_url.rstrip("/")
    headers = {
        "apikey": service_role,
        "Authorization": f"Bearer {service_role}",
    }
    status, payload = _http_json(
        "POST",
        f"{base}/auth/v1/admin/users",
        headers=headers,
        body={
            "email": email,
            "password": password,
            "email_confirm": True,
        },
    )
    if status in (200, 201):
        return "created"

    detail = payload if isinstance(payload, str) else json.dumps(payload)[:400]
    already = status in (422, 400) or "already" in detail.lower()
    if not already:
        raise RuntimeError(f"Supabase admin create user HTTP {status}: {detail}")

    # Locate existing user by email, then force confirm + password for this run.
    list_url = f"{base}/auth/v1/admin/users?{urlencode({'page': '1', 'per_page': '200'})}"
    status_l, listed = _http_json("GET", list_url, headers=headers)
    if status_l != 200:
        raise RuntimeError(
            f"Supabase admin list users HTTP {status_l}: {listed!r}"[:400]
        )
    users: list[Any] = []
    if isinstance(listed, dict):
        raw_users = listed.get("users")
        if isinstance(raw_users, list):
            users = raw_users
    uid: str | None = None
    email_l = email.lower()
    for item in users:
        if not isinstance(item, dict):
            continue
        if str(item.get("email") or "").lower() == email_l:
            cand = item.get("id")
            if isinstance(cand, str) and cand.strip():
                uid = cand.strip()
                break
    if uid is None:
        raise RuntimeError(
            f"Supabase admin: user exists but id not found for {email!r} "
            f"(listed={len(users)}; may need higher per_page)"
        )
    status_u, updated = _http_json(
        "PUT",
        f"{base}/auth/v1/admin/users/{uid}",
        headers=headers,
        body={"email_confirm": True, "password": password},
    )
    if status_u not in (200, 201):
        raise RuntimeError(
            f"Supabase admin confirm/update HTTP {status_u}: {updated!r}"[:400]
        )
    return "updated"


def identity_get_me(*, identity_url: str, bearer: str) -> dict[str, Any]:
    status, payload = _http_json(
        "GET",
        f"{identity_url.rstrip('/')}/me",
        headers={"Authorization": f"Bearer {bearer}"},
    )
    if status != 200 or not isinstance(payload, dict):
        raise RuntimeError(f"GET /me failed HTTP {status}: {payload!r}"[:400])
    data = payload.get("data") if isinstance(payload.get("data"), dict) else payload
    if not isinstance(data, dict):
        raise RuntimeError("GET /me response missing data object")
    return data


def identity_phone_request(*, identity_url: str, bearer: str, phone: str) -> None:
    status, payload = _http_json(
        "POST",
        f"{identity_url.rstrip('/')}/auth/phone/request",
        headers={"Authorization": f"Bearer {bearer}"},
        body={"phone": phone},
    )
    if status != 200:
        raise RuntimeError(f"phone/request HTTP {status}: {payload!r}"[:400])


def identity_phone_confirm(
    *, identity_url: str, bearer: str, phone: str, code: str
) -> None:
    status, payload = _http_json(
        "POST",
        f"{identity_url.rstrip('/')}/auth/phone/confirm",
        headers={"Authorization": f"Bearer {bearer}"},
        body={"phone": phone, "code": code},
    )
    if status != 200:
        raise RuntimeError(f"phone/confirm HTTP {status}: {payload!r}"[:400])


def provision_one(
    user: dict[str, Any],
    *,
    supabase_url: str,
    anon_key: str,
    service_role: str,
    identity_url: str,
    outbox_dir: Path,
    existing: dict[str, Any] | None,
    dry_run: bool,
    otp_wait_s: float,
) -> dict[str, Any]:
    fid = str(user["fixture_user_id"])
    email = lib.derive_email(fid)
    phone = lib.derive_phone_e164(fid)
    if existing and existing.get("email") == email and existing.get("password"):
        password = str(existing["password"])
    else:
        password = lib.generate_password()

    entry = {
        "fixture_user_id": fid,
        "email": email,
        "password": password,
        "phone_e164": phone,
        "created_at_utc": lib.utc_now_iso(),
    }

    if dry_run:
        entry["status"] = "dry-run"
        return entry

    # Admin create/confirm avoids email_not_confirmed when Confirm email is on.
    entry["admin_auth"] = supabase_admin_ensure_confirmed(
        email=email,
        password=password,
        supabase_url=supabase_url,
        service_role=service_role,
    )
    bearer = supabase_password_grant(
        email=email, password=password, supabase_url=supabase_url, anon_key=anon_key
    )
    entry["signup"] = "admin_confirmed_login"

    me = identity_get_me(identity_url=identity_url, bearer=bearer)
    if me.get("phone_verified") is True:
        entry["phone_verified"] = True
        entry["verify"] = "already_verified"
        return entry

    identity_phone_request(identity_url=identity_url, bearer=bearer, phone=phone)
    code = lib.read_latest_otp_from_outbox(outbox_dir, phone, wait_s=otp_wait_s)
    identity_phone_confirm(
        identity_url=identity_url, bearer=bearer, phone=phone, code=code
    )
    me2 = identity_get_me(identity_url=identity_url, bearer=bearer)
    if me2.get("phone_verified") is not True:
        raise RuntimeError(f"phone_verified still false after confirm for {fid}")
    entry["phone_verified"] = True
    entry["verify"] = "file_otp_confirmed"
    return entry


def main(argv: list[str] | None = None) -> int:
    _load_env()
    _force_identity_supabase_auth_env()
    parser = argparse.ArgumentParser(description="Provision life-sim fixture users (REQ11-05)")
    parser.add_argument("--limit", type=int, default=None, help="Provision only first N users")
    parser.add_argument(
        "--generation-id",
        type=str,
        default=None,
        help="Secrets generation id (default: UTC compact)",
    )
    parser.add_argument(
        "--pace-s",
        type=float,
        default=float(os.getenv("LIFE_SIM_PROVISION_PACE_S", "65") or "65"),
        help="Sleep between phone/request calls (rate-limit / resend cooldown)",
    )
    parser.add_argument(
        "--otp-wait-s",
        type=float,
        default=5.0,
        help="Max wait for OTP line to appear in file outbox",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Derive email/phone/password + write secrets only (no HTTP)",
    )
    parser.add_argument(
        "--creds-in",
        type=str,
        default=None,
        help="Optional existing secrets file to refresh/reuse passwords",
    )
    args = parser.parse_args(argv)

    users = life_sim.load_life_sim_users()
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be >= 1")
        users = users[: args.limit]

    generation_id = args.generation_id or lib.new_generation_id()
    out_path = lib.secrets_path_for_generation(generation_id)

    existing_by_id: dict[str, dict[str, Any]] = {}
    if args.creds_in:
        existing_doc = lib.load_users_creds(Path(args.creds_in))
        existing_by_id = lib.index_creds_by_fixture_user_id(existing_doc)
    else:
        latest = lib.discover_latest_creds_path()
        if latest is not None:
            try:
                existing_by_id = lib.index_creds_by_fixture_user_id(lib.load_users_creds(latest))
            except (OSError, RuntimeError, ValueError):
                existing_by_id = {}

    outbox = _outbox_dir()
    identity_url = _identity_base_url()
    supabase_url = ""
    anon_key = ""
    service_role = ""
    if not args.dry_run:
        supabase_url = _required_env("SUPABASE_URL")
        anon_key = _required_env("SUPABASE_ANON_KEY")
        service_role = _required_env("SUPABASE_SERVICE_ROLE")
        # Fail-fast reachability facts
        try:
            st, _ = _http_json("GET", f"{identity_url}/ready", timeout=5.0)
            if st != 200:
                st, _ = _http_json("GET", f"{identity_url}/health", timeout=5.0)
            if st != 200:
                raise RuntimeError(f"Identity ready/health HTTP {st}")
        except Exception as exc:  # noqa: BLE001
            print(
                "OPERATOR BLOCKER: Identity unreachable at "
                f"{identity_url}: {exc}. Ship code+unit tests; re-run provision when up.",
                file=sys.stderr,
            )
            return 2
        if not outbox.is_dir():
            print(
                f"OPERATOR BLOCKER: file SMS outbox missing: {outbox} "
                "(set LIFE_SIM_FILE_SMS_OUTBOX_DIR; require SMS_PROVIDER=file). "
                "Do not invent GET /dev/last-otp.",
                file=sys.stderr,
            )
            return 2

    print("DOGEstonia life-sim provision (REQ11-05)")
    print(f"Users: {len(users)} (of {life_sim.EXPECTED_USERS})")
    print(f"Generation: {generation_id}")
    print(f"Secrets out: {out_path} (gitignored)")
    print(f"Identity: {identity_url}")
    if supabase_url:
        host = supabase_url.split("//", 1)[-1].split("/", 1)[0]
        print(f"Auth Supabase host (Identity project): {host}")
    print(f"Outbox: {outbox}")
    print(f"Pace: {args.pace_s}s between phone/request")
    if args.dry_run:
        print("Mode: DRY-RUN (no HTTP)")
    print()

    entries: list[dict[str, Any]] = []
    failures: list[str] = []
    for i, user in enumerate(users):
        fid = str(user["fixture_user_id"])
        did_phone_otp = False
        try:
            entry = provision_one(
                user,
                supabase_url=supabase_url,
                anon_key=anon_key,
                service_role=service_role,
                identity_url=identity_url,
                outbox_dir=outbox,
                existing=existing_by_id.get(fid),
                dry_run=args.dry_run,
                otp_wait_s=args.otp_wait_s,
            )
            entry["generation_id"] = generation_id
            entries.append(entry)
            # Checkpoint: survive Cursor/shell death mid-run (secrets gitignored).
            if not args.dry_run:
                doc = lib.build_creds_document(generation_id=generation_id, entries=entries)
                lib.write_creds_document(out_path, doc)
            did_phone_otp = entry.get("verify") == "file_otp_confirmed"
            print(
                f"[{i+1:>4}/{len(users)}] {fid} "
                f"email={entry['email']} phone={entry['phone_e164']} "
                f"verified={entry.get('phone_verified', args.dry_run)} "
                f"via={entry.get('verify', entry.get('status', 'ok'))}"
            )
        except Exception as exc:  # noqa: BLE001
            failures.append(fid)
            print(f"[{i+1:>4}/{len(users)}] {fid} -> ERROR {exc}", file=sys.stderr)
            # Still record partial? fail-closed: skip incomplete entry
        # Pace only after a live phone/request (rate-limit); skip for already_verified.
        if (
            i + 1 < len(users)
            and not args.dry_run
            and args.pace_s > 0
            and did_phone_otp
        ):
            time.sleep(args.pace_s)

    doc = lib.build_creds_document(generation_id=generation_id, entries=entries)
    lib.write_creds_document(out_path, doc)
    print()
    print(f"Wrote {len(entries)} entries → {out_path}")
    print(f"Failed: {len(failures)}")
    if failures:
        print("Failed IDs: " + ", ".join(failures[:20]))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
