"""GW-REQ11-08 — shared fail-closed settings for pack-wave provision.

Hard requirements:
  - SMS_PROVIDER=file + readable outbox (no invent GET /dev/last-otp)
  - Email domain @dogestonia.me
  - Auth Supabase credentials = Identity project (not gateway content DB)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# SSOT domain for life-sim fixture emails (AC-GW-REQ1108-02).
EMAIL_DOMAIN = "dogestonia.me"
REQUIRED_SMS_PROVIDER = "file"

_SANDBOX = Path(__file__).resolve().parent
_TESTS = _SANDBOX.parent
_GATEWAY_ROOT = _TESTS.parent
_REPO_MONOREPO = _GATEWAY_ROOT.parent


class ProvisionConfigError(RuntimeError):
    """Fail-closed shared config violation."""


def load_env_file(path: Path) -> None:
    """Load KEY=value into os.environ if key not already set."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if " #" in line:
            line = line.split(" #", 1)[0].rstrip()
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_gateway_and_identity_env() -> None:
    """Load gateway then Identity .env (Identity wins for Auth via force_*)."""
    load_env_file(_GATEWAY_ROOT / ".env.test")
    load_env_file(_GATEWAY_ROOT / ".env")
    load_env_file(_REPO_MONOREPO / "doge-identity-service" / ".env")


def force_identity_supabase_auth_env() -> None:
    """Auth users must live in Identity's Supabase (JWT iss/JWKS).

    Gateway `.env` often points at a different project; re-apply Identity SUPABASE_*.
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


def assert_email_domain(domain: str = EMAIL_DOMAIN) -> None:
    """Fail-closed if configured domain is not @dogestonia.me."""
    cleaned = domain.strip().lstrip("@").lower()
    expected = EMAIL_DOMAIN.lower()
    if cleaned != expected:
        raise ProvisionConfigError(
            f"email domain must be @{expected}; got @{cleaned} "
            "(AC-GW-REQ1108-02; do not use dogestonia.com)"
        )


def require_sms_provider_file() -> str:
    """Require SMS_PROVIDER=file (case-insensitive)."""
    raw = os.getenv("SMS_PROVIDER", "").strip().lower()
    if raw != REQUIRED_SMS_PROVIDER:
        raise ProvisionConfigError(
            f"SMS_PROVIDER must be '{REQUIRED_SMS_PROVIDER}' (got {raw!r}). "
            "Do not invent GET /dev/last-otp; do not silent-fallback to Telnyx/mock."
        )
    return raw


def resolve_file_sms_outbox_dir() -> Path:
    """Resolve FILE_SMS / LIFE_SIM outbox path (Identity-relative if not absolute)."""
    raw = (
        os.getenv("LIFE_SIM_FILE_SMS_OUTBOX_DIR", "").strip()
        or os.getenv("FILE_SMS_OUTBOX_DIR", "").strip()
    )
    if raw:
        if " #" in raw:
            raw = raw.split(" #", 1)[0].strip()
        p = Path(raw)
        if not p.is_absolute():
            p = (_REPO_MONOREPO / "doge-identity-service" / p).resolve()
        return p
    return (_REPO_MONOREPO / "doge-identity-service" / "var" / "sms-outbox").resolve()


def require_readable_outbox(outbox: Path | None = None) -> Path:
    """Fail-closed if outbox directory is missing or not readable."""
    path = outbox or resolve_file_sms_outbox_dir()
    if not path.is_dir():
        raise ProvisionConfigError(
            f"file SMS outbox missing or not a directory: {path} "
            "(set LIFE_SIM_FILE_SMS_OUTBOX_DIR / FILE_SMS_OUTBOX_DIR; "
            "require SMS_PROVIDER=file; do not invent GET /dev/last-otp)"
        )
    if not os.access(path, os.R_OK):
        raise ProvisionConfigError(f"file SMS outbox not readable: {path}")
    return path


def identity_base_url() -> str:
    explicit = os.getenv("LIFE_SIM_IDENTITY_URL", "").strip() or os.getenv(
        "IDENTITY_URL", ""
    ).strip()
    if explicit:
        return explicit.rstrip("/")
    return "http://127.0.0.1:8100"


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise ProvisionConfigError(f"Missing required env variable: {name}")
    return value


@dataclass(frozen=True)
class PackWaveConfig:
    """Resolved fail-closed settings for a pack-wave run."""

    sms_provider: str
    outbox_dir: Path
    email_domain: str
    identity_url: str
    supabase_url: str
    anon_key: str
    service_role: str


def resolve_pack_wave_config(*, skip_live_auth: bool = False) -> PackWaveConfig:
    """Load env + force Identity Auth + fail-closed SMS/domain/outbox.

    When skip_live_auth=True (offline/dry-run unit path), Supabase keys may be empty.
    """
    load_gateway_and_identity_env()
    force_identity_supabase_auth_env()
    assert_email_domain(EMAIL_DOMAIN)
    sms = require_sms_provider_file()
    outbox = require_readable_outbox()
    identity_url = identity_base_url()
    if skip_live_auth:
        return PackWaveConfig(
            sms_provider=sms,
            outbox_dir=outbox,
            email_domain=EMAIL_DOMAIN,
            identity_url=identity_url,
            supabase_url=os.getenv("SUPABASE_URL", "").strip(),
            anon_key=os.getenv("SUPABASE_ANON_KEY", "").strip(),
            service_role=os.getenv("SUPABASE_SERVICE_ROLE", "").strip(),
        )
    return PackWaveConfig(
        sms_provider=sms,
        outbox_dir=outbox,
        email_domain=EMAIL_DOMAIN,
        identity_url=identity_url,
        supabase_url=require_env("SUPABASE_URL"),
        anon_key=require_env("SUPABASE_ANON_KEY"),
        service_role=require_env("SUPABASE_SERVICE_ROLE"),
    )
