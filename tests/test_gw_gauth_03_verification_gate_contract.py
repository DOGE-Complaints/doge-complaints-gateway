"""GW-GAUTH-03: phone_verified gate + verification_required (403, OAUTH-04)."""

from __future__ import annotations

import pytest

from core.config import load_config_from_env
from core.identity.introspection_result import IntrospectionResult
from core.identity.verification_gate import (
    VerificationGateOutcome,
    evaluate_verification_gate,
)
from core.identity.verify_url import build_verify_url

GAUTH_TEST_SPA_VERIFY_BASE = "https://spa.test"


def test_build_verify_url_from_spa_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("SPA_VERIFY_BASE_URL", GAUTH_TEST_SPA_VERIFY_BASE)
    config = load_config_from_env()
    assert build_verify_url(config) == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify"
    assert (
        build_verify_url(config, return_context="intake")
        == f"{GAUTH_TEST_SPA_VERIFY_BASE}/verify?context=intake"
    )


def test_evaluate_verification_gate_branches() -> None:
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", phone_verified=True)
        )
        is VerificationGateOutcome.ALLOW
    )
    assert (
        evaluate_verification_gate(
            IntrospectionResult(active=True, sub="u", phone_verified=False)
        )
        is VerificationGateOutcome.VERIFICATION_REQUIRED
    )
    assert (
        evaluate_verification_gate(IntrospectionResult(active=False))
        is VerificationGateOutcome.UNAUTHORIZED
    )
