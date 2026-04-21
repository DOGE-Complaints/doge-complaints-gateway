from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
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
)
from core.geo import GeoService
from core.intake import StoryIntakeRequest
from core.profile import (
    infer_signals_from_narrative,
    normalize_signal_map,
    validate_profile_minimum_quality,
)


@dataclass(frozen=True)
class HealthService:
    repository: HealthRepository

    def get_status(self) -> str:
        """Return health status for API or orchestration layer."""
        return self.repository.get_health().status


@dataclass(frozen=True)
class StoryIntakeService:
    repository: StoryRepository
    idempotency_repository: IdempotencyRepository
    geo_service: GeoService | None = None

    def create_story(
        self, request: StoryIntakeRequest, *, idempotency_key: str | None = None
    ) -> StoryRecord:
        if idempotency_key:
            existing_key = self.idempotency_repository.get_by_key(idempotency_key)
            if existing_key is not None:
                existing_story = self.repository.get_story(existing_key.story_id)
                if existing_story is not None:
                    return existing_story

        now = datetime.now(UTC)
        geo = (
            self.geo_service.resolve_for_story(request.narrative.location_query)
            if self.geo_service is not None
            else None
        )
        record = StoryRecord(
            story_id=str(uuid4()),
            schema_version=request.schema_version,
            narrative_original_text=request.narrative.original_text,
            submitter_external_user_id=request.submitter.external_user_id,
            submitter_identity_issuer=request.submitter.identity_issuer,
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            created_at=now,
            updated_at=now,
            geo=geo,
            origin_source=request.origin.source if request.origin is not None else None,
            origin_conversation_id=(
                request.origin.conversation_id if request.origin is not None else None
            ),
            origin_tool_call_id=(
                request.origin.tool_call_id if request.origin is not None else None
            ),
            privacy_contains_pii=(
                request.privacy.contains_pii if request.privacy is not None else False
            ),
            privacy_redaction_requested=(
                request.privacy.redaction_requested
                if request.privacy is not None
                else False
            ),
        )
        saved = self.repository.save_story(record)
        if idempotency_key:
            self.idempotency_repository.save(
                IdempotencyRecord(
                    key=idempotency_key, story_id=saved.story_id, created_at=now
                )
            )
        return self.advance_story_readiness(
            story_id=saved.story_id,
            narrative_complete=bool(
                saved.narrative_original_text.strip()
                and request.narrative.language
                and request.narrative.title_hint
            ),
        )

    def advance_story_readiness(
        self, *, story_id: str, narrative_complete: bool
    ) -> StoryRecord:
        current = self.repository.get_story(story_id)
        if current is None:
            raise ValueError(f"Unknown story_id: {story_id}.")

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
            geo=current.geo,
            origin_source=current.origin_source,
            origin_conversation_id=current.origin_conversation_id,
            origin_tool_call_id=current.origin_tool_call_id,
            privacy_contains_pii=current.privacy_contains_pii,
            privacy_redaction_requested=current.privacy_redaction_requested,
        )
        return self.repository.save_story(updated)


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
            system_inferred=infer_signals_from_narrative(narrative_text),
            created_at=datetime.now(UTC),
        )
        return self.repository.save_version(profile)

    def get_versions(self, story_id: str) -> list[SignalProfileRecord]:
        return self.repository.get_versions(story_id)

    def validate_quality(self, profile: SignalProfileRecord) -> list[str]:
        return validate_profile_minimum_quality(profile)

