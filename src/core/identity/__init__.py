"""Gateway → identity session helpers (GW-DRAFT-02 /me, verification gate, author)."""

from core.identity.authoritative_submitter import (
    authoritative_submitter_from_introspection,
    payload_submitter_mismatches_introspection,
    resolve_identity_issuer_from_introspect_url,
)
from core.identity.introspection_result import IntrospectionResult
from core.identity.verification_gate import (
    DEFAULT_VERIFICATION_REQUIRED_REASON,
    VerificationGateOutcome,
    evaluate_verification_gate,
)
from core.identity.me_client import (
    IdentityMeClient,
    IdentityMeError,
    build_identity_me_from_config,
)

from core.identity.verify_url import build_verify_url, resolve_spa_verify_base_url

__all__ = [
    "DEFAULT_VERIFICATION_REQUIRED_REASON",
    "IdentityMeClient",
    "IdentityMeError",
    "IntrospectionResult",
    "VerificationGateOutcome",
    "authoritative_submitter_from_introspection",
    "build_identity_me_from_config",
    "build_verify_url",
    "evaluate_verification_gate",
    "payload_submitter_mismatches_introspection",
    "resolve_identity_issuer_from_introspect_url",
    "resolve_spa_verify_base_url",
]
