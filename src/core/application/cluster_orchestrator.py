from __future__ import annotations

import logging
from dataclasses import dataclass

from core.application.issue_create import IssueCreateCommand, IssueCreateService
from core.cluster import ClusteringEngine, StoryProfileSignals
from core.domain import (
    ClusterMembershipStore,
    StoryLifecycleStatus,
    StoryRecord,
    StoryRepository,
    StorySignalStore,
)
from core.profile import get_signals_for_story
from core.promotion.service import PromotionStateError

logger = logging.getLogger(__name__)


def _signal_policy(signal_source: str) -> str:
    src = signal_source.strip().lower()
    _map = {
        "canonical": "v2.canonical",
        "keyword": "v1.keyword",
        "narrative": "v1.keyword",
        "hybrid": "v2.hybrid",
    }
    return _map.get(src, "v2.canonical")


@dataclass(frozen=True)
class StoryClusterOrchestrator:
    story_repository: StoryRepository
    clustering_engine: ClusteringEngine
    issue_create_service: IssueCreateService
    story_signal_store: StorySignalStore | None = None
    cluster_membership_store: ClusterMembershipStore | None = None

    def _get_or_compute_signals(
        self, story: StoryRecord, signal_source: str, policy: str
    ) -> dict[str, str]:
        if self.story_signal_store is not None:
            cached = self.story_signal_store.get_signals(story.story_id, policy)
            if cached is not None:
                return dict(cached)
        signals = get_signals_for_story(story, signal_source)
        if self.story_signal_store is not None:
            try:
                self.story_signal_store.save_signals(story.story_id, policy, signals)
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "cluster.signal_persist_failed",
                    extra={
                        "story_id": story.story_id,
                        "policy": policy,
                        "error": str(exc),
                    },
                )
        return signals

    def process_story(self, story_id: str) -> str | None:
        target = self.story_repository.get_story(story_id)
        if target is None:
            return None
        if target.lifecycle_status is StoryLifecycleStatus.CLUSTERED:
            logger.info(
                "cluster.skipped_already_clustered",
                extra={"story_id": story_id},
            )
            return None
        if target.lifecycle_status is not StoryLifecycleStatus.READY_FOR_PROFILE:
            logger.warning(
                "cluster.story_not_ready",
                extra={"story_id": story_id, "status": target.lifecycle_status.value},
            )
            return None

        ready_stories = self.story_repository.list_stories_ready_for_clustering()
        if not ready_stories:
            return None

        signal_src = getattr(self.clustering_engine, "signal_source", "canonical")
        id_algorithm = getattr(self.clustering_engine, "id_algorithm", "legacy_hash")
        policy = _signal_policy(signal_src)

        profile_list: list[StoryProfileSignals] = []
        for story in ready_stories:
            inferred = self._get_or_compute_signals(story, signal_src, policy)
            profile_list.append(StoryProfileSignals(story_id=story.story_id, signals=inferred))
        profiles = tuple(profile_list)

        memberships = self.clustering_engine.memberships(
            profiles, id_algorithm=id_algorithm
        )
        if story_id not in memberships:
            return None

        primary = self.clustering_engine.resolved_primary_lens()
        lens_key = primary.value
        cluster_id = memberships[story_id].get(lens_key)
        if cluster_id is None:
            return None

        member_story_ids = tuple(
            profile.story_id
            for profile in profiles
            if memberships.get(profile.story_id, {}).get(lens_key) == cluster_id
        )
        if not member_story_ids:
            return None

        readiness_score, readiness_factors = self.clustering_engine.readiness_for_story(
            story_id=story_id,
            profiles=profiles,
            primary_lens=primary,
            id_algorithm=id_algorithm,
        )

        issue_title = (
            target.narrative_title_hint or f"cluster:{primary.value}:{cluster_id}"
        )
        try:
            result = self.issue_create_service.create_issue(
                IssueCreateCommand(
                    cluster_id=cluster_id,
                    story_ids=member_story_ids,
                    readiness_score=readiness_score,
                    title=issue_title,
                )
            )
        except (ValueError, PromotionStateError) as exc:
            logger.info(
                "cluster.issue_creation_skipped",
                extra={
                    "story_id": story_id,
                    "cluster_id": cluster_id,
                    "lens": primary.value,
                    "readiness_score": readiness_score,
                    "reason": str(exc),
                },
            )
            return None

        issue_id = result.issue_id
        for member_id in member_story_ids:
            try:
                self.story_repository.update_lifecycle_status(
                    member_id, StoryLifecycleStatus.CLUSTERED
                )
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "cluster.lifecycle_update_failed",
                    extra={
                        "story_id": member_id,
                        "issue_id": issue_id,
                        "error": str(exc),
                    },
                )

        if self.cluster_membership_store is not None:
            for lens in self.clustering_engine.active_lenses:
                for member_id in member_story_ids:
                    member_cluster_id = memberships.get(member_id, {}).get(lens.value)
                    if member_cluster_id is None:
                        continue
                    try:
                        self.cluster_membership_store.save_membership(
                            story_id=member_id,
                            lens=lens.value,
                            cluster_id=member_cluster_id,
                        )
                    except Exception as exc:  # noqa: BLE001
                        logger.warning(
                            "cluster.membership_persist_failed",
                            extra={
                                "story_id": member_id,
                                "lens": lens.value,
                                "cluster_id": member_cluster_id,
                                "error": str(exc),
                            },
                        )

        logger.info(
            "cluster.issue_created",
            extra={
                "story_id": story_id,
                "issue_id": issue_id,
                "cluster_id": cluster_id,
                "lens": primary.value,
                "member_count": len(member_story_ids),
                "readiness_score": readiness_score,
                "readiness_factors": readiness_factors,
            },
        )
        return issue_id
