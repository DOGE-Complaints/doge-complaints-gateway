from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

from core.api.envelope import build_success_envelope
from core.domain.narrative_i18n import (
    I18N_LANGS,
    parse_optional_i18n_dict,
    parse_required_i18n_dict,
)
from core.taxonomy import (
    AxisLabelEntry,
    canonical_flat_labels_from_taxonomy,
    parse_taxonomy_payload,
)


INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"
INTAKE_SCHEMA_VERSION_V1 = "m2.story_intake_envelope.v1"
INTAKE_RESPONSE_SCHEMA_VERSION = "m2.story_intake_response.v1"
# Legacy value for pre-GW-DRAFT-05 drafts only; stripped in _normalize_stored_draft_payload (T02).
_LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID = "__stash_pending_author__"


class IntakeValidationError(ValueError):
    """Raised when Story Intake request payload is invalid."""


@dataclass(frozen=True)
class Submitter:
    external_user_id: str
    identity_issuer: str


@dataclass(frozen=True)
class Narrative:
    original_text: str
    language: str
    title: dict[str, str]
    description: dict[str, str]
    session_language: str
    location_query: str | None = None
    canonical_type: str | None = None
    canonical_labels: tuple[str, ...] = ()
    taxonomy: tuple[AxisLabelEntry, ...] = ()
    summary: dict[str, str] | None = None
    institution: dict[str, str] | None = None


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


GPT_SIGNAL_SEVERITY_VALUES = frozenset({"LOW", "MEDIUM", "HIGH", "CRITICAL"})
GPT_SIGNAL_IMPACT_VALUES = frozenset({"LOCAL", "DISTRICT", "CITY", "NATIONAL"})
GPT_SIGNAL_PROBLEM_STATUS_VALUES = frozenset(
    {"ONGOING", "RESOLVED", "RECURRING", "UNKNOWN"}
)


@dataclass(frozen=True)
class GptSignalsBlock:
    severity: str | None = None
    impact_estimation: str | None = None
    problem_status: str | None = None


def gpt_signals_block_has_values(block: GptSignalsBlock) -> bool:
    """True when at least one classifier field is set (REQ-42 §2.2 — no empty row)."""
    return (
        block.severity is not None
        or block.impact_estimation is not None
        or block.problem_status is not None
    )


@dataclass(frozen=True)
class StoryDraftStashRequest:
    schema_version: str
    narrative: Narrative
    origin: Origin | None = None
    privacy: Privacy | None = None
    live_story_context: LiveStoryContext | None = None
    gpt_signals: GptSignalsBlock | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StoryIntakeRequest:
    schema_version: str
    submitter: Submitter
    narrative: Narrative
    origin: Origin | None = None
    privacy: Privacy | None = None
    live_story_context: LiveStoryContext | None = None
    gpt_signals: GptSignalsBlock | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntakeNotes:
    geo_resolved: bool
    gpt_signals_persisted: bool

    def as_dict(self) -> dict[str, bool]:
        return {
            "geo_resolved": self.geo_resolved,
            "gpt_signals_persisted": self.gpt_signals_persisted,
        }


@dataclass(frozen=True)
class StoryIntakeResponse:
    schema_version: str
    story_id: str
    status: str
    intake_notes: IntakeNotes | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": self.schema_version,
            "story_id": self.story_id,
            "status": self.status,
        }
        if self.intake_notes is not None:
            payload["intake_notes"] = self.intake_notes.as_dict()
        return payload


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


def _parse_gpt_signal_enum(
    raw_value: object,
    *,
    field_name: str,
    parent: str,
    allowed: frozenset[str],
) -> str | None:
    if raw_value is None:
        return None
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise IntakeValidationError(
            f"Missing or invalid {parent}.{field_name}. Expected one of: "
            f"{', '.join(sorted(allowed))}."
        )
    normalized = raw_value.strip().upper()
    if normalized not in allowed:
        raise IntakeValidationError(
            f"Missing or invalid {parent}.{field_name}. Expected one of: "
            f"{', '.join(sorted(allowed))}."
        )
    return normalized


def _parse_gpt_signals_block(gpt_payload: object) -> GptSignalsBlock:
    if gpt_payload is None:
        return GptSignalsBlock()
    if not isinstance(gpt_payload, Mapping):
        raise IntakeValidationError("Missing or invalid root.gpt_signals.")
    return GptSignalsBlock(
        severity=_parse_gpt_signal_enum(
            gpt_payload.get("severity"),
            field_name="severity",
            parent="gpt_signals",
            allowed=GPT_SIGNAL_SEVERITY_VALUES,
        ),
        impact_estimation=_parse_gpt_signal_enum(
            gpt_payload.get("impact_estimation"),
            field_name="impact_estimation",
            parent="gpt_signals",
            allowed=GPT_SIGNAL_IMPACT_VALUES,
        ),
        problem_status=_parse_gpt_signal_enum(
            gpt_payload.get("problem_status"),
            field_name="problem_status",
            parent="gpt_signals",
            allowed=GPT_SIGNAL_PROBLEM_STATUS_VALUES,
        ),
    )


def _parse_language_code(raw: str, *, field_name: str, parent: str) -> str:
    normalized = raw.strip().lower()
    if normalized not in I18N_LANGS:
        raise IntakeValidationError(
            f"Missing or invalid {parent}.{field_name}. Supported values: et, ru, en."
        )
    return normalized


def _parse_story_envelope_body(payload: Mapping[str, Any]) -> tuple[
    str,
    Narrative,
    Origin | None,
    Privacy | None,
    LiveStoryContext | None,
    GptSignalsBlock | None,
]:
    schema_version = _require_non_empty_string(payload, "schema_version")
    if schema_version == INTAKE_SCHEMA_VERSION_V1:
        raise IntakeValidationError(
            f"Unsupported schema_version={schema_version!r}. "
            f"Migrate clients to {INTAKE_SCHEMA_VERSION!r} (multilingual title/description)."
        )
    if schema_version != INTAKE_SCHEMA_VERSION:
        raise IntakeValidationError(
            f"Unsupported schema_version={schema_version!r}. "
            f"Expected {INTAKE_SCHEMA_VERSION!r}."
        )

    narrative_payload = payload.get("narrative")
    if not isinstance(narrative_payload, Mapping):
        raise IntakeValidationError("Missing or invalid root.narrative.")
    original_text = _require_non_empty_string(
        narrative_payload, "original_text", parent="narrative"
    )
    language = _parse_language_code(
        _require_non_empty_string(narrative_payload, "language", parent="narrative"),
        field_name="language",
        parent="narrative",
    )
    session_language = _parse_language_code(
        _require_non_empty_string(
            narrative_payload, "session_language", parent="narrative"
        ),
        field_name="session_language",
        parent="narrative",
    )
    title_payload = narrative_payload.get("title")
    if title_payload is None:
        raise IntakeValidationError("Missing or invalid narrative.title.")
    description_payload = narrative_payload.get("description")
    if description_payload is None:
        raise IntakeValidationError("Missing or invalid narrative.description.")
    try:
        title = parse_required_i18n_dict(title_payload, field_name="title", parent="narrative")
        description = parse_required_i18n_dict(
            description_payload, field_name="description", parent="narrative"
        )
        summary = parse_optional_i18n_dict(
            narrative_payload.get("summary"), field_name="summary", parent="narrative"
        )
        institution = parse_optional_i18n_dict(
            narrative_payload.get("institution"),
            field_name="institution",
            parent="narrative",
        )
    except ValueError as exc:
        raise IntakeValidationError(str(exc)) from exc

    location_query_raw = narrative_payload.get("location_query")
    location_query = (
        location_query_raw.strip()
        if isinstance(location_query_raw, str) and location_query_raw.strip()
        else None
    )
    canonical_type_raw = narrative_payload.get("canonical_type")
    canonical_type = (
        canonical_type_raw.strip()
        if isinstance(canonical_type_raw, str) and canonical_type_raw.strip()
        else None
    )
    canonical_labels_raw = narrative_payload.get("canonical_labels")
    canonical_labels: tuple[str, ...] = ()
    if canonical_labels_raw is not None:
        if not isinstance(canonical_labels_raw, (list, tuple)):
            raise IntakeValidationError(
                "Missing or invalid narrative.canonical_labels. Expected array."
            )
        normalized_labels: list[str] = []
        for idx, label in enumerate(canonical_labels_raw):
            if not isinstance(label, str) or not label.strip():
                raise IntakeValidationError(
                    f"Missing or invalid narrative.canonical_labels[{idx}]."
                )
            normalized_labels.append(label.strip().lower())
        canonical_labels = tuple(dict.fromkeys(normalized_labels))

    taxonomy: tuple[AxisLabelEntry, ...] = ()
    taxonomy_raw = narrative_payload.get("taxonomy")
    if taxonomy_raw is not None:
        if isinstance(taxonomy_raw, Mapping):
            try:
                taxonomy = parse_taxonomy_payload(taxonomy_raw)
            except ValueError as exc:
                raise IntakeValidationError(str(exc)) from exc
        elif isinstance(taxonomy_raw, (list, tuple)) and not taxonomy_raw:
            taxonomy = ()
        else:
            raise IntakeValidationError(
                "Missing or invalid narrative.taxonomy. Expected object."
            )
        if taxonomy and not canonical_labels:
            canonical_labels = canonical_flat_labels_from_taxonomy(taxonomy)

    narrative = Narrative(
        original_text=original_text,
        language=language,
        title=title,
        description=description,
        session_language=session_language,
        location_query=location_query,
        canonical_type=canonical_type,
        canonical_labels=canonical_labels,
        taxonomy=taxonomy,
        summary=summary,
        institution=institution,
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

    gpt_signals: GptSignalsBlock | None = None
    if "gpt_signals" in payload:
        parsed_gpt_signals = _parse_gpt_signals_block(payload.get("gpt_signals"))
        if gpt_signals_block_has_values(parsed_gpt_signals):
            gpt_signals = parsed_gpt_signals

    return (
        schema_version,
        narrative,
        origin,
        privacy,
        live_story_context,
        gpt_signals,
    )


def parse_story_intake_request(payload: Mapping[str, Any]) -> StoryIntakeRequest:
    (
        schema_version,
        narrative,
        origin,
        privacy,
        live_story_context,
        gpt_signals,
    ) = _parse_story_envelope_body(payload)
    submitter_payload = payload.get("submitter")
    if not isinstance(submitter_payload, Mapping):
        raise IntakeValidationError("Missing or invalid root.submitter.")
    external_user_id = _require_non_empty_string(
        submitter_payload, "external_user_id", parent="submitter"
    )
    identity_issuer = _require_non_empty_string(
        submitter_payload, "identity_issuer", parent="submitter"
    )
    return StoryIntakeRequest(
        schema_version=schema_version,
        submitter=Submitter(
            external_user_id=external_user_id,
            identity_issuer=identity_issuer,
        ),
        narrative=narrative,
        origin=origin,
        privacy=privacy,
        live_story_context=live_story_context,
        gpt_signals=gpt_signals,
    )


def parse_story_draft_stash_request(payload: Mapping[str, Any]) -> StoryDraftStashRequest:
    """Validate GPT stash payload (StoryDraftStashRequest) — submitter omitted by design."""
    if "submitter" in payload:
        raise IntakeValidationError(
            "root.submitter must be omitted for story draft stash."
        )
    (
        schema_version,
        narrative,
        origin,
        privacy,
        live_story_context,
        gpt_signals,
    ) = _parse_story_envelope_body(payload)
    return StoryDraftStashRequest(
        schema_version=schema_version,
        narrative=narrative,
        origin=origin,
        privacy=privacy,
        live_story_context=live_story_context,
        gpt_signals=gpt_signals,
    )


def _normalize_stored_draft_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Strip legacy placeholder submitter from pre-GW-DRAFT-05 drafts (T02 tolerant read)."""
    normalized = dict(payload)
    submitter = normalized.get("submitter")
    if isinstance(submitter, Mapping):
        ext = submitter.get("external_user_id")
        if ext == _LEGACY_STASH_PLACEHOLDER_EXTERNAL_USER_ID:
            normalized.pop("submitter", None)
    return normalized


def parse_stored_draft_stash_request(payload: Mapping[str, Any]) -> StoryDraftStashRequest:
    """Parse draft store payload; tolerates legacy placeholder submitter on submit."""
    return parse_story_draft_stash_request(_normalize_stored_draft_payload(payload))


def intake_request_from_stash_and_submitter(
    stash: StoryDraftStashRequest,
    *,
    submitter: Submitter,
) -> StoryIntakeRequest:
    """Bridge stash → intake at browser submit boundary (GW-DRAFT-05)."""
    return StoryIntakeRequest(
        schema_version=stash.schema_version,
        submitter=submitter,
        narrative=stash.narrative,
        origin=stash.origin,
        privacy=stash.privacy,
        live_story_context=stash.live_story_context,
        gpt_signals=stash.gpt_signals,
    )


def build_story_intake_response(
    *,
    story_id: str,
    status: str,
    trace_id: str,
    geo_resolved: bool = False,
    gpt_signals_persisted: bool | None = None,
) -> dict[str, Any]:
    notes = IntakeNotes(
        geo_resolved=geo_resolved,
        gpt_signals_persisted=(
            gpt_signals_persisted if gpt_signals_persisted is not None else True
        ),
    )
    contract = StoryIntakeResponse(
        schema_version=INTAKE_RESPONSE_SCHEMA_VERSION,
        story_id=story_id,
        status=status,
        intake_notes=notes,
    )
    return build_success_envelope(data=contract.as_dict(), trace_id=trace_id).as_dict()
