from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from core.config import AppConfig


class IdentityIntrospectionError(Exception):
    """Identity introspection transport or response parse failure (fail-closed)."""


@dataclass(frozen=True)
class IntrospectionResult:
    active: bool
    sub: str | None = None
    phone_verified: bool | None = None


@dataclass(frozen=True)
class IdentityIntrospectionClient:
    """POST /oauth/introspect with service Bearer + form token= (RFC 7662-style)."""

    introspect_url: str
    service_token: str
    timeout_s: float

    def introspect(self, user_token: str) -> IntrospectionResult:
        token = user_token.strip()
        if not token:
            return IntrospectionResult(active=False)
        try:
            with httpx.Client(timeout=self.timeout_s) as client:
                response = client.post(
                    self.introspect_url,
                    data={"token": token},
                    headers={
                        "Authorization": f"Bearer {self.service_token}",
                        "Content-Type": "application/x-www-form-urlencoded",
                    },
                )
        except httpx.TimeoutException as exc:
            raise IdentityIntrospectionError("Identity introspection timed out.") from exc
        except httpx.HTTPError as exc:
            raise IdentityIntrospectionError("Identity introspection request failed.") from exc

        if response.status_code >= 500:
            raise IdentityIntrospectionError(
                f"Identity introspection returned {response.status_code}."
            )
        if response.status_code in {401, 403}:
            raise IdentityIntrospectionError("Identity rejected gateway service token.")

        try:
            body: Any = response.json()
        except ValueError as exc:
            raise IdentityIntrospectionError("Identity introspection returned invalid JSON.") from exc
        if not isinstance(body, dict):
            raise IdentityIntrospectionError("Identity introspection returned non-object JSON.")
        return _parse_introspection_body(body)


def _parse_introspection_body(body: dict[str, Any]) -> IntrospectionResult:
    active = body.get("active")
    if active is not True:
        return IntrospectionResult(active=False)
    sub = body.get("sub")
    if not isinstance(sub, str) or not sub.strip():
        raise IdentityIntrospectionError("Invalid introspection response: missing sub.")
    phone_verified = body.get("phone_verified")
    if not isinstance(phone_verified, bool):
        raise IdentityIntrospectionError(
            "Invalid introspection response: phone_verified must be bool."
        )
    return IntrospectionResult(active=True, sub=sub.strip(), phone_verified=phone_verified)


def build_identity_introspection_from_config(
    config: AppConfig,
) -> IdentityIntrospectionClient | None:
    base = config.identity_introspect_url
    token = config.identity_service_token
    if base is None or token is None:
        return None
    return IdentityIntrospectionClient(
        introspect_url=f"{base.rstrip('/')}/oauth/introspect",
        service_token=token,
        timeout_s=float(config.request_timeout_s),
    )
