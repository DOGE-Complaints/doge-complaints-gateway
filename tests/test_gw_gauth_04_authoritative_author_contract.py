"""GW-GAUTH-04: authoritative author from introspection `sub` (unit coverage)."""

from __future__ import annotations

from core.identity.authoritative_submitter import (
    authoritative_submitter_from_introspection,
    payload_submitter_mismatches_introspection,
    resolve_identity_issuer_from_introspect_url,
)
from core.identity.introspection_result import IntrospectionResult
from core.intake.contracts import Submitter
from tests.conftest import GAUTH_TEST_IDENTITY_URL

CLAIMED_PAYLOAD_SUB = "claimed-payload-sub-wrong"
INTROSPECTION_SUB = "introspected-author-sub-99"


def test_resolve_identity_issuer_from_introspect_url() -> None:
    assert (
        resolve_identity_issuer_from_introspect_url(GAUTH_TEST_IDENTITY_URL)
        == "https://identity.test"
    )
    assert resolve_identity_issuer_from_introspect_url(None) == "identity://gateway"


def test_authoritative_submitter_mapping_unit() -> None:
    payload = Submitter(
        external_user_id=CLAIMED_PAYLOAD_SUB,
        identity_issuer="https://idp.example.com/eid",
    )
    intro = IntrospectionResult(active=True, sub=INTROSPECTION_SUB, phone_verified=True)
    assert payload_submitter_mismatches_introspection(payload, intro) is True
    resolved = authoritative_submitter_from_introspection(
        payload_submitter=payload,
        introspection=intro,
        identity_introspect_url=GAUTH_TEST_IDENTITY_URL,
    )
    assert resolved.external_user_id == INTROSPECTION_SUB
    assert resolved.identity_issuer == "https://identity.test"
