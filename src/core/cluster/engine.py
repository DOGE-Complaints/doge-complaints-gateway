from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Iterable, Mapping

from core.cluster.types import (
    Cluster,
    ClusterLens,
    ClusterMember,
    ClusteringMode,
    ClusterView,
    StoryProfileSignals,
)
from core.domain import SignalDimension


CANONICAL_LENSES: tuple[ClusterLens, ...] = (
    ClusterLens.TOPIC_MICRO,
    ClusterLens.NEED_LOCAL,
    ClusterLens.FAILURE_SYSTEMIC,
    ClusterLens.FAILURE_MICRO,
    ClusterLens.REPEATABILITY_LOCAL,
    ClusterLens.RELEVANCE_SYSTEMIC,
)


def merged_signals(profile: StoryProfileSignals) -> dict[str, str]:
    merged: dict[str, str] = {}
    merged.update(profile.signals)
    return merged


def lens_dimension(lens: ClusterLens) -> SignalDimension:
    mapping: dict[ClusterLens, SignalDimension] = {
        ClusterLens.TOPIC_MICRO: SignalDimension.TOPIC,
        ClusterLens.NEED_LOCAL: SignalDimension.NEED,
        ClusterLens.FAILURE_SYSTEMIC: SignalDimension.SYSTEM_FAILURE,
        ClusterLens.FAILURE_MICRO: SignalDimension.SYSTEM_FAILURE,
        ClusterLens.REPEATABILITY_LOCAL: SignalDimension.REPEATABILITY,
        ClusterLens.RELEVANCE_SYSTEMIC: SignalDimension.RELEVANCE,
    }
    return mapping[lens]


def cluster_key_for_lens(profile: StoryProfileSignals, lens: ClusterLens) -> str:
    signals = merged_signals(profile)
    dimension = lens_dimension(lens)
    raw_value = signals.get(dimension.value, "unknown").strip() or "unknown"

    if lens in (ClusterLens.FAILURE_MICRO, ClusterLens.TOPIC_MICRO, ClusterLens.REPEATABILITY_LOCAL):
        return f"{lens.value}:{dimension.value}:{raw_value}:micro"
    if lens in (ClusterLens.FAILURE_SYSTEMIC, ClusterLens.RELEVANCE_SYSTEMIC):
        return f"{lens.value}:{dimension.value}:{raw_value}:systemic"
    return f"{lens.value}:{dimension.value}:{raw_value}:local"


def stable_cluster_id(lens: ClusterLens, key: str) -> str:
    digest = abs(hash((lens.value, key))) % 1_000_000_000
    return f"cluster:{lens.value}:{digest:09d}"


def dominant_value(values: Iterable[str]) -> str:
    counts = Counter(value for value in values if value.strip())
    if not counts:
        return "unknown"
    max_count = max(counts.values())
    candidates = sorted(value for value, count in counts.items() if count == max_count)
    return candidates[0]


def build_cluster_narrative(*, lens: ClusterLens, members: tuple[ClusterMember, ...]) -> str:
    return (
        f"Lens={lens.value}; members={len(members)}; "
        "summary aggregates dominant signal values without rewriting original narratives."
    )


def readiness_score_for_cluster(
    *, lens: ClusterLens, members: tuple[ClusterMember, ...], mode: ClusteringMode
) -> tuple[int, dict[str, int]]:
    size = len(members)
    base = min(100, 20 + size * 15)
    lens_bonus = 5 if lens in (ClusterLens.FAILURE_SYSTEMIC, ClusterLens.RELEVANCE_SYSTEMIC) else 0
    mode_bonus = 10 if mode == ClusteringMode.ISSUE_READY else 0
    score = min(100, base + lens_bonus + mode_bonus)
    factors = {
        "size": size,
        "lens_bonus": lens_bonus,
        "mode_bonus": mode_bonus,
    }
    return score, factors


@dataclass(frozen=True)
class ClusteringEngine:
    def build_view(
        self, *, lens: ClusterLens, profiles: tuple[StoryProfileSignals, ...], mode: ClusteringMode
    ) -> ClusterView:
        buckets: dict[str, list[StoryProfileSignals]] = defaultdict(list)
        for profile in sorted(profiles, key=lambda item: item.story_id):
            buckets[cluster_key_for_lens(profile, lens)].append(profile)

        clusters: list[Cluster] = []
        for key in sorted(buckets.keys()):
            members = tuple(ClusterMember(story_id=item.story_id) for item in buckets[key])
            clusters.append(
                Cluster(
                    cluster_id=stable_cluster_id(lens, key),
                    lens=lens,
                    members=members,
                )
            )

        primary = max(clusters, key=lambda cluster: len(cluster.members)) if clusters else None
        narrative = (
            build_cluster_narrative(lens=lens, members=primary.members)
            if primary is not None
            else f"Lens={lens.value}; empty_view"
        )
        readiness_members = primary.members if primary is not None else tuple()
        readiness_score, readiness_factors = readiness_score_for_cluster(
            lens=lens, members=readiness_members, mode=mode
        )

        return ClusterView(
            lens=lens,
            mode=mode,
            clusters=tuple(clusters),
            narrative=narrative,
            readiness_score=readiness_score,
            readiness_factors=readiness_factors,
        )

    def memberships(self, profiles: tuple[StoryProfileSignals, ...]) -> dict[str, dict[str, str]]:
        """Map story_id -> {lens: cluster_id} for all canonical lenses."""
        result: dict[str, dict[str, str]] = {}
        for lens in CANONICAL_LENSES:
            view = self.build_view(lens=lens, profiles=profiles, mode=ClusteringMode.ANALYTIC)
            for cluster in view.clusters:
                for member in cluster.members:
                    result.setdefault(member.story_id, {})[lens.value] = cluster.cluster_id
        return result

    def dominant_signals(self, profiles: tuple[StoryProfileSignals, ...]) -> dict[str, str]:
        merged_dimensions: dict[str, list[str]] = defaultdict(list)
        for profile in profiles:
            for key, value in merged_signals(profile).items():
                merged_dimensions[key].append(value)
        return {key: dominant_value(values) for key, values in merged_dimensions.items()}
