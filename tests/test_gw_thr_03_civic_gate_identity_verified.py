"""GW-THR-03: civic gate opaque identity_verified only — no phone dual-read."""

from __future__ import annotations

import pytest

from core.identity.introspection_result import IntrospectionResult
from core.identity.me_client import IdentityMeError, _parse_me_body
from core.identity.verification_gate import (
    VerificationGateOutcome,
    evaluate_verification_gate,
)


def test_parse_me_reads_identity_verified_bool() -> None:
    result = _parse_me_body(
        {
            "data": {
                "supabase_user_id": "user-1",
                "identity_verified": True,
                "phone_verified": False,
            }
        }
    )
    assert result.active is True
    assert result.sub == "user-1"
    assert result.identity_verified is True
    assert result.phone_verified is False


def test_parse_me_missing_opaque_is_none_not_phone_fallback() -> None:
    result = _parse_me_body(
        {
            "data": {
                "supabase_user_id": "user-2",
                "phone_verified": True,
            }
        }
    )
    assert result.phone_verified is True
    assert result.identity_verified is None


def test_parse_me_invalid_opaque_fail_closed() -> None:
    with pytest.raises(IdentityMeError, match="identity_verified must be bool"):
        _parse_me_body(
            {
                "data": {
                    "supabase_user_id": "user-3",
                    "identity_verified": "yes",
                }
            }
        )


def test_gate_allow_only_opaque_true() -> None:
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", identity_verified=True)
        )
        is VerificationGateOutcome.ALLOW
    )


def test_gate_phone_only_stub_must_not_allow() -> None:
    assert (
        evaluate_verification_gate(
            IntrospectionResult(
                active=True,
                sub="u",
                phone_verified=True,
                identity_verified=None,
            )
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )
    assert (
        evaluate_verification_gate(
            IntrospectionResult(
                active=True,
                sub="u",
                phone_verified=True,
                identity_verified=False,
            )
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )


def test_gate_inactive_unauthorized() -> None:
    assert (
        evaluate_verification_gate(IntrospectionResult(active=False))
        is VerificationGateOutcome.UNAUTHORIZED
    )


def test_gate_missing_or_false_opaque_verification_required() -> None:
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", identity_verified=None)
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", identity_verified=False)
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )
