from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from core.api.envelope import build_success_envelope


INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v1"
INTAKE_RESPONSE_SCHEMA_VERSION = "m2.story_intake_response.v1"


class IntakeValidationError(ValueError):
    """Raised when Story Intake request payload is invalid."""


@dataclass(frozen=True)
class Submitter:
    external_user_id: str
    identity_issuer: str | None = None


@dataclass(frozen=True)
class Narrative:
    original_text: str
    language: str | None = None
    title_hint: str | None = None
    location_query: str | None = None


@dataclass(frozen=True)
class Origin:
    source: str | None = None
    conversation_id: str | None = None
    tool_call_id: str | None = None


@dataclass(frozen=True)
class Privacy:
    contains_pii: bool = False
    redaction_requested: bool = False


@dataclass(frozen=True)
class LiveStoryContext:
    consistency_notes: str | None = None


@dataclass(frozen=True)
class StoryIntakeRequest:
    schema_version: str
    submitter: Submitter
    narrative: Narrative
    origin: Origin | None = None
    privacy: Privacy | None = None
    live_story_context: LiveStoryContext | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StoryIntakeResponse:
    schema_version: str
    story_id: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _require_non_empty_string(
    payload: Mapping[str, Any], key: str, *, parent: str = "root"
) -> str:
    raw_value = payload.get(key)
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise IntakeValidationError(f"Missing or invalid {parent}.{key}.")
    return raw_value.strip()


def _optional_bool(
    payload: Mapping[str, Any], key: str, *, parent: str = "root"
) -> bool | None:
    raw_value = payload.get(key)
    if raw_value is None:
        return None
    if isinstance(raw_value, bool):
        return raw_value
    raise IntakeValidationError(f"Missing or invalid {parent}.{key}. Expected boolean.")


def parse_story_intake_request(payload: Mapping[str, Any]) -> StoryIntakeRequest:
    schema_version = _require_non_empty_string(payload, "schema_version")
    if schema_version != INTAKE_SCHEMA_VERSION:
        raise IntakeValidationError(
            f"Unsupported schema_version={schema_version!r}. "
            f"Expected {INTAKE_SCHEMA_VERSION!r}."
        )

    submitter_payload = payload.get("submitter")
    if not isinstance(submitter_payload, Mapping):
        raise IntakeValidationError("Missing or invalid root.submitter.")
    external_user_id = _require_non_empty_string(
        submitter_payload, "external_user_id", parent="submitter"
    )
    identity_issuer_raw = submitter_payload.get("identity_issuer")
    identity_issuer = (
        identity_issuer_raw.strip()
        if isinstance(identity_issuer_raw, str) and identity_issuer_raw.strip()
        else None
    )

    narrative_payload = payload.get("narrative")
    if not isinstance(narrative_payload, Mapping):
        raise IntakeValidationError("Missing or invalid root.narrative.")
    original_text = _require_non_empty_string(
        narrative_payload, "original_text", parent="narrative"
    )
    language_raw = narrative_payload.get("language")
    title_hint_raw = narrative_payload.get("title_hint")
    language = language_raw.strip() if isinstance(language_raw, str) and language_raw.strip() else None
    title_hint = (
        title_hint_raw.strip()
        if isinstance(title_hint_raw, str) and title_hint_raw.strip()
        else None
    )
    location_query_raw = narrative_payload.get("location_query")
    location_query = (
        location_query_raw.strip()
        if isinstance(location_query_raw, str) and location_query_raw.strip()
        else None
    )

    origin_payload = payload.get("origin")
    origin: Origin | None = None
    if origin_payload is not None:
        if not isinstance(origin_payload, Mapping):
            raise IntakeValidationError("Missing or invalid root.origin.")
        source_raw = origin_payload.get("source")
        conversation_raw = origin_payload.get("conversation_id")
        tool_call_raw = origin_payload.get("tool_call_id")
        origin = Origin(
            source=source_raw.strip()
            if isinstance(source_raw, str) and source_raw.strip()
            else None,
            conversation_id=conversation_raw.strip()
            if isinstance(conversation_raw, str) and conversation_raw.strip()
            else None,
            tool_call_id=tool_call_raw.strip()
            if isinstance(tool_call_raw, str) and tool_call_raw.strip()
            else None,
        )

    privacy_payload = payload.get("privacy")
    privacy: Privacy | None = None
    if privacy_payload is not None:
        if not isinstance(privacy_payload, Mapping):
            raise IntakeValidationError("Missing or invalid root.privacy.")
        contains_pii = _optional_bool(
            privacy_payload, "contains_pii", parent="privacy"
        )
        redaction_requested = _optional_bool(
            privacy_payload, "redaction_requested", parent="privacy"
        )
        privacy = Privacy(
            contains_pii=contains_pii if contains_pii is not None else False,
            redaction_requested=(
                redaction_requested if redaction_requested is not None else False
            ),
        )

    live_payload = payload.get("live_story_context")
    live_story_context: LiveStoryContext | None = None
    if live_payload is not None:
        if not isinstance(live_payload, Mapping):
            raise IntakeValidationError("Missing or invalid root.live_story_context.")
        notes_raw = live_payload.get("consistency_notes")
        live_story_context = LiveStoryContext(
            consistency_notes=notes_raw.strip()
            if isinstance(notes_raw, str) and notes_raw.strip()
            else None
        )

    return StoryIntakeRequest(
        schema_version=schema_version,
        submitter=Submitter(
            external_user_id=external_user_id, identity_issuer=identity_issuer
        ),
        narrative=Narrative(
            original_text=original_text,
            language=language,
            title_hint=title_hint,
            location_query=location_query,
        ),
        origin=origin,
        privacy=privacy,
        live_story_context=live_story_context,
    )


def build_story_intake_response(
    *,
    story_id: str,
    status: str,
    trace_id: str,
) -> dict[str, Any]:
    contract = StoryIntakeResponse(
        schema_version=INTAKE_RESPONSE_SCHEMA_VERSION,
        story_id=story_id,
        status=status,
    )
    return build_success_envelope(data=contract.as_dict(), trace_id=trace_id).as_dict()

