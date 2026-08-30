from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Mapping

from core.application.issue_create import IssueCreateCommand, IssueCreateService
from core.cluster import ClusterLens, ClusteringEngine, StoryProfileSignals
from core.cluster.engine import composite_primary_signal_pair
from core.domain import (
    ClusterMembershipStore,
    StoryLabelRepository,
    StoryLifecycleStatus,
    StoryRecord,
    StoryRepository,
    StorySignalStore,
)
from core.domain.narrative_i18n import story_primary_title
from core.logging_setup import StoryDebugLogger, open_story_debug_logger
from core.profile import get_signals_for_story
from core.profile.enrichment import log_story_signals_inferred
from core.promotion.gates import evaluate_promotion_gates
from core.promotion.service import PromotionStateError
from core.promotion.types import IssueCandidateRecord, IssueCandidateStatus
from core.schema.errors import PackLensMissingPathError, SchemaRuntimeError
from core.schema.pack_engine import PackMembership, SchemaPackClusterEngine, is_schema_bound
from core.schema.pack_policy import promotion_gate_policy_from_pack

logger = logging.getLogger(__name__)

_CANONICAL_SIGNAL_POLICY = "v2.canonical"


@dataclass(frozen=True)
class StoryClusterOrchestrator:
    story_repository: StoryRepository
    clustering_engine: ClusteringEngine
    issue_create_service: IssueCreateService
    story_signal_store: StorySignalStore | None = None
    story_label_repository: StoryLabelRepository | None = None
    cluster_membership_store: ClusterMembershipStore | None = None
    log_debug_dir: str | None = None
    cluster_min_size_by_lens: Mapping[str, int] = field(default_factory=dict)
    default_cluster_min_size: int = 1
    schema_pack_engine: SchemaPackClusterEngine | None = None
    node_schema_id: str | None = None
    node_schema_version: str | None = None

    def _cluster_key_from_signals(self, signals: dict[str, str]) -> str:
        civic_domain, failure_pattern = composite_primary_signal_pair(signals)
        return f"{civic_domain}+{failure_pattern}"

    def _get_or_compute_signals(
        self,
        story: StoryRecord,
        *,
        debug_logger: StoryDebugLogger | None = None,
    ) -> dict[str, str]:
        if self.story_signal_store is not None:
            cached = self.story_signal_store.get_signals(
                story.story_id, _CANONICAL_SIGNAL_POLICY
            )
            if cached is not None:
                return dict(cached)
        signals = get_signals_for_story(
            story,
            story_label_repository=self.story_label_repository,
        )
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
        log_story_signals_inferred(debug_logger, signals=signals)
        return signals

    def _pack_engine(self) -> SchemaPackClusterEngine:
        return self.schema_pack_engine or SchemaPackClusterEngine()

    def _civic_ready(self, stories: list[StoryRecord]) -> list[StoryRecord]:
        """SSR-18: civic pool is unbound-only. Mismatch bound is skipped, not civic."""
        return [story for story in stories if not is_schema_bound(story)]

    def _matches_active_node_schema(self, story: StoryRecord) -> bool:
        if not self.node_schema_id or not self.node_schema_version:
            return False
        return (
            story.schema_id == self.node_schema_id
            and story.bound_schema_version == self.node_schema_version
        )

    def _skip_schema_mismatch(self, story: StoryRecord) -> None:
        logger.info(
            "cluster.skipped_schema_mismatch",
            extra={
                "story_id": story.story_id,
                "persist_schema_id": story.schema_id,
                "persist_schema_version": story.bound_schema_version,
                "node_schema_id": self.node_schema_id,
                "node_schema_version": self.node_schema_version,
            },
        )

    def _dual_civic_enabled(self, story: StoryRecord) -> bool:
        """Dual flag from the *active* pack.json (NODE_SCHEMA_*), not a foreign story pack."""
        if not self.node_schema_id or not self.node_schema_version:
            return False
        try:
            return self._pack_engine().dual_civic_lenses_for_ref(
                self.node_schema_id,
                self.node_schema_version,
                profile_ref=story.profile_id,
            )
        except SchemaRuntimeError:
            return False

    def _process_dual_civic_membership(self, story: StoryRecord) -> str | None:
        """Civic memberships + civic-policy promote. Separate from pack candidate."""
        profiles, memberships, primary, id_algorithm = self._compute_cluster_inputs(
            [story],
            trigger_story_id=story.story_id,
        )
        if story.story_id not in memberships:
            return None
        self._persist_memberships((story.story_id,), memberships)
        lens_key = primary.value
        cluster_id = memberships[story.story_id].get(lens_key)
        if cluster_id is None:
            return None
        return self._create_issue_for_cluster(
            trigger_story_id=story.story_id,
            target=story,
            cluster_id=cluster_id,
            member_story_ids=(story.story_id,),
            primary_lens=primary.value,
            profiles=profiles,
            id_algorithm=id_algorithm,
            memberships=memberships,
        )

    def _process_bound_story(self, story: StoryRecord) -> str | None:
        pack_issue = self._process_pack_bound_story(story)
        if not self._dual_civic_enabled(story):
            return pack_issue
        civic_issue = self._process_dual_civic_membership(story)
        return civic_issue or pack_issue

    def _process_pack_bound_story(self, story: StoryRecord) -> str | None:
        """Save pack memberships; promote + CLUSTERED only if pack gate passes."""
        try:
            memberships = self._pack_engine().memberships_for_story(story)
        except PackLensMissingPathError as exc:
            logger.warning(
                "cluster.pack_lens_path_miss",
                extra={"story_id": story.story_id, "error": str(exc)},
            )
            return None
        except SchemaRuntimeError as exc:
            logger.warning(
                "cluster.pack_engine_failed",
                extra={"story_id": story.story_id, "error": str(exc)},
            )
            return None
        store = self.cluster_membership_store
        if store is None:
            return None
        for item in memberships:
            try:
                store.save_membership(
                    story_id=item.story_id,
                    lens=item.lens,
                    cluster_id=item.cluster_id,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "cluster.pack_membership_persist_failed",
                    extra={
                        "story_id": item.story_id,
                        "lens": item.lens,
                        "error": str(exc),
                    },
                )
        issue_id: str | None = None
        for item in memberships:
            promoted = self._promote_pack_membership(story, item)
            if promoted is not None:
                issue_id = promoted
        return issue_id

    def _pack_readiness_score(self, member_count: int, min_size: int, min_readiness_score: int) -> int:
        """T-wave pack score: at/above pack threshold iff membership meets min_size."""
        if member_count >= min_size:
            return min_readiness_score
        return min_readiness_score - 1

    def _promote_pack_membership(
        self, story: StoryRecord, item: PackMembership
    ) -> str | None:
        store = self.cluster_membership_store
        if store is None:
            return None
        member_ids = tuple(store.get_cluster_members(item.cluster_id, item.lens))
        if not member_ids:
            return None
        lens = self._pack_engine().lens_block_for(story, item.lens)
        if lens is None:
            return None
        gate_policy = promotion_gate_policy_from_pack(lens.readiness_policy)
        readiness_score = self._pack_readiness_score(
            len(member_ids),
            lens.min_size,
            lens.readiness_policy.min_readiness_score,
        )
        first = self.story_repository.get_story(member_ids[0]) or story
        primary_title = story_primary_title(
            narrative_title=first.narrative_title,
            narrative_session_language=first.narrative_session_language,
            narrative_language=first.narrative_language,
        )
        issue_title = primary_title or first.narrative_original_text or f"pack:{item.lens}"
        try:
            result = self.issue_create_service.create_issue(
                IssueCreateCommand(
                    cluster_id=item.cluster_id,
                    story_ids=member_ids,
                    readiness_score=readiness_score,
                    title=issue_title,
                    gate_policy=gate_policy,
                )
            )
        except (ValueError, PromotionStateError) as exc:
            logger.info(
                "story_cluster_issue_pending",
                extra={
                    "story_id": story.story_id,
                    "cluster_id": item.cluster_id,
                    "lens": item.lens,
                    "story_count": len(member_ids),
                    "readiness_score": readiness_score,
                    "gate_reason": str(exc),
                    "outcome": "not_clustered",
                    "path": "pack",
                },
            )
            return None
        issue_id = result.issue_id
        for member_id in member_ids:
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
        logger.info(
            "story_cluster_issue_created",
            extra={
                "story_id": story.story_id,
                "issue_id": issue_id,
                "cluster_id": item.cluster_id,
                "lens": item.lens,
                "story_count": len(member_ids),
                "readiness_score": readiness_score,
                "outcome": "clustered",
                "path": "pack",
            },
        )
        return issue_id

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

        if is_schema_bound(target):
            if not self._matches_active_node_schema(target):
                self._skip_schema_mismatch(target)
                return None
            return self._process_bound_story(target)

        ready_stories = self._civic_ready(
            self.story_repository.list_stories_ready_for_clustering()
        )
        logger.debug(
            "cluster.ready_snapshot",
            extra={"story_id": story_id, "ready_count": len(ready_stories)},
        )
        if not ready_stories:
            return None
        with open_story_debug_logger(story_id, self.log_debug_dir) as debug_logger:
            profiles, memberships, primary, id_algorithm = self._compute_cluster_inputs(
                ready_stories,
                debug_logger=debug_logger,
                trigger_story_id=story_id,
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
            trigger_signals = next(
                (dict(p.signals) for p in profiles if p.story_id == story_id),
                {},
            )
            min_size = self._resolve_min_size_guard(lens_key)
            is_new = len(member_story_ids) <= min_size
            if isinstance(debug_logger, StoryDebugLogger):
                debug_logger.log(
                    "cluster",
                    "assigned" if not is_new else "created",
                    {
                        "cluster_id": cluster_id,
                        "lens": lens_key,
                        "key": self._cluster_key_from_signals(trigger_signals),
                        "is_new": is_new,
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
                debug_logger=debug_logger,
            )

    def process_all_pending(self) -> list[str]:
        ready_stories = self.story_repository.list_stories_ready_for_clustering()
        logger.debug("cluster.batch_start", extra={"ready_count": len(ready_stories)})
        pack_stories: list[StoryRecord] = []
        for story in ready_stories:
            if not is_schema_bound(story):
                continue
            if not self._matches_active_node_schema(story):
                self._skip_schema_mismatch(story)
                continue
            pack_stories.append(story)
        civic_stories = self._civic_ready(ready_stories)
        created_issue_ids: list[str] = []
        for story in pack_stories:
            issue_id = self._process_bound_story(story)
            if issue_id is not None:
                created_issue_ids.append(issue_id)
        primary_lens = self.clustering_engine.resolved_primary_lens()
        min_size_guard = max(1, self._resolve_min_size_guard(primary_lens.value))
        if len(civic_stories) < min_size_guard:
            logger.info(
                "cluster.batch_skipped_min_size",
                extra={
                    "ready_count": len(civic_stories),
                    "min_size_guard": min_size_guard,
                },
            )
            return created_issue_ids

        profiles, memberships, primary, id_algorithm = self._compute_cluster_inputs(
            civic_stories
        )
        clusters = self._cluster_members(primary.value, profiles, memberships)
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

    def _resolve_min_size_guard(self, lens: str | None = None) -> int:
        lens_key = lens or self.clustering_engine.resolved_primary_lens().value
        configured = self.cluster_min_size_by_lens.get(lens_key)
        if isinstance(configured, int):
            return configured
        gate = getattr(self.issue_create_service, "promotion_service", None)
        policy = getattr(gate, "gate_policy", None)
        min_stories = getattr(policy, "min_stories", None)
        if isinstance(min_stories, int):
            return min_stories
        return max(1, self.default_cluster_min_size)

    def _compute_cluster_inputs(
        self,
        ready_stories: list[StoryRecord],
        *,
        debug_logger: StoryDebugLogger | None = None,
        trigger_story_id: str | None = None,
    ) -> tuple[
        tuple[StoryProfileSignals, ...],
        dict[str, dict[str, str]],
        ClusterLens,
        str,
    ]:
        id_algorithm = getattr(self.clustering_engine, "id_algorithm", "legacy_hash")
        profile_list: list[StoryProfileSignals] = []
        for story in ready_stories:
            story_logger = (
                debug_logger
                if debug_logger is not None and story.story_id == trigger_story_id
                else None
            )
            inferred = self._get_or_compute_signals(story, debug_logger=story_logger)
            profile_list.append(
                StoryProfileSignals(
                    story_id=story.story_id,
                    signals=inferred,
                    geo=story.geo,
                )
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
        debug_logger: StoryDebugLogger | None = None,
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
        promotion_service = getattr(self.issue_create_service, "promotion_service", None)
        gate_policy = getattr(promotion_service, "gate_policy", None)
        if gate_policy is None:
            from core.promotion.gates import PromotionGatePolicy

            gate_policy = PromotionGatePolicy()
        cluster_canonical_types = tuple(
            record.narrative_canonical_type
            for member_id in member_story_ids
            if (record := self.story_repository.get_story(member_id)) is not None
            and record.narrative_canonical_type
        )
        gate_preview = IssueCandidateRecord(
            candidate_id="preview",
            status=IssueCandidateStatus.DRAFT,
            cluster_id=cluster_id,
            story_ids=member_story_ids,
            readiness_score=readiness_score,
            title=issue_title,
        )
        gate_result = evaluate_promotion_gates(
            gate_preview,
            gate_policy,
            cluster_canonical_types=cluster_canonical_types,
        )
        canonical_type_gate = (
            "pass"
            if "no_actionable_canonical_type" not in gate_result.reasons
            else "fail"
        )

        def _log_promotion(*, promoted: bool, issue_id: str | None = None) -> None:
            if not isinstance(debug_logger, StoryDebugLogger):
                return
            debug_logger.log(
                "promotion",
                "gate_result",
                {
                    "readiness_score": readiness_score,
                    "threshold": gate_policy.min_readiness_score,
                    "canonical_type_gate": canonical_type_gate,
                    "promoted": promoted,
                    "issue_id": issue_id,
                },
            )

        try:
            result = self.issue_create_service.create_issue(
                IssueCreateCommand(
                    cluster_id=cluster_id,
                    story_ids=member_story_ids,
                    readiness_score=readiness_score,
                    title=issue_title,
                    min_stories=self._resolve_min_size_guard(primary_lens),
                )
            )
        except (ValueError, PromotionStateError) as exc:
            _log_promotion(promoted=False)
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
        _log_promotion(promoted=True, issue_id=issue_id)
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
