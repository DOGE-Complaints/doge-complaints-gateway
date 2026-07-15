from __future__ import annotations

from core.cluster import CANONICAL_LENSES, ClusteringEngine, ClusterLens, ClusteringMode, StoryProfileSignals
from core.cluster.engine import build_cluster_narrative, stable_cluster_id
from core.cluster.types import ClusterMember
from core.domain import SignalDimension
from core.profile import infer_signals_from_canonical


def _profile(story_id: str, **signals: str) -> StoryProfileSignals:
    return StoryProfileSignals(story_id=story_id, signals=signals)


def _engine(
    *,
    lenses: tuple[ClusterLens, ...] = (ClusterLens.CIVIC_DOMAIN_MICRO,),
    primary: ClusterLens | None = None,
    id_algorithm: str = "sha256",
) -> ClusteringEngine:
    return ClusteringEngine(
        active_lenses=lenses,
        primary_lens=primary if primary is not None else lenses[0],
        id_algorithm=id_algorithm,
    )


def test_canonical_lenses_minimum_ten() -> None:
    assert len(CANONICAL_LENSES) == 10


def test_clustering_engine_default_id_algorithm_matches_runtime_default() -> None:
    assert ClusteringEngine().id_algorithm == "sha256"


def test_clustering_engine_build_view_is_deterministic() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-a",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="recurring_issue",
            desired_outcome="safer_space",
            affected_group="general_public",
            geographic_district="unknown",
        ),
        _profile(
            "story-b",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="isolated",
            desired_outcome="safer_space",
            affected_group="general_public",
            geographic_district="unknown",
        ),
    )

    first = engine.build_view(
        lens=ClusterLens.CIVIC_DOMAIN_MICRO, profiles=profiles, mode=ClusteringMode.ANALYTIC
    )
    second = engine.build_view(
        lens=ClusterLens.CIVIC_DOMAIN_MICRO, profiles=profiles, mode=ClusteringMode.ANALYTIC
    )
    assert first == second


def test_memberships_allow_multi_membership_across_lenses() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="systemic_pattern",
            desired_outcome="digital_fix",
            affected_group="general_public",
            geographic_district="unknown",
        ),
    )

    memberships = engine.memberships(profiles)
    assert memberships["story-1"][ClusterLens.CIVIC_DOMAIN_MICRO.value] != memberships["story-1"][
        ClusterLens.DESIRED_OUTCOME_LOCAL.value
    ]


def test_cluster_narrative_is_non_empty() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="systemic_pattern",
            desired_outcome="safer_space",
            affected_group="general_public",
            geographic_district="unknown",
        ),
    )
    view = engine.build_view(
        lens=ClusterLens.CIVIC_WEIGHT_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ANALYTIC
    )
    assert view.narrative


def test_readiness_scoring_differs_between_modes() -> None:
    engine = ClusteringEngine()
    profiles = (
        _profile(
            "story-1",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="systemic_pattern",
            desired_outcome="safer_space",
            affected_group="general_public",
            geographic_district="unknown",
        ),
        _profile(
            "story-2",
            civic_domain="roads",
            failure_pattern="broken_infrastructure",
            civic_weight="systemic_pattern",
            desired_outcome="safer_space",
            affected_group="general_public",
            geographic_district="unknown",
        ),
    )

    analytic = engine.build_view(
        lens=ClusterLens.CIVIC_WEIGHT_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ANALYTIC
    )
    issue_ready = engine.build_view(
        lens=ClusterLens.CIVIC_WEIGHT_SYSTEMIC, profiles=profiles, mode=ClusteringMode.ISSUE_READY
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


def test_ac06_language_neutral_clustering_via_canonical() -> None:
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.FAILURE_PATTERN_MICRO,),
        primary_lens=ClusterLens.FAILURE_PATTERN_MICRO,
        id_algorithm="sha256",
    )
    et_signals = infer_signals_from_canonical("complaint", ("roads", "broken_infrastructure"))
    en_signals = infer_signals_from_canonical("complaint", ("roads", "broken_infrastructure"))
    profiles = (
        StoryProfileSignals(story_id="s-et", signals=et_signals),
        StoryProfileSignals(story_id="s-en", signals=en_signals),
    )

    memberships = engine.memberships(profiles)
    lens_key = ClusterLens.FAILURE_PATTERN_MICRO.value
    assert memberships["s-et"][lens_key] == memberships["s-en"][lens_key]


def test_ac02_civic_weight_systemic_readiness_threshold() -> None:
    profiles = (
        StoryProfileSignals(
            story_id="s1",
            signals={SignalDimension.CIVIC_WEIGHT.value: "systemic_pattern"},
        ),
        StoryProfileSignals(
            story_id="s2",
            signals={SignalDimension.CIVIC_WEIGHT.value: "systemic_pattern"},
        ),
        StoryProfileSignals(
            story_id="s3",
            signals={SignalDimension.CIVIC_WEIGHT.value: "systemic_pattern"},
        ),
    )
    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_WEIGHT_SYSTEMIC,),
        primary_lens=ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
        id_algorithm="sha256",
    )
    score, _ = engine.readiness_for_story(
        story_id="s1",
        profiles=profiles,
        primary_lens=ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
        id_algorithm="sha256",
    )
    assert score >= 60


def test_ac03_civic_domain_and_failure_pattern_separability() -> None:
    roads_broken = infer_signals_from_canonical(None, ("roads", "broken_infrastructure"))
    waste_maint = infer_signals_from_canonical(None, ("waste", "maintenance_gap"))
    roads_maint = infer_signals_from_canonical(None, ("roads", "maintenance_gap"))

    engine = ClusteringEngine(
        active_lenses=(ClusterLens.CIVIC_DOMAIN_MICRO, ClusterLens.FAILURE_PATTERN_MICRO),
        primary_lens=ClusterLens.CIVIC_DOMAIN_MICRO,
        id_algorithm="sha256",
    )
    profiles = (
        StoryProfileSignals("s-rb", roads_broken),
        StoryProfileSignals("s-wm", waste_maint),
        StoryProfileSignals("s-rm", roads_maint),
    )
    memberships = engine.memberships(profiles)
    civic = ClusterLens.CIVIC_DOMAIN_MICRO.value
    failure = ClusterLens.FAILURE_PATTERN_MICRO.value

    assert memberships["s-rb"][civic] != memberships["s-wm"][civic]
    assert memberships["s-rb"][civic] == memberships["s-rm"][civic]
    assert memberships["s-rb"][failure] != memberships["s-rm"][failure]


def test_ac05_desired_outcome_local_separates_digital_fix() -> None:
    digital = infer_signals_from_canonical(None, ("roads", "digital_fix"))
    other = infer_signals_from_canonical(None, ("roads", "safer_space"))

    engine = ClusteringEngine(
        active_lenses=(ClusterLens.DESIRED_OUTCOME_LOCAL,),
        primary_lens=ClusterLens.DESIRED_OUTCOME_LOCAL,
        id_algorithm="sha256",
    )
    profiles = (
        StoryProfileSignals("s-digital", digital),
        StoryProfileSignals("s-other", other),
    )
    memberships = engine.memberships(profiles)
    desired = ClusterLens.DESIRED_OUTCOME_LOCAL.value

    assert memberships["s-digital"][desired] != memberships["s-other"][desired]
