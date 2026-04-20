from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from core.domain import (
    HealthRepository,
    IdempotencyRecord,
    IdempotencyRepository,
    StoryLifecycleStatus,
    StoryRecord,
    StoryRepository,
)
from core.intake import StoryIntakeRequest


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
        record = StoryRecord(
            story_id=str(uuid4()),
            schema_version=request.schema_version,
            narrative_original_text=request.narrative.original_text,
            submitter_external_user_id=request.submitter.external_user_id,
            submitter_identity_issuer=request.submitter.identity_issuer,
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
            created_at=now,
            updated_at=now,
        )
        saved = self.repository.save_story(record)
        if idempotency_key:
            self.idempotency_repository.save(
                IdempotencyRecord(
                    key=idempotency_key, story_id=saved.story_id, created_at=now
                )
            )
        return saved

