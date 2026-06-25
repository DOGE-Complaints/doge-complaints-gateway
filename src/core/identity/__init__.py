"""Gateway → identity OAuth introspection (GW-GAUTH-02)."""

from core.identity.authoritative_submitter import (
    authoritative_submitter_from_introspection,
    payload_submitter_mismatches_introspection,
    resolve_identity_issuer_from_introspect_url,
)
from core.identity.introspection_client import (
    IdentityIntrospectionClient,
    IdentityIntrospectionError,
    IntrospectionResult,
    build_identity_introspection_from_config,
)
from core.identity.verification_gate import (
    DEFAULT_VERIFICATION_REQUIRED_REASON,
    VerificationGateOutcome,
    evaluate_verification_gate,
)
from core.identity.verify_url import build_verify_url, resolve_spa_verify_base_url

__all__ = [
    "DEFAULT_VERIFICATION_REQUIRED_REASON",
    "IdentityIntrospectionClient",
    "IdentityIntrospectionError",
    "IntrospectionResult",
    "VerificationGateOutcome",
    "authoritative_submitter_from_introspection",
    "build_identity_introspection_from_config",
    "build_verify_url",
    "evaluate_verification_gate",
    "payload_submitter_mismatches_introspection",
    "resolve_identity_issuer_from_introspect_url",
    "resolve_spa_verify_base_url",
]
