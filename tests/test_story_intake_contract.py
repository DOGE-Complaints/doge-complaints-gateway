from __future__ import annotations

import pytest

from core.intake import (
    INTAKE_RESPONSE_SCHEMA_VERSION,
    INTAKE_SCHEMA_VERSION,
    INTAKE_SCHEMA_VERSION_V1,
    IntakeValidationError,
    build_story_intake_response,
    parse_story_intake_request,
)
from tests.intake_v2_fixtures import narrative_dict, valid_v2_intake_payload


def test_parse_story_intake_request_valid_payload() -> None:
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            origin={
                "source": "openai_gpt_action",
                "conversation_id": "conv-1",
                "tool_call_id": "call-1",
            },
            privacy={"contains_pii": False, "redaction_requested": True},
            live_story_context={"consistency_notes": "User clarified scope."},
        )
    )
    assert request.schema_version == INTAKE_SCHEMA_VERSION
    assert request.submitter.external_user_id == "opaque-user-123"
    assert request.submitter.identity_issuer == "https://idp.example.com/eid"
    assert request.narrative.original_text.startswith("Road is blocked")
    assert request.narrative.session_language == "en"
    assert request.narrative.title["en"] == "Title EN"
    assert request.narrative.description["ru"] == "Описание RU"
    assert request.origin is not None
    assert request.origin.source == "openai_gpt_action"
    assert request.privacy is not None
    assert request.privacy.redaction_requested is True
    assert request.live_story_context is not None
    assert request.live_story_context.consistency_notes == "User clarified scope."


def test_parse_story_intake_request_rejects_v1_schema() -> None:
    payload = valid_v2_intake_payload()
    payload["schema_version"] = INTAKE_SCHEMA_VERSION_V1
    with pytest.raises(IntakeValidationError, match="Migrate clients"):
        parse_story_intake_request(payload)


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
        parse_story_intake_request(valid_v2_intake_payload(submitter={}, merge_submitter=False))


def test_parse_story_intake_request_requires_identity_issuer() -> None:
    with pytest.raises(IntakeValidationError, match="submitter.identity_issuer"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                submitter={"external_user_id": "opaque-user-123"},
                merge_submitter=False,
            )
        )


def test_parse_story_intake_request_requires_narrative_original_text() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.original_text"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "language": "en",
                    "session_language": "en",
                    "title": narrative_dict(),
                    "description": narrative_dict(en="d", et="d", ru="d"),
                },
                merge_narrative=False,
            )
        )


def test_parse_story_intake_request_requires_narrative_language() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.language"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "session_language": "en",
                    "title": narrative_dict(),
                    "description": narrative_dict(en="d", et="d", ru="d"),
                },
                merge_narrative=False,
            )
        )


def test_parse_story_intake_request_requires_session_language() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.session_language"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "language": "en",
                    "title": narrative_dict(),
                    "description": narrative_dict(en="d", et="d", ru="d"),
                },
                merge_narrative=False,
            )
        )


def test_parse_story_intake_request_requires_narrative_title() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.title"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "language": "en",
                    "session_language": "en",
                    "description": narrative_dict(en="d", et="d", ru="d"),
                },
                merge_narrative=False,
            )
        )


def test_parse_story_intake_request_requires_narrative_description() -> None:
    with pytest.raises(IntakeValidationError, match="narrative.description"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "language": "en",
                    "session_language": "en",
                    "title": narrative_dict(),
                },
                merge_narrative=False,
            )
        )


def test_parse_story_intake_request_rejects_unsupported_language() -> None:
    with pytest.raises(IntakeValidationError, match="Supported values: et, ru, en"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "language": "de",
                    "session_language": "en",
                    "title": {"et": "t", "ru": "t", "en": "t"},
                    "description": {"et": "d", "ru": "d", "en": "d"},
                }
            )
        )


def test_parse_story_intake_request_rejects_unsupported_session_language() -> None:
    with pytest.raises(IntakeValidationError, match="Supported values: et, ru, en"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                narrative={
                    "original_text": "text",
                    "language": "en",
                    "session_language": "de",
                    "title": {"et": "t", "ru": "t", "en": "t"},
                    "description": {"et": "d", "ru": "d", "en": "d"},
                }
            )
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
            "intake_notes": {
                "geo_resolved": False,
                "gpt_signals_persisted": True,
            },
        },
        "trace_id": "trace-001",
    }


def test_parse_story_intake_request_rejects_non_boolean_privacy_fields() -> None:
    with pytest.raises(IntakeValidationError, match="privacy.contains_pii"):
        parse_story_intake_request(
            valid_v2_intake_payload(privacy={"contains_pii": "yes"})
        )


def test_parse_story_intake_request_normalizes_canonical_fields() -> None:
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            narrative={
                "original_text": "text",
                "language": "EN",
                "session_language": "en",
                "title": {"et": "t", "ru": "t", "en": "title"},
                "description": {"et": "d", "ru": "d", "en": "d"},
                "canonical_type": " complaint ",
                "canonical_labels": ["Road", "Road", " Safety "],
            }
        )
    )
    assert request.narrative.language == "en"
    assert request.narrative.canonical_type == "complaint"
    assert request.narrative.canonical_labels == ("road", "safety")
