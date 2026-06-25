from __future__ import annotations

from urllib.parse import urlencode

from core.config import AppConfig

DEFAULT_SPA_VERIFY_BASE_URL = "http://localhost:3000"


def resolve_spa_verify_base_url(config: AppConfig) -> str:
    raw = config.spa_verify_base_url
    if raw and raw.strip():
        return raw.strip().rstrip("/")
    return DEFAULT_SPA_VERIFY_BASE_URL


def build_verify_url(config: AppConfig, *, return_context: str | None = None) -> str:
    """OAUTH-04 verify_url for gateway verification_required responses (GW-GAUTH-03)."""
    base = resolve_spa_verify_base_url(config)
    if return_context:
        query = urlencode({"context": return_context})
        return f"{base}/verify?{query}"
    return f"{base}/verify"
