"""GW-GAUTH-04: authoritative author from identity introspection `sub`."""

from __future__ import annotations

from urllib.parse import urlparse

from core.identity.introspection_result import IntrospectionResult
from core.intake.contracts import Submitter


def resolve_identity_issuer_from_introspect_url(introspect_url: str | None) -> str:
    """Issuer for persisted authorship when `sub` comes from identity introspection."""
    if not introspect_url:
        return "identity://gateway"
    parsed = urlparse(introspect_url.strip())
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}"
    return introspect_url.strip().rstrip("/")


def authoritative_submitter_from_introspection(
    *,
    payload_submitter: Submitter,
    introspection: IntrospectionResult,
    identity_introspect_url: str | None,
) -> Submitter:
    """Map verified introspection `sub` to Story Store submitter fields (GW-GAUTH-04)."""
    if not introspection.active:
        msg = "Introspection must be active to resolve authoritative submitter."
        raise ValueError(msg)
    if introspection.sub is None or not introspection.sub.strip():
        msg = "Introspection sub is required for authoritative submitter."
        raise ValueError(msg)
    _ = payload_submitter  # payload retained for mismatch logging upstream
    return Submitter(
        external_user_id=introspection.sub.strip(),
        identity_issuer=resolve_identity_issuer_from_introspect_url(
            identity_introspect_url
        ),
    )


def payload_submitter_mismatches_introspection(
    payload_submitter: Submitter,
    introspection: IntrospectionResult,
) -> bool:
    if introspection.sub is None:
        return False
    return payload_submitter.external_user_id != introspection.sub.strip()
