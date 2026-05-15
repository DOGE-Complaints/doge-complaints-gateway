from __future__ import annotations

import logging
from dataclasses import dataclass

from core.application.issue_create import IssueCreateCommand, IssueCreateService
from core.cluster import ClusterLens, ClusteringEngine, StoryProfileSignals
from core.domain import (
    ClusterMembershipStore,
    StoryLifecycleStatus,
    StoryRecord,
    StoryRepository,
    StorySignalStore,
)
from core.domain.narrative_i18n import story_primary_title
from core.profile import get_signals_for_story
from core.promotion.service import PromotionStateError

logger = logging.getLogger(__name__)

_CANONICAL_SIGNAL_POLICY = "v2.canonical"


@dataclass(frozen=True)
class StoryClusterOrchestrator:
    story_repository: StoryRepository
    clustering_engine: ClusteringEngine
    issue_create_service: IssueCreateService
    story_signal_store: StorySignalStore | None = None
    cluster_membership_store: ClusterMembershipStore | None = None

    def _get_or_compute_signals(self, story: StoryRecord) -> dict[str, str]:
        if self.story_signal_store is not None:
            cached = self.story_signal_store.get_signals(
                story.story_id, _CANONICAL_SIGNAL_POLICY
            )
            if cached is not None:
                return dict(cached)
        signals = get_signals_for_story(story)
        if self.story_signal_store is not None:
            try:
                self.story_signal_store.save_signals(
                    story.story_id, _CANONICAL_SIGNAL_POLICY, signals
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "cluster.signal_persist_failed",
                    extra={
                        "story_id": story.story_id,
                        "policy": _CANONICAL_SIGNAL_POLICY,
                        "error": str(exc),
                    },
                )
        return signals

    def process_story(self, story_id: str) -> str | None:
        logger.debug("cluster.process_story_start", extra={"story_id": story_id})
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
        logger.debug(
            "cluster.ready_snapshot",
            extra={"story_id": story_id, "ready_count": len(ready_stories)},
        )
        if not ready_stories:
            return None
        profiles, memberships, primary, id_algorithm = self._compute_cluster_inputs(
            ready_stories
        )
        if story_id not in memberships:
            return None

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
        logger.debug(
            "cluster.members_resolved",
            extra={
                "story_id": story_id,
                "cluster_id": cluster_id,
                "member_count": len(member_story_ids),
            },
        )

        return self._create_issue_for_cluster(
            trigger_story_id=story_id,
            target=target,
            cluster_id=cluster_id,
            member_story_ids=member_story_ids,
            primary_lens=primary.value,
            profiles=profiles,
            id_algorithm=id_algorithm,
            memberships=memberships,
        )

    def process_all_pending(self) -> list[str]:
        ready_stories = self.story_repository.list_stories_ready_for_clustering()
        logger.debug("cluster.batch_start", extra={"ready_count": len(ready_stories)})
        min_size_guard = max(1, self._resolve_min_size_guard())
        if len(ready_stories) < min_size_guard:
            logger.info(
                "cluster.batch_skipped_min_size",
                extra={
                    "ready_count": len(ready_stories),
                    "min_size_guard": min_size_guard,
                },
            )
            return []

        profiles, memberships, primary, id_algorithm = self._compute_cluster_inputs(
            ready_stories
        )
        clusters = self._cluster_members(primary.value, profiles, memberships)
        created_issue_ids: list[str] = []
        for cluster_id, member_story_ids in clusters.items():
            logger.debug(
                "cluster.batch_cluster_candidate",
                extra={"cluster_id": cluster_id, "member_count": len(member_story_ids)},
            )
            if not member_story_ids:
                continue
            target = self.story_repository.get_story(member_story_ids[0])
            if target is None:
                continue
            issue_id = self._create_issue_for_cluster(
                trigger_story_id=member_story_ids[0],
                target=target,
                cluster_id=cluster_id,
                member_story_ids=member_story_ids,
                primary_lens=primary.value,
                profiles=profiles,
                id_algorithm=id_algorithm,
                memberships=memberships,
            )
            if issue_id is not None:
                created_issue_ids.append(issue_id)
        return created_issue_ids

    def _resolve_min_size_guard(self) -> int:
        gate = getattr(self.issue_create_service, "promotion_service", None)
        policy = getattr(gate, "gate_policy", None)
        min_stories = getattr(policy, "min_stories", None)
        if isinstance(min_stories, int):
            return min_stories
        return 1

    def _compute_cluster_inputs(
        self, ready_stories: list[StoryRecord]
    ) -> tuple[
        tuple[StoryProfileSignals, ...],
        dict[str, dict[str, str]],
        ClusterLens,
        str,
    ]:
        id_algorithm = getattr(self.clustering_engine, "id_algorithm", "legacy_hash")
        profile_list: list[StoryProfileSignals] = []
        for story in ready_stories:
            inferred = self._get_or_compute_signals(story)
            profile_list.append(
                StoryProfileSignals(story_id=story.story_id, signals=inferred)
            )
        profiles = tuple(profile_list)
        memberships = self.clustering_engine.memberships(
            profiles, id_algorithm=id_algorithm
        )
        primary = self.clustering_engine.resolved_primary_lens()
        return profiles, memberships, primary, id_algorithm

    def _cluster_members(
        self,
        lens_key: str,
        profiles: tuple[StoryProfileSignals, ...],
        memberships: dict[str, dict[str, str]],
    ) -> dict[str, tuple[str, ...]]:
        grouped: dict[str, list[str]] = {}
        for profile in profiles:
            cluster_id = memberships.get(profile.story_id, {}).get(lens_key)
            if cluster_id is None:
                continue
            grouped.setdefault(cluster_id, []).append(profile.story_id)
        return {cluster_id: tuple(members) for cluster_id, members in grouped.items()}

    def _create_issue_for_cluster(
        self,
        *,
        trigger_story_id: str,
        target: StoryRecord,
        cluster_id: str,
        member_story_ids: tuple[str, ...],
        primary_lens: str,
        profiles: tuple[StoryProfileSignals, ...],
        id_algorithm: str,
        memberships: dict[str, dict[str, str]],
    ) -> str | None:
        readiness_score, readiness_factors = self.clustering_engine.readiness_for_story(
            story_id=target.story_id,
            profiles=profiles,
            primary_lens=self.clustering_engine.resolved_primary_lens(),
            id_algorithm=id_algorithm,
        )
        primary_title = story_primary_title(
            narrative_title=target.narrative_title,
            narrative_session_language=target.narrative_session_language,
            narrative_language=target.narrative_language,
        )
        issue_title = primary_title or f"cluster:{primary_lens}:{cluster_id}"
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
                "story_cluster_issue_pending",
                extra={
                    "story_id": trigger_story_id,
                    "cluster_id": cluster_id,
                    "lens": primary_lens,
                    "story_count": len(member_story_ids),
                    "readiness_score": readiness_score,
                    "gate_reason": str(exc),
                    "outcome": "not_clustered",
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
        self._persist_memberships(member_story_ids, memberships)
        logger.info(
            "story_cluster_issue_created",
            extra={
                "story_id": trigger_story_id,
                "issue_id": issue_id,
                "cluster_id": cluster_id,
                "lens": primary_lens,
                "story_count": len(member_story_ids),
                "readiness_score": readiness_score,
                "readiness_factors": readiness_factors,
                "outcome": "clustered",
            },
        )
        return issue_id

    def _persist_memberships(
        self,
        member_story_ids: tuple[str, ...],
        memberships: dict[str, dict[str, str]],
    ) -> None:
        if self.cluster_membership_store is None:
            return
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
