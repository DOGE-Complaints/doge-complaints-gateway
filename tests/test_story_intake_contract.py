from __future__ import annotations

import pytest

from core.intake import (
    INTAKE_RESPONSE_SCHEMA_VERSION,
    INTAKE_SCHEMA_VERSION,
    IntakeValidationError,
    build_story_intake_response,
    parse_story_intake_request,
)


def test_parse_story_intake_request_valid_payload() -> None:
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {
                "external_user_id": "opaque-user-123",
                "identity_issuer": "https://idp.example.com",
            },
            "narrative": {
                "original_text": "Road is blocked near district center.",
                "language": "en",
                "title_hint": "Blocked road",
            },
            "origin": {
                "source": "openai_gpt_action",
                "conversation_id": "conv-1",
                "tool_call_id": "call-1",
            },
            "privacy": {
                "contains_pii": False,
                "redaction_requested": True,
            },
            "live_story_context": {
                "consistency_notes": "User clarified scope.",
            },
        }
    )
    assert request.schema_version == INTAKE_SCHEMA_VERSION
    assert request.submitter.external_user_id == "opaque-user-123"
    assert request.submitter.identity_issuer == "https://idp.example.com"
    assert request.narrative.original_text.startswith("Road is blocked")
    assert request.origin is not None
    assert request.origin.source == "openai_gpt_action"
    assert request.privacy is not None
    assert request.privacy.redaction_requested is True
    assert request.live_story_context is not None
    assert request.live_story_context.consistency_notes == "User clarified scope."


def test_parse_story_intake_request_requires_schema_version() -> None:
    with pytest.raises(IntakeValidationError, match="schema_version"):
        parse_story_intake_request(
            {
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {"original_text": "text"},
            }
        )


def test_parse_story_intake_request_rejects_unsupported_version() -> None:
    with pytest.raises(IntakeValidationError, match="Unsupported schema_version"):
        parse_story_intake_request(
            {
                "schema_version": "v0",
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {"original_text": "text"},
            }
        )


def test_parse_story_intake_request_requires_external_user_id() -> None:
    with pytest.raises(IntakeValidationError, match="submitter.external_user_id"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {},
                "narrative": {"original_text": "text"},
            }
        )


def test_parse_story_intake_request_requires_narrative_original_text() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.original_text"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {},
            }
        )


def test_parse_story_intake_request_requires_narrative_language() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.language"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {"original_text": "text", "title_hint": "title"},
            }
        )


def test_parse_story_intake_request_rejects_unsupported_language() -> None:
    with pytest.raises(IntakeValidationError, match="Supported values: et, ru, en"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {
                    "original_text": "text",
                    "language": "de",
                    "title_hint": "title",
                },
            }
        )


def test_parse_story_intake_request_requires_narrative_title_hint() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.title_hint"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {"original_text": "text", "language": "en"},
            }
        )


def test_build_story_intake_response_contract_shape() -> None:
    payload = build_story_intake_response(
        story_id="story-001",
        status="accepted",
        trace_id="trace-001",
    )
    assert payload == {
        "data": {
            "schema_version": INTAKE_RESPONSE_SCHEMA_VERSION,
            "story_id": "story-001",
            "status": "accepted",
        },
        "trace_id": "trace-001",
    }


def test_parse_story_intake_request_rejects_non_boolean_privacy_fields() -> None:
    with pytest.raises(IntakeValidationError, match="privacy.contains_pii"):
        parse_story_intake_request(
            {
                "schema_version": INTAKE_SCHEMA_VERSION,
                "submitter": {"external_user_id": "opaque-user-123"},
                "narrative": {
                    "original_text": "text",
                    "language": "en",
                    "title_hint": "title",
                },
                "privacy": {"contains_pii": "yes"},
            }
        )


def test_parse_story_intake_request_normalizes_canonical_fields() -> None:
    request = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {"external_user_id": "opaque-user-123"},
            "narrative": {
                "original_text": "text",
                "language": "EN",
                "title_hint": "title",
                "canonical_type": " complaint ",
                "canonical_labels": ["Road", "Road", " Safety "],
            },
        }
    )
    assert request.narrative.language == "en"
    assert request.narrative.canonical_type == "complaint"
    assert request.narrative.canonical_labels == ("road", "safety")

