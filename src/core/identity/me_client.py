from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from core.config import AppConfig
from core.identity.introspection_client import IntrospectionResult


class IdentityMeError(Exception):
    """Identity /me transport or response parse failure (fail-closed)."""


@dataclass(frozen=True)
class IdentityMeClient:
    """GET /me with forwarded Supabase Bearer (GW-DRAFT-02, D-DRAFT-1)."""

    base_url: str
    timeout_s: float

    def fetch_me(self, bearer_token: str) -> IntrospectionResult:
        token = bearer_token.strip()
        if not token:
            return IntrospectionResult(active=False)
        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                response = client.get(
                    f"{self.base_url.rstrip('/')}/me",
                    headers={"Authorization": f"Bearer {token}"},
                )
        except httpx.TimeoutException as exc:
            raise IdentityMeError("Identity /me timed out.") from exc
        except httpx.HTTPError as exc:
            raise IdentityMeError("Identity /me request failed.") from exc

        if response.status_code in {401, 403}:
            return IntrospectionResult(active=False)
        if response.status_code >= 500:
            raise IdentityMeError(f"Identity /me returned {response.status_code}.")

        try:
            body: Any = response.json()
        except ValueError as exc:
            raise IdentityMeError("Identity /me returned invalid JSON.") from exc
        if not isinstance(body, dict):
            raise IdentityMeError("Identity /me returned non-object JSON.")
        return _parse_me_body(body)


def _parse_me_body(body: dict[str, Any]) -> IntrospectionResult:
    data = body.get("data")
    if not isinstance(data, dict):
        raise IdentityMeError("Invalid /me response: missing data object.")
    sub = data.get("supabase_user_id")
    if not isinstance(sub, str) or not sub.strip():
        raise IdentityMeError("Invalid /me response: missing supabase_user_id.")
    phone_verified = data.get("phone_verified")
    if not isinstance(phone_verified, bool):
        raise IdentityMeError("Invalid /me response: phone_verified must be bool.")
    return IntrospectionResult(active=True, sub=sub.strip(), phone_verified=phone_verified)


def build_identity_me_from_config(config: AppConfig) -> IdentityMeClient | None:
    base = config.identity_base_url
    if base is None:
        return None
    return IdentityMeClient(
        base_url=base,
        timeout_s=float(config.request_timeout_s),
    )
