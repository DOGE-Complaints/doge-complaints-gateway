from __future__ import annotations

from enum import Enum

from core.identity.introspection_result import IntrospectionResult

VERIFICATION_REQUIRED_ERROR = "verification_required"
DEFAULT_VERIFICATION_REQUIRED_REASON = (
    "Phone verification is required before this action can proceed."
)


class VerificationGateOutcome(str, Enum):
    ALLOW = "allow"
    VERIFICATION_REQUIRED = "verification_required"
    UNAUTHORIZED = "unauthorized"


def evaluate_verification_gate(result: IntrospectionResult) -> VerificationGateOutcome:
    """GW-GAUTH-03: decide access from introspection result (active already fetched)."""
    if not result.active:
        return VerificationGateOutcome.UNAUTHORIZED
    if result.phone_verified is not True:
        return VerificationGateOutcome.VERIFICATION_REQUIRED
    return VerificationGateOutcome.ALLOW
