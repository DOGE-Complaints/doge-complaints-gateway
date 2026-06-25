from __future__ import annotations

import secrets
from dataclasses import dataclass
from typing import Mapping


class UnauthorizedError(Exception):
    """Raised when the service API token is missing or invalid."""


class UserTokenMissingError(UnauthorizedError):
    """Raised when a verify-gated route lacks the user access token."""


class UserTokenIntrospectionError(UnauthorizedError):
    """Raised when identity introspection fails or user token is inactive (fail-closed)."""


def extract_user_token(headers: Mapping[str, str]) -> str | None:
    """Read end-user OAuth access token from X-User-Token (GW-GAUTH-01 stub; GAUTH-02 introspects)."""
    h = _lower_headers(headers)
    raw = h.get("x-user-token")
    if not raw:
        return None
    token = raw.strip()
    return token if token else None


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
    """Service-to-service gate for channel trust (req-19 §5).

    When ``mandatory`` is True, ``require()`` rejects if no token is configured or
    missing from headers (public-content mutations — GW-GAUTH-01).
    """

    _expected: str | None
    mandatory: bool = False

    @classmethod
    def disabled(cls) -> ServiceTokenAuth:
        return cls(_expected=None, mandatory=False)

    @classmethod
    def from_secret(cls, secret: str, *, mandatory: bool = False) -> ServiceTokenAuth:
        s = secret.strip()
        if not s:
            return cls(_expected=None, mandatory=mandatory)
        return cls(_expected=s, mandatory=mandatory)

    @classmethod
    def mandatory_channel(cls) -> ServiceTokenAuth:
        """Configured or not — public mutations always require a valid service token."""
        return cls(_expected=None, mandatory=True)

    def is_enabled(self) -> bool:
        return self._expected is not None

    def require(self, headers: Mapping[str, str], *, mandatory: bool | None = None) -> None:
        enforce = self.mandatory if mandatory is None else mandatory
        if not self.is_enabled():
            if enforce:
                raise UnauthorizedError("Missing service API token.")
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
        return ServiceTokenAuth.mandatory_channel()
    return ServiceTokenAuth.from_secret(raw, mandatory=True)
