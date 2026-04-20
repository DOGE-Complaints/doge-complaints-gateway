from __future__ import annotations

from core.cluster import CANONICAL_LENSES, ClusteringEngine, ClusterLens, ClusteringMode, StoryProfileSignals


def _profile(story_id: str, **signals: str) -> StoryProfileSignals:
    return StoryProfileSignals(story_id=story_id, signals=signals)


def test_canonical_lenses_minimum_six() -> None:
    assert len(CANONICAL_LENSES) == 6


def test_clustering_engine_build_view_is_deterministic() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-a",
            topic="mobility",
            need="restore_access",
            system_failure="service_disruption",
            repeatability="recurrent",
            relevance="high",
            desired_state="stable_public_service",
        ),
        _profile(
            "story-b",
            topic="mobility",
            need="resolve_issue",
            system_failure="quality_gap",
            repeatability="single_or_unknown",
            relevance="high",
            desired_state="stable_public_service",
        ),
    )

    first = engine.build_view(lens=ClusterLens.TOPIC_MICRO, profiles=profiles, mode=ClusteringMode.ANALYTIC)
    second = engine.build_view(lens=ClusterLens.TOPIC_MICRO, profiles=profiles, mode=ClusteringMode.ANALYTIC)
    assert first == second


def test_memberships_allow_multi_membership_across_lenses() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            topic="mobility",
            need="restore_access",
            system_failure="service_disruption",
            repeatability="recurrent",
            relevance="high",
            desired_state="stable_public_service",
        ),
    )

    memberships = engine.memberships(profiles)
    assert memberships["story-1"][ClusterLens.TOPIC_MICRO.value] != memberships["story-1"][
        ClusterLens.NEED_LOCAL.value
    ]


def test_cluster_narrative_is_non_empty() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            topic="mobility",
            need="restore_access",
            system_failure="service_disruption",
            repeatability="recurrent",
            relevance="high",
            desired_state="stable_public_service",
        ),
    )
    view = engine.build_view(lens=ClusterLens.FAILURE_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ANALYTIC)
    assert view.narrative


def test_readiness_scoring_differs_between_modes() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            topic="mobility",
            need="restore_access",
            system_failure="service_disruption",
            repeatability="recurrent",
            relevance="high",
            desired_state="stable_public_service",
        ),
        _profile(
            "story-2",
            topic="mobility",
            need="resolve_issue",
            system_failure="service_disruption",
            repeatability="recurrent",
            relevance="high",
            desired_state="stable_public_service",
        ),
    )

    analytic = engine.build_view(
        lens=ClusterLens.FAILURE_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ANALYTIC
    )
    issue_ready = engine.build_view(
        lens=ClusterLens.FAILURE_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ISSUE_READY
    )
    assert issue_ready.readiness_score >= analytic.readiness_score
