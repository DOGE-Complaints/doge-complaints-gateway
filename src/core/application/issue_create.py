from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any
from typing import Protocol

from core.domain import StoryRepository
from core.projection import (
    DeterministicStoryToProjectionPolicy,
    IssueProjectionService,
    ProjectionInput,
    StoryToProjectionPolicy,
    build_projection_input_from_draft,
)
from core.promotion import IssuePromotionService, ReviewDecision

DERIVATION_POLICY_VERSION = "m2.spa_issue_derivation.v1"


@dataclass(frozen=True)
class IssueCreateCommand:
    cluster_id: str
    story_ids: tuple[str, ...]
    readiness_score: int
    title: str


@dataclass(frozen=True)
class IssueCreateResult:
    issue_id: str
    status: str
    projection: dict[str, Any]
    policy_version: str = DERIVATION_POLICY_VERSION

    def as_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "status": self.status,
            "projection": self.projection,
            "policy_version": self.policy_version,
        }


class IssueProjectionStore(Protocol):
    def save_projection(
        self,
        *,
        issue_id: str,
        status: str,
        payload: dict[str, object],
        policy_version: str,
    ) -> None:
        """Persist issue projection payload."""


class IssueProjectionEmbeddingStore(Protocol):
    def save_projection_embedding(
        self,
        *,
        issue_id: str,
        model_name: str,
        embedding_vector: tuple[float, ...],
        source_checksum: str,
        embedding_policy_version: str,
    ) -> None:
        """Persist issue projection embedding payload."""


class IssueStoryLinkStore(Protocol):
    def save_issue_story_links(
        self,
        *,
        issue_id: str,
        cluster_id: str,
        story_ids: tuple[str, ...],
    ) -> None:
        """Persist explicit issue->stories linkage for process recovery."""


@dataclass(frozen=True)
class StoryPromotionProjectionBridge:
    story_repository: StoryRepository
    extraction_policy: StoryToProjectionPolicy = field(
        default_factory=DeterministicStoryToProjectionPolicy
    )

    def build_projection_input(
        self,
        *,
        issue_id: str,
        promoted_title: str,
        story_ids: tuple[str, ...],
    ) -> ProjectionInput:
        stories = []
        for story_id in story_ids:
            story = self.story_repository.get_story(story_id)
            if story is None:
                raise ValueError(f"Unknown story_id: {story_id}.")
            stories.append(story)

        narrative_chunks = [story.narrative_original_text.strip() for story in stories if story.narrative_original_text.strip()]
        aggregate_text = " ".join(narrative_chunks) if narrative_chunks else promoted_title
        draft = self.extraction_policy.build_draft(
            promoted_title=promoted_title,
            aggregate_text=aggregate_text,
        )
        return build_projection_input_from_draft(issue_id=issue_id, draft=draft)


@dataclass(frozen=True)
class IssueCreateService:
    promotion_service: IssuePromotionService
    projection_service: IssueProjectionService
    bridge: StoryPromotionProjectionBridge
    issue_projection_store: IssueProjectionStore | None = None
    issue_projection_embedding_store: IssueProjectionEmbeddingStore | None = None
    issue_story_link_store: IssueStoryLinkStore | None = None

    def create_issue(self, command: IssueCreateCommand) -> IssueCreateResult:
        if not command.cluster_id.strip():
            raise ValueError("cluster_id must be non-empty.")
        if not command.story_ids:
            raise ValueError("story_ids must contain at least one story id.")
        if not command.title.strip():
            raise ValueError("title must be non-empty.")

        candidate = self.promotion_service.create_candidate(
            cluster_id=command.cluster_id.strip(),
            story_ids=tuple(story_id.strip() for story_id in command.story_ids if story_id.strip()),
            readiness_score=command.readiness_score,
            title=command.title.strip(),
        )
        self.promotion_service.submit_for_review(candidate.candidate_id)
        self.promotion_service.start_review(candidate.candidate_id)
        promoted = self.promotion_service.record_review(
            candidate_id=candidate.candidate_id,
            actor="system",
            decision=ReviewDecision.APPROVE,
            rationale="http_create_issue_auto_promote",
        )

        projection_input = self.bridge.build_projection_input(
            issue_id=promoted.candidate_id,
            promoted_title=promoted.title,
            story_ids=promoted.story_ids,
        )
        projection = self.projection_service.project(projection_input)
        projection_payload = projection.to_public_dict()
        if self.issue_story_link_store is not None:
            self.issue_story_link_store.save_issue_story_links(
                issue_id=promoted.candidate_id,
                cluster_id=promoted.cluster_id,
                story_ids=promoted.story_ids,
            )
        if self.issue_projection_store is not None:
            self.issue_projection_store.save_projection(
                issue_id=promoted.candidate_id,
                status=promoted.status.value,
                payload=projection_payload,
                policy_version=DERIVATION_POLICY_VERSION,
            )
        if self.issue_projection_embedding_store is not None:
            checksum = sha256(
                _canonical_issue_embedding_source(projection_payload).encode("utf-8")
            ).hexdigest()
            self.issue_projection_embedding_store.save_projection_embedding(
                issue_id=promoted.candidate_id,
                model_name="deterministic-baseline-v1",
                embedding_vector=_build_embedding_vector_from_projection(
                    projection_payload
                ),
                source_checksum=checksum,
                embedding_policy_version=ISSUE_EMBEDDING_POLICY_VERSION,
            )

        return IssueCreateResult(
            issue_id=promoted.candidate_id,
            status=promoted.status.value,
            projection=projection_payload,
        )


def _build_embedding_vector_from_projection(
    projection_payload: dict[str, object],
) -> tuple[float, ...]:
    serialized = _canonical_issue_embedding_source(projection_payload)
    digest = sha256(serialized.encode("utf-8")).digest()
    vector: list[float] = []
    for idx in range(0, 16, 2):
        value = int.from_bytes(digest[idx : idx + 2], byteorder="big", signed=False)
        vector.append(round(value / 65535.0, 6))
    return tuple(vector)


ISSUE_EMBEDDING_POLICY_VERSION = "m2.issue_embedding_policy.v1"


def _canonical_issue_embedding_source(projection_payload: dict[str, object]) -> str:
    issue_id = str(projection_payload.get("id", ""))
    issue_type = str(projection_payload.get("type", ""))
    labels = projection_payload.get("labels")
    if isinstance(labels, list):
        labels_value = ",".join(str(item) for item in labels)
    else:
        labels_value = ""
    title = projection_payload.get("title")
    summary = projection_payload.get("summary")
    description = projection_payload.get("description")
    return "|".join(
        [
            f"id={issue_id}",
            f"type={issue_type}",
            f"labels={labels_value}",
            f"title={json.dumps(title, sort_keys=True, ensure_ascii=True)}",
            f"summary={json.dumps(summary, sort_keys=True, ensure_ascii=True)}",
            f"description={json.dumps(description, sort_keys=True, ensure_ascii=True)}",
        ]
    )
