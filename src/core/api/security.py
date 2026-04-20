from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Mapping


class UnauthorizedError(Exception):
    """Raised when the service API token is missing or invalid."""


def _lower_headers(headers: Mapping[str, str]) -> dict[str, str]:
    return {str(k).lower(): str(v) for k, v in headers.items()}


def extract_service_token(headers: Mapping[str, str]) -> str | None:
    """Read token from Authorization: Bearer … or X-Service-Token."""
    h = _lower_headers(headers)
    auth = h.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth[7:].strip()
        return token if token else None
    xst = h.get("x-service-token")
    if xst:
        t = xst.strip()
        return t if t else None
    return None


@dataclass(frozen=True)
class ServiceTokenAuth:
    """Service-to-service gate: optional; when disabled, require() is a no-op.

User identity stays on GPT/IdP; this token protects gateway-to-gateway calls only
(see requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md §5).
"""

    _expected: str | None

    @classmethod
    def disabled(cls) -> ServiceTokenAuth:
        return cls(_expected=None)

    @classmethod
    def from_secret(cls, secret: str) -> ServiceTokenAuth:
        s = secret.strip()
        if not s:
            return cls.disabled()
        return cls(_expected=s)

    def is_enabled(self) -> bool:
        return self._expected is not None

    def require(self, headers: Mapping[str, str]) -> None:
        if not self.is_enabled():
            return
        assert self._expected is not None
        got = extract_service_token(headers)
        if got is None:
            raise UnauthorizedError("Missing service API token.")
        if not secrets.compare_digest(got, self._expected):
            raise UnauthorizedError("Invalid service API token.")


def build_service_auth_from_env(env: Mapping[str, str] | None = None) -> ServiceTokenAuth:
    from os import environ

    source = env if env is not None else environ
    raw = source.get("SERVICE_API_TOKEN")
    if raw is None:
        return ServiceTokenAuth.disabled()
    return ServiceTokenAuth.from_secret(raw)
