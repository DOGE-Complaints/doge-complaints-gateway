"""GW-REQ11-05 — offline helpers for life-sim user provision (no secrets in git).

Deterministic email/phone derivation, CSPRNG passwords, secrets path hygiene,
file-SMS outbox OTP parse. Live HTTP lives in life_sim_provision_users.py.
"""

from __future__ import annotations

import json
import re
import secrets
import string
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SANDBOX = Path(__file__).resolve().parent
SECRETS_DIR = SANDBOX / ".secrets"
USERS_PATH = SANDBOX / "dogestonia_life_sim_users_v0_1.json"

PASSWORD_MIN_LEN = 24
# AC-GW-REQ1108-02 / REQ11-05: hard domain (shared with life_sim_provision_config).
EMAIL_DOMAIN = "dogestonia.me"
_EMAIL_DOMAIN = EMAIL_DOMAIN
_OTP_RE = re.compile(r"verification code is\s+(\d{6})", re.IGNORECASE)
_CREDS_NAME_RE = re.compile(r"^life_sim_users_creds_(.+)\.json$")


def utc_now_iso() -> str:
    """UTC ISO-8601 with Z suffix (second precision)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fixture_user_index(fixture_user_id: str) -> int:
    """Parse life-sim-user-NNNN → zero-based index."""
    prefix = "life-sim-user-"
    if not fixture_user_id.startswith(prefix):
        raise ValueError(f"unexpected fixture_user_id={fixture_user_id!r}")
    n = int(fixture_user_id[len(prefix) :])
    if n < 1:
        raise ValueError(f"fixture_user_id index must be >= 1: {fixture_user_id!r}")
    return n - 1


def derive_email(fixture_user_id: str) -> str:
    """Deterministic email from fixture_user_id (Supabase-valid domain).

    Local-part uses dots (not only hyphens) — some Auth configs reject
    `*.local` / multi-label custom domains as invalid.
    """
    idx = fixture_user_index(fixture_user_id)
    n = idx + 1
    return f"life.sim.user.{n:04d}@{_EMAIL_DOMAIN}"


def derive_phone_e164(fixture_user_id: str) -> str:
    """Unique +372 E.164 from fixture index (PHONE_ONE_ACCOUNT_PER_NUMBER).

    Pattern: +37251 + zero-padded 1-based user number (6 digits) →
    life-sim-user-0001 → +37251000001 … life-sim-user-0200 → +37251000200.
    """
    idx = fixture_user_index(fixture_user_id)
    n = idx + 1
    if n < 1 or n > 999999:
        raise ValueError(f"phone derivation out of range for {fixture_user_id!r}")
    return f"+37251{n:06d}"


def generate_password(*, length: int = PASSWORD_MIN_LEN) -> str:
    """CSPRNG password via secrets; length >= 24 with mixed classes."""
    if length < PASSWORD_MIN_LEN:
        raise ValueError(f"password length must be >= {PASSWORD_MIN_LEN}")
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_"
    # Ensure at least one of each class, then fill with CSPRNG.
    required = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice("!@#$%^&*-_"),
    ]
    rest = [secrets.choice(alphabet) for _ in range(length - len(required))]
    chars = required + rest
    # Fisher–Yates with secrets
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def password_is_strong(password: str) -> bool:
    """AC-02 strength check (length + mixed class)."""
    if len(password) < PASSWORD_MIN_LEN:
        return False
    classes = 0
    if any(c.islower() for c in password):
        classes += 1
    if any(c.isupper() for c in password):
        classes += 1
    if any(c.isdigit() for c in password):
        classes += 1
    if any(c in "!@#$%^&*-_" for c in password):
        classes += 1
    return classes >= 3


def new_generation_id(now: datetime | None = None) -> str:
    """Filesystem-safe generation id (UTC compact)."""
    dt = now or datetime.now(timezone.utc)
    return dt.strftime("%Y%m%dT%H%M%SZ")


def secrets_path_for_generation(generation_id: str, *, secrets_dir: Path | None = None) -> Path:
    """Target path under gitignored .secrets/ (never commit)."""
    gid = generation_id.strip()
    if not gid or "/" in gid or "\\" in gid or ".." in gid:
        raise ValueError(f"invalid generation_id={generation_id!r}")
    base = secrets_dir or SECRETS_DIR
    if not _is_under_secrets_tree(base):
        raise ValueError(f"secrets_dir must resolve under sandbox/.secrets: {base}")
    return base / f"life_sim_users_creds_{gid}.json"


def _is_under_secrets_tree(path: Path) -> bool:
    """Fail-closed: secrets dir must be sandbox/.secrets (or equal)."""
    try:
        resolved = path.resolve()
        secrets_resolved = SECRETS_DIR.resolve()
        return resolved == secrets_resolved or secrets_resolved in resolved.parents
    except OSError:
        return False


def assert_secrets_path_hygiene(path: Path) -> None:
    """Raise if path is not under .secrets/ or would be tracked as product fixture."""
    resolved = path.resolve()
    secrets_resolved = SECRETS_DIR.resolve()
    if secrets_resolved not in resolved.parents and resolved.parent != secrets_resolved:
        # allow exact file under .secrets/
        if resolved.parent != secrets_resolved:
            raise ValueError(
                f"secrets path must live under {SECRETS_DIR}: got {path}"
            )
    name = resolved.name
    if not _CREDS_NAME_RE.match(name):
        raise ValueError(
            f"secrets filename must match life_sim_users_creds_<generation_id>.json: {name}"
        )


def extract_otp_from_outbox_text(text: str) -> str | None:
    """Parse latest OTP from file-SMS outbox log contents (PV-10 file sink)."""
    code: str | None = None
    for line in text.splitlines():
        match = _OTP_RE.search(line)
        if match:
            code = match.group(1)
    return code


def read_latest_otp_from_outbox(
    outbox_dir: Path,
    phone_e164: str,
    *,
    wait_s: float = 0.0,
) -> str:
    """Read OTP for phone from `{sanitized}.log` under FILE_SMS_OUTBOX_DIR.

    Does **not** invent GET /dev/last-otp — disk only.
    """
    import time

    safe = re.sub(r"[^+0-9]", "", phone_e164)
    log_path = outbox_dir / f"{safe}.log"
    deadline = time.monotonic() + max(0.0, wait_s)
    while True:
        if log_path.is_file():
            code = extract_otp_from_outbox_text(log_path.read_text(encoding="utf-8"))
            if code:
                return code
        if time.monotonic() >= deadline:
            break
        time.sleep(0.25)
    raise FileNotFoundError(
        f"OTP not found in file outbox for {phone_e164} at {log_path} "
        "(require Identity SMS_PROVIDER=file; do not invent HTTP last-otp)"
    )


def load_users_creds(path: Path) -> dict[str, Any]:
    """Load secrets JSON; never log password fields."""
    assert_secrets_path_hygiene(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError("creds root must be a JSON object")
    users = data.get("users")
    if not isinstance(users, list):
        raise RuntimeError("creds.users must be a list")
    return data


def index_creds_by_fixture_user_id(doc: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Map fixture_user_id → creds entry."""
    out: dict[str, dict[str, Any]] = {}
    for entry in doc.get("users", []):
        if not isinstance(entry, dict):
            continue
        fid = str(entry.get("fixture_user_id") or "").strip()
        if fid:
            out[fid] = entry
    return out


def discover_latest_creds_path(*, secrets_dir: Path | None = None) -> Path | None:
    """Newest life_sim_users_creds_*.json by mtime, or None."""
    base = secrets_dir or SECRETS_DIR
    if not base.is_dir():
        return None
    candidates = sorted(
        base.glob("life_sim_users_creds_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def build_creds_document(
    *,
    generation_id: str,
    entries: list[dict[str, Any]],
    created_at_utc: str | None = None,
) -> dict[str, Any]:
    """Secrets document body (min fields per AC)."""
    return {
        "schema_note": "life-sim fixture user credentials; gitignored; never commit",
        "generation_id": generation_id,
        "created_at_utc": created_at_utc or utc_now_iso(),
        "auth_path": "supabase_password_grant",
        "otp_path": "identity_file_sms_outbox",
        "pool_m20_status": "deprecated_for_new_pass",
        "users": entries,
    }


def write_creds_document(path: Path, doc: dict[str, Any]) -> Path:
    """Write secrets file under .secrets/ (mkdir). Never print passwords."""
    assert_secrets_path_hygiene(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
