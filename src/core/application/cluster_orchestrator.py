from __future__ import annotations

from dataclasses import dataclass

from core.application.issue_create import IssueCreateCommand, IssueCreateService
from core.cluster import ClusterLens, ClusteringEngine, StoryProfileSignals
from core.domain import StoryLifecycleStatus, StoryRepository
from core.profile import infer_signals_from_narrative
from core.promotion.service import PromotionStateError


@dataclass(frozen=True)
class StoryClusterOrchestrator:
    story_repository: StoryRepository
    clustering_engine: ClusteringEngine
    issue_create_service: IssueCreateService

    def process_story(self, story_id: str) -> str | None:
        target = self.story_repository.get_story(story_id)
        if target is None:
            return None
        if target.lifecycle_status is not StoryLifecycleStatus.READY_FOR_PROFILE:
            return None

        ready_stories = [
            item
            for item in self.story_repository.list_stories()
            if item.lifecycle_status is StoryLifecycleStatus.READY_FOR_PROFILE
        ]
        if not ready_stories:
            return None

        profiles = tuple(
            StoryProfileSignals(
                story_id=item.story_id,
                signals=infer_signals_from_narrative(item.narrative_original_text),
            )
            for item in ready_stories
        )
        memberships = self.clustering_engine.memberships(profiles)
        if story_id not in memberships:
            return None

        first_lens = self.clustering_engine.active_lenses[0]
        lens_key = first_lens.value
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

        issue_title = target.narrative_title_hint or f"cluster:{ClusterLens(first_lens).value}"
        try:
            result = self.issue_create_service.create_issue(
                IssueCreateCommand(
                    cluster_id=cluster_id,
                    story_ids=member_story_ids,
                    readiness_score=100,
                    title=issue_title,
                )
            )
            return result.issue_id
        except (ValueError, PromotionStateError):
            return None
