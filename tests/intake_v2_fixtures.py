from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from core.domain import StoryLifecycleStatus, StoryRecord
from core.intake import INTAKE_SCHEMA_VERSION
from gw_ssr_16_node_schema import active_node_schema_binding

_I18N = {
    "et": "Pealkiri ET",
    "ru": "Заголовок RU",
    "en": "Title EN",
}
_DESC = {
    "et": "Kirjeldus ET",
    "ru": "Описание RU",
    "en": "Description EN",
}


def narrative_dict(
    *,
    et: str = "t",
    ru: str = "t",
    en: str = "t",
) -> dict[str, str]:
    return {"et": et, "ru": ru, "en": en}


def valid_v2_intake_payload(
    *,
    merge_narrative: bool = True,
    merge_submitter: bool = True,
    **overrides: Any,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {
            "external_user_id": "opaque-user-123",
            "identity_issuer": "https://idp.example.com/eid",
        },
        "narrative": {
            "original_text": "Road is blocked near district center.",
            "language": "en",
            "session_language": "en",
            "title": dict(_I18N),
            "description": dict(_DESC),
        },
    }
    for key, value in overrides.items():
        if key == "narrative" and isinstance(value, dict):
            payload["narrative"] = (
                {**payload["narrative"], **value} if merge_narrative else value
            )
        elif key == "submitter" and isinstance(value, dict):
            payload["submitter"] = (
                {**payload["submitter"], **value} if merge_submitter else value
            )
        else:
            payload[key] = value
    if "schema_binding" not in overrides:
        payload["schema_binding"] = active_node_schema_binding()
    return payload


def valid_v2_stash_payload(**overrides: Any) -> dict[str, Any]:
    """StoryDraftStashRequest wire shape — no submitter (GW-DRAFT-05)."""
    payload = valid_v2_intake_payload(**overrides)
    payload.pop("submitter", None)
    return payload


def intake_payload_simple(
    *,
    external_user_id: str = "opaque-user-001",
    original_text: str = "Sample narrative text.",
    title_en: str = "Title EN",
    language: str = "en",
    identity_issuer: str = "https://idp.example.com/eid",
    **extra: Any,
) -> dict[str, Any]:
    return valid_v2_intake_payload(
        submitter={"external_user_id": external_user_id, "identity_issuer": identity_issuer},
        narrative={
            "original_text": original_text,
            "language": language,
            "session_language": language,
            "title": narrative_dict(en=title_en, et=title_en, ru=title_en),
            "description": narrative_dict(
                en=original_text, et=original_text, ru=original_text
            ),
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "broken_infrastructure"],
        },
        **extra,
    )


def make_story_record(**overrides: Any) -> StoryRecord:
    now = datetime.now(UTC)
    defaults: dict[str, Any] = {
        "story_id": "story-test-001",
        "schema_version": INTAKE_SCHEMA_VERSION,
        "narrative_original_text": "Sample narrative text.",
        "submitter_external_user_id": "opaque-user-123",
        "submitter_identity_issuer": "https://idp.example.com/eid",
        "lifecycle_status": StoryLifecycleStatus.READY_FOR_PROFILE,
        "created_at": now,
        "updated_at": now,
        "narrative_language": "en",
        "narrative_title": narrative_dict(en="Sample title"),
        "narrative_description": narrative_dict(en="Sample description"),
        "narrative_session_language": "en",
    }
    defaults.update(overrides)
    return StoryRecord(**defaults)
