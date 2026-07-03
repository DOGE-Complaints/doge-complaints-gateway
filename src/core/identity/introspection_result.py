from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class IntrospectionResult:
    """Identity session snapshot from /me or legacy introspection-shaped JSON."""

    active: bool
    sub: str | None = None
    phone_verified: bool | None = None
