from __future__ import annotations

from core.cluster import CANONICAL_LENSES, ClusteringEngine, ClusterLens, ClusteringMode, StoryProfileSignals
from core.cluster.engine import build_cluster_narrative, stable_cluster_id
from core.cluster.types import ClusterMember


def _profile(story_id: str, **signals: str) -> StoryProfileSignals:
    return StoryProfileSignals(story_id=story_id, signals=signals)


def _engine(
    *,
    lenses: tuple[ClusterLens, ...] = (ClusterLens.CIVIC_DOMAIN_MICRO,),
    primary: ClusterLens | None = None,
    id_algorithm: str = "sha256",
    signal_source: str = "keyword",
) -> ClusteringEngine:
    return ClusteringEngine(
        active_lenses=lenses,
        primary_lens=primary if primary is not None else lenses[0],
        id_algorithm=id_algorithm,
        signal_source=signal_source,
        geo_filter="any",
        tie_breaker="lexical",
        type_resolution="canonical_priority",
    )


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


def test_stable_cluster_id_sha256_deterministic() -> None:
    lens = ClusterLens.CIVIC_DOMAIN_MICRO
    id1 = stable_cluster_id(lens, "roads::broken_infrastructure", id_algorithm="sha256")
    id2 = stable_cluster_id(lens, "roads::broken_infrastructure", id_algorithm="sha256")
    assert id1 == id2
    assert id1.startswith("cluster:civic_domain_micro:")
    assert len(id1.split(":")[-1]) == 10


def test_stable_cluster_id_sha256_vs_legacy_differ() -> None:
    lens = ClusterLens.CIVIC_DOMAIN_MICRO
    sha_id = stable_cluster_id(lens, "roads::broken_infrastructure", id_algorithm="sha256")
    legacy_id = stable_cluster_id(lens, "roads::broken_infrastructure", id_algorithm="legacy_hash")
    assert sha_id != legacy_id
    assert sha_id.startswith("cluster:civic_domain_micro:")
    assert legacy_id.startswith("cluster:civic_domain_micro:")


def test_readiness_per_cluster_not_max_cluster() -> None:
    engine = _engine()
    profiles_a = tuple(_profile(f"a{i}", civic_domain="roads") for i in range(5))
    profiles_b = tuple(_profile(f"b{i}", civic_domain="waste") for i in range(2))
    profiles = profiles_a + profiles_b

    view = engine.build_view(
        lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        profiles=profiles,
        mode=ClusteringMode.ISSUE_READY,
    )
    cluster_b = next(c for c in view.clusters if any(m.story_id.startswith("b") for m in c.members))
    score_b = cluster_b.readiness_score
    assert score_b < 80
    assert view.readiness_score > score_b


def test_build_view_each_cluster_has_score() -> None:
    engine = _engine()
    profiles = (
        _profile("x1", civic_domain="roads"),
        _profile("x2", civic_domain="roads"),
        _profile("y1", civic_domain="waste"),
        _profile("y2", civic_domain="waste"),
        _profile("z1", civic_domain="transport"),
    )
    view = engine.build_view(
        lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        profiles=profiles,
        mode=ClusteringMode.ISSUE_READY,
    )
    for cluster in view.clusters:
        assert cluster.readiness_score > 0
        assert "size" in cluster.readiness_factors
        assert "base" in cluster.readiness_factors


def test_memberships_uses_issue_ready_mode() -> None:
    engine = _engine()
    profiles = (
        _profile("s1", civic_domain="roads"),
        _profile("s2", civic_domain="roads"),
    )
    engine.memberships(profiles)
    score, _factors = engine.readiness_for_story(
        story_id="s1",
        profiles=profiles,
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
    )
    assert score == 60


def test_build_cluster_narrative_dynamic() -> None:
    profiles = [
        _profile("s1", civic_domain="roads", failure_pattern="broken_infrastructure"),
        _profile("s2", civic_domain="roads", failure_pattern="broken_infrastructure"),
    ]
    members = tuple(ClusterMember(story_id=p.story_id) for p in profiles)
    dominant = {"civic_domain": "roads", "failure_pattern": "broken_infrastructure"}
    narrative = build_cluster_narrative(
        lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        members=members,
        dominant=dominant,
    )
    assert "roads" in narrative
    assert "broken_infrastructure" in narrative
    assert narrative != f"Lens={ClusterLens.CIVIC_DOMAIN_MICRO.value}; members=2"
