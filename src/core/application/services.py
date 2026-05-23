from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
import logging
from typing import Protocol
from typing import Mapping
from uuid import uuid4

from core.domain import (
    HealthRepository,
    IdempotencyRecord,
    IdempotencyRepository,
    SignalProfileRecord,
    SignalProfileRepository,
    StoryLifecycleStatus,
    StoryRecord,
    StoryRepository,
    StorySignalStore,
)
from core.redaction import redact_pii
from core.geo import GeoService
from core.domain.narrative_i18n import narrative_v2_complete, story_primary_title
from core.intake import GptSignalsBlock, StoryIntakeRequest
from core.logging_setup import StoryDebugLogger, open_story_debug_logger
from core.profile import (
    infer_signals_from_canonical,
    normalize_signal_map,
    validate_profile_minimum_quality,
)

logger = logging.getLogger(__name__)


def _backend_from_repository_name(name: str) -> str:
    lower = name.lower()
    if "supabase" in lower:
        return "supabase"
    if "sqlite" in lower:
        return "sqlite"
    if "inmemory" in lower:
        return "in_memory"
    return "unknown"


@dataclass(frozen=True)
class HealthService:
    repository: HealthRepository

    def get_status(self) -> str:
        """Return health status for API or orchestration layer."""
        return self.repository.get_health().status


class StoryEmbeddingStore(Protocol):
    def save_story_embedding(
        self,
        *,
        story_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        """Persist deterministic story-level embedding payload."""


GPT_CLASSIFIER_POLICY_VERSION = "gpt.story_classifier.v1"
GPT_SIGNALS_SOURCE = "gpt_intake_v1"


def _gpt_signals_json(gpt_signals: GptSignalsBlock) -> dict[str, str]:
    payload: dict[str, str] = {"source": GPT_SIGNALS_SOURCE}
    if gpt_signals.severity is not None:
        payload["severity"] = gpt_signals.severity
    if gpt_signals.impact_estimation is not None:
        payload["impact_estimation"] = gpt_signals.impact_estimation
    if gpt_signals.problem_status is not None:
        payload["problem_status"] = gpt_signals.problem_status
    return payload


@dataclass(frozen=True)
class StoryIntakeService:
    repository: StoryRepository
    idempotency_repository: IdempotencyRepository
    geo_service: GeoService | None = None
    story_embedding_store: StoryEmbeddingStore | None = None
    story_signal_store: StorySignalStore | None = None
    log_debug_dir: str | None = None

    def _persist_gpt_classifier_signals(
        self, *, story_id: str, gpt_signals: GptSignalsBlock
    ) -> None:
        if self.story_signal_store is None:
            return
        try:
            self.story_signal_store.save_signals(
                story_id,
                GPT_CLASSIFIER_POLICY_VERSION,
                _gpt_signals_json(gpt_signals),
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "intake.gpt_signals_persist_failed",
                extra={
                    "story_id": story_id,
                    "policy": GPT_CLASSIFIER_POLICY_VERSION,
                    "error": str(exc),
                },
            )

    def create_story(
        self, request: StoryIntakeRequest, *, idempotency_key: str | None = None
    ) -> StoryRecord:
        contains_pii = (
            request.privacy.contains_pii if request.privacy is not None else False
        )
        text_preview = redact_pii(
            request.narrative.original_text.strip()[:50], contains_pii
        )
        logger.debug(
            "intake.create_story_start",
            extra={
                "idempotency_key": idempotency_key or "-",
                "lang": request.narrative.language,
                "text_len": len(request.narrative.original_text),
                "text_preview": text_preview,
            },
        )
        if idempotency_key:
            existing_key = self.idempotency_repository.get_by_key(idempotency_key)
            if existing_key is not None:
                logger.debug(
                    "intake.idempotency_check",
                    extra={
                        "idempotency_key": idempotency_key,
                        "result": "hit",
                        "story_id": existing_key.story_id,
                    },
                )
                existing_story = self.repository.get_story(existing_key.story_id)
                if existing_story is not None:
                    return existing_story
            else:
                logger.debug(
                    "intake.idempotency_check",
                    extra={"idempotency_key": idempotency_key, "result": "miss"},
                )

        now = datetime.now(UTC)
        story_id = str(uuid4())
        with open_story_debug_logger(story_id, self.log_debug_dir) as debug_logger:
            geo = (
                self.geo_service.resolve_for_story(
                    request.narrative.location_query,
                    debug_logger=debug_logger,
                )
                if self.geo_service is not None
                else None
            )
            if geo is None and debug_logger is not None and self.geo_service is None:
                debug_logger.log("geo", "skipped", {"reason": "geo_service_disabled"})
            if geo is None:
                logger.debug("intake.geo_skip", extra={"reason": "no_geo_or_not_resolved"})
            else:
                logger.debug(
                    "intake.geo_resolved",
                    extra={
                        "geo_label": geo.normalized_label,
                        "geo_provider": geo.provider,
                        "geo_confidence": geo.confidence,
                    },
                )
            consistency_notes = (
                request.live_story_context.consistency_notes
                if request.live_story_context is not None
                else None
            )
            record = StoryRecord(
                story_id=story_id,
            schema_version=request.schema_version,
            narrative_original_text=request.narrative.original_text,
            submitter_external_user_id=request.submitter.external_user_id,
            submitter_identity_issuer=request.submitter.identity_issuer,
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            created_at=now,
            updated_at=now,
            narrative_language=request.narrative.language,
            narrative_title=dict(request.narrative.title),
            narrative_description=dict(request.narrative.description),
            narrative_summary=(
                dict(request.narrative.summary)
                if request.narrative.summary is not None
                else None
            ),
            narrative_session_language=request.narrative.session_language,
            narrative_consistency_notes=consistency_notes,
            narrative_canonical_type=request.narrative.canonical_type,
            narrative_canonical_labels=request.narrative.canonical_labels,
            geo=geo,
            origin_source=request.origin.source if request.origin is not None else None,
            origin_conversation_id=(
                request.origin.conversation_id if request.origin is not None else None
            ),
            origin_tool_call_id=(
                request.origin.tool_call_id if request.origin is not None else None
            ),
            privacy_contains_pii=contains_pii,
            privacy_redaction_requested=(
                request.privacy.redaction_requested
                if request.privacy is not None
                else False
            ),
            )
            repository_class = self.repository.__class__.__name__
            backend_hint = _backend_from_repository_name(repository_class)
            logger.info(
                "intake.persistence_save_start backend=%s repository_class=%s stage=%s",
                backend_hint,
                repository_class,
                "application.intake.save_story",
                extra={
                    "story_id": record.story_id,
                    "backend": backend_hint,
                    "repository_class": repository_class,
                    "stage": "application.intake.save_story",
                    "outcome": "start",
                },
            )
            saved = self.repository.save_story(record)
            logger.info(
                "intake.persistence_save_done backend=%s repository_class=%s stage=%s",
                backend_hint,
                repository_class,
                "application.intake.save_story",
                extra={
                    "story_id": saved.story_id,
                    "status": saved.lifecycle_status.value,
                    "backend": backend_hint,
                    "repository_class": repository_class,
                    "stage": "application.intake.save_story",
                    "outcome": "success",
                },
            )
            logger.debug(
                "intake.story_saved",
                extra={"story_id": saved.story_id, "status": saved.lifecycle_status.value},
            )
            if idempotency_key:
                self.idempotency_repository.save(
                    IdempotencyRecord(
                        key=idempotency_key, story_id=saved.story_id, created_at=now
                    )
                )
                logger.info(
                    "intake.idempotency_save_done backend=%s repository_class=%s stage=%s",
                    backend_hint,
                    self.idempotency_repository.__class__.__name__,
                    "application.intake.idempotency",
                    extra={
                        "story_id": saved.story_id,
                        "idempotency_key": idempotency_key,
                        "backend": backend_hint,
                        "repository_class": self.idempotency_repository.__class__.__name__,
                        "stage": "application.intake.idempotency",
                        "outcome": "success",
                    },
                )
            final_story = self.advance_story_readiness(
                story_id=saved.story_id,
                narrative_complete=narrative_v2_complete(
                    original_text=saved.narrative_original_text,
                    language=request.narrative.language,
                    title=request.narrative.title,
                    description=request.narrative.description,
                    session_language=request.narrative.session_language,
                ),
            )
            logger.debug(
                "intake.lifecycle_advance_done",
                extra={
                    "story_id": final_story.story_id,
                    "status": final_story.lifecycle_status.value,
                },
            )
            if isinstance(debug_logger, StoryDebugLogger):
                debug_logger.log(
                    "intake",
                    "story_accepted",
                    {
                        "lifecycle": final_story.lifecycle_status.value,
                        "language": final_story.narrative_language or "",
                        "session_language": final_story.narrative_session_language or "",
                        "has_canonical_type": bool(final_story.narrative_canonical_type),
                    },
                )
            if self.story_embedding_store is not None:
                canonical_source = _canonical_story_embedding_source(final_story)
                checksum = sha256(canonical_source.encode("utf-8")).hexdigest()
                self.story_embedding_store.save_story_embedding(
                    story_id=final_story.story_id,
                    model_name="deterministic-baseline-v1",
                    embedding_vector=_build_embedding_vector(canonical_source),
                    source_checksum=checksum,
                    embedding_policy_version=STORY_EMBEDDING_POLICY_VERSION,
                )
                logger.debug(
                    "intake.embedding_computed",
                    extra={
                        "story_id": final_story.story_id,
                        "model": "deterministic-baseline-v1",
                        "checksum8": checksum[:8],
                    },
                )
            if request.gpt_signals is not None:
                self._persist_gpt_classifier_signals(
                    story_id=final_story.story_id,
                    gpt_signals=request.gpt_signals,
                )
            return final_story

    def advance_story_readiness(
        self, *, story_id: str, narrative_complete: bool
    ) -> StoryRecord:
        current = self.repository.get_story(story_id)
        if current is None:
            raise ValueError(f"Unknown story_id: {story_id}.")
        repository_class = self.repository.__class__.__name__
        backend_hint = _backend_from_repository_name(repository_class)
        logger.info(
            "intake.persistence_status_update_start backend=%s repository_class=%s stage=%s",
            backend_hint,
            repository_class,
            "application.intake.advance_story_readiness",
            extra={
                "story_id": story_id,
                "current_status": current.lifecycle_status.value,
                "backend": backend_hint,
                "repository_class": repository_class,
                "stage": "application.intake.advance_story_readiness",
                "outcome": "start",
            },
        )

        next_status = current.lifecycle_status
        if current.lifecycle_status is StoryLifecycleStatus.ACCEPTED:
            next_status = (
                StoryLifecycleStatus.READY_FOR_PROFILE
                if narrative_complete
                else StoryLifecycleStatus.PARTIAL_READY
            )
        elif (
            current.lifecycle_status is StoryLifecycleStatus.PARTIAL_READY
            and narrative_complete
        ):
            next_status = StoryLifecycleStatus.READY_FOR_PROFILE
        elif (
            current.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
            and not narrative_complete
        ):
            raise ValueError("Cannot regress story lifecycle from READY_FOR_PROFILE.")

        if next_status is current.lifecycle_status:
            logger.info(
                "intake.persistence_status_update_done backend=%s repository_class=%s stage=%s",
                backend_hint,
                repository_class,
                "application.intake.advance_story_readiness",
                extra={
                    "story_id": current.story_id,
                    "current_status": current.lifecycle_status.value,
                    "next_status": next_status.value,
                    "backend": backend_hint,
                    "repository_class": repository_class,
                    "stage": "application.intake.advance_story_readiness",
                    "outcome": "success",
                },
            )
            return current

        updated = StoryRecord(
            story_id=current.story_id,
            schema_version=current.schema_version,
            narrative_original_text=current.narrative_original_text,
            submitter_external_user_id=current.submitter_external_user_id,
            submitter_identity_issuer=current.submitter_identity_issuer,
            lifecycle_status=next_status,
            created_at=current.created_at,
            updated_at=datetime.now(UTC),
            narrative_language=current.narrative_language,
            narrative_title=current.narrative_title,
            narrative_description=current.narrative_description,
            narrative_summary=current.narrative_summary,
            narrative_session_language=current.narrative_session_language,
            narrative_consistency_notes=current.narrative_consistency_notes,
            narrative_canonical_type=current.narrative_canonical_type,
            narrative_canonical_labels=current.narrative_canonical_labels,
            geo=current.geo,
            origin_source=current.origin_source,
            origin_conversation_id=current.origin_conversation_id,
            origin_tool_call_id=current.origin_tool_call_id,
            privacy_contains_pii=current.privacy_contains_pii,
            privacy_redaction_requested=current.privacy_redaction_requested,
        )
        result = self.repository.save_story(updated)
        logger.info(
            "intake.persistence_status_update_done backend=%s repository_class=%s stage=%s",
            backend_hint,
            repository_class,
            "application.intake.advance_story_readiness",
            extra={
                "story_id": result.story_id,
                "current_status": current.lifecycle_status.value,
                "next_status": result.lifecycle_status.value,
                "backend": backend_hint,
                "repository_class": repository_class,
                "stage": "application.intake.advance_story_readiness",
                "outcome": "success",
            },
        )
        return result


@dataclass(frozen=True)
class SignalProfileService:
    repository: SignalProfileRepository

    def create_or_update_profile(
        self,
        *,
        story_id: str,
        narrative_text: str,
        user_asserted: Mapping[str, str] | None = None,
    ) -> SignalProfileRecord:
        latest = self.repository.get_latest(story_id)
        version = 1 if latest is None else latest.version + 1
        profile = SignalProfileRecord(
            story_id=story_id,
            version=version,
            user_asserted=normalize_signal_map(dict(user_asserted or {})),
            system_inferred=infer_signals_from_canonical(None, (), None),
            created_at=datetime.now(UTC),
        )
        return self.repository.save_version(profile)

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        return self.repository.get_versions(story_id)

    def validate_quality(self, profile: SignalProfileRecord) -> list[str]:
        return validate_profile_minimum_quality(profile)


def _build_embedding_vector(text: str) -> tuple[float, ...]:
    digest = sha256(text.encode("utf-8")).digest()
    vector: list[float] = []
    for idx in range(0, 16, 2):
        value = int.from_bytes(digest[idx : idx + 2], byteorder="big", signed=False)
        vector.append(round(value / 65535.0, 6))
    return tuple(vector)


STORY_EMBEDDING_POLICY_VERSION = "m2.story_embedding_policy.v1"


def _canonical_story_embedding_source(story: StoryRecord) -> str:
    labels = ",".join(story.narrative_canonical_labels)
    redacted_text = redact_pii(
        story.narrative_original_text.strip(), story.privacy_contains_pii
    )
    return "|".join(
        [
            f"story_id={story.story_id}",
            f"lang={story.narrative_language or ''}",
            f"title={story_primary_title(narrative_title=story.narrative_title, narrative_session_language=story.narrative_session_language, narrative_language=story.narrative_language)}",
            f"type={story.narrative_canonical_type or ''}",
            f"labels={labels}",
            f"text={redacted_text}",
        ]
    )

