from __future__ import annotations

import hashlib
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


LEGACY_LENSES: tuple[ClusterLens, ...] = (
    ClusterLens.TOPIC_MICRO,
    ClusterLens.NEED_LOCAL,
    ClusterLens.FAILURE_SYSTEMIC,
    ClusterLens.FAILURE_MICRO,
    ClusterLens.REPEATABILITY_LOCAL,
    ClusterLens.RELEVANCE_SYSTEMIC,
)

CANONICAL_LENSES: tuple[ClusterLens, ...] = LEGACY_LENSES  # backward-compat alias (deprecated name)

_SYSTEMIC_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
        ClusterLens.FAILURE_SYSTEMIC,
        ClusterLens.RELEVANCE_SYSTEMIC,
    }
)
_LOCAL_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.DESIRED_OUTCOME_LOCAL,
        ClusterLens.AFFECTED_GROUP_LOCAL,
        ClusterLens.NEED_LOCAL,
        ClusterLens.REPEATABILITY_LOCAL,
    }
)
_MICRO_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.CIVIC_DOMAIN_MICRO,
        ClusterLens.FAILURE_PATTERN_MICRO,
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
        ClusterLens.TOPIC_MICRO,
        ClusterLens.FAILURE_MICRO,
    }
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
        ClusterLens.CIVIC_DOMAIN_MICRO: SignalDimension.CIVIC_DOMAIN,
        ClusterLens.FAILURE_PATTERN_MICRO: SignalDimension.FAILURE_PATTERN,
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC: SignalDimension.CIVIC_WEIGHT,
        ClusterLens.DESIRED_OUTCOME_LOCAL: SignalDimension.DESIRED_OUTCOME,
        ClusterLens.AFFECTED_GROUP_LOCAL: SignalDimension.AFFECTED_GROUP,
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO: SignalDimension.GEOGRAPHIC_DISTRICT,
    }
    return mapping[lens]


def cluster_key_for_lens(profile: StoryProfileSignals, lens: ClusterLens) -> str:
    signals = merged_signals(profile)
    dimension = lens_dimension(lens)
    raw_value = str(signals.get(dimension.value, "unknown")).strip() or "unknown"

    if lens in _SYSTEMIC_LENSES:
        return f"{lens.value}:{dimension.value}:{raw_value}:systemic"
    if lens in _LOCAL_LENSES:
        return f"{lens.value}:{dimension.value}:{raw_value}:local"
    if lens in _MICRO_LENSES:
        return f"{lens.value}:{dimension.value}:{raw_value}:micro"
    return f"{lens.value}:{dimension.value}:{raw_value}:micro"


def stable_cluster_id(lens: ClusterLens, key: str, *, id_algorithm: str = "legacy_hash") -> str:
    if id_algorithm == "sha256":
        digest_hex = hashlib.sha256(f"{lens.value}:{key}".encode("utf-8")).hexdigest()
        numeric = int(digest_hex, 16) % 10_000_000_000
        return f"cluster:{lens.value}:{numeric:010d}"
    digest = abs(hash((lens.value, key))) % 1_000_000_000
    return f"cluster:{lens.value}:{digest:09d}"


def dominant_value(values: Iterable[str]) -> str:
    counts = Counter(value for value in values if str(value).strip())
    if not counts:
        return "unknown"
    max_count = max(counts.values())
    candidates = sorted(value for value, count in counts.items() if count == max_count)
    return candidates[0]


def lens_readiness_bonus(lens: ClusterLens) -> int:
    high_bonus = frozenset({ClusterLens.CIVIC_WEIGHT_SYSTEMIC})
    med_bonus = frozenset(
        {
            ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
            ClusterLens.FAILURE_SYSTEMIC,
            ClusterLens.RELEVANCE_SYSTEMIC,
        }
    )
    if lens in high_bonus:
        return 10
    if lens in med_bonus:
        return 5
    return 0


def build_cluster_narrative(
    *,
    lens: ClusterLens,
    members: tuple[ClusterMember, ...],
    dominant: dict[str, str] | None = None,
) -> str:
    size = len(members)
    if dominant is None or not dominant:
        return f"lens={lens.value}; members={size}"

    interesting_dims = (
        "civic_domain",
        "failure_pattern",
        "civic_weight",
        "desired_outcome",
        "affected_group",
        "geographic_district",
    )
    parts = [
        f"{dim}={dominant[dim]}"
        for dim in interesting_dims
        if dominant.get(dim) not in (None, "unknown", "isolated", "general_public")
    ]
    parts_str = "; ".join(parts) if parts else "no_dominant_signals"
    return f"lens={lens.value}; size={size}; {parts_str}"


def readiness_score_for_cluster(
    *, lens: ClusterLens, members: tuple[ClusterMember, ...], mode: ClusteringMode
) -> tuple[int, dict[str, int]]:
    size = len(members)
    base = min(100, 20 + size * 15)
    lens_bonus = lens_readiness_bonus(lens)
    mode_bonus = 10 if mode == ClusteringMode.ISSUE_READY else 0
    score = min(100, base + lens_bonus + mode_bonus)
    factors = {
        "size": size,
        "base": base,
        "lens_bonus": lens_bonus,
        "mode_bonus": mode_bonus,
    }
    return score, factors


@dataclass(frozen=True)
class ClusteringEngine:
    active_lenses: tuple[ClusterLens, ...] = LEGACY_LENSES
    primary_lens: ClusterLens | None = None
    id_algorithm: str = "legacy_hash"
    signal_source: str = "canonical"
    geo_filter: str = "any"
    tie_breaker: str = "lexical"
    type_resolution: str = "canonical_priority"

    def resolved_primary_lens(self) -> ClusterLens:
        if self.primary_lens is not None:
            return self.primary_lens
        if self.active_lenses:
            return self.active_lenses[0]
        return ClusterLens.TOPIC_MICRO

    @staticmethod
    def _dominant_for_profiles(profiles: list[StoryProfileSignals]) -> dict[str, str]:
        merged_dimensions: dict[str, list[str]] = defaultdict(list)
        for profile in profiles:
            for key, value in merged_signals(profile).items():
                merged_dimensions[key].append(str(value))
        return {key: dominant_value(values) for key, values in merged_dimensions.items()}

    def build_view(
        self,
        *,
        lens: ClusterLens,
        profiles: tuple[StoryProfileSignals, ...],
        mode: ClusteringMode,
        id_algorithm: str | None = None,
    ) -> ClusterView:
        id_alg = self.id_algorithm if id_algorithm is None else id_algorithm
        buckets: dict[str, list[StoryProfileSignals]] = defaultdict(list)
        for profile in sorted(profiles, key=lambda item: item.story_id):
            buckets[cluster_key_for_lens(profile, lens)].append(profile)

        clusters: list[Cluster] = []
        for key in sorted(buckets.keys()):
            bucket_profiles = buckets[key]
            members = tuple(ClusterMember(story_id=item.story_id) for item in bucket_profiles)
            c_score, c_factors = readiness_score_for_cluster(lens=lens, members=members, mode=mode)
            dominant_bucket = ClusteringEngine._dominant_for_profiles(bucket_profiles)
            clusters.append(
                Cluster(
                    cluster_id=stable_cluster_id(lens, key, id_algorithm=id_alg),
                    lens=lens,
                    members=members,
                    readiness_score=c_score,
                    readiness_factors=dict(c_factors),
                    key=key,
                )
            )

        primary = max(clusters, key=lambda cluster: len(cluster.members)) if clusters else None
        if primary is not None:
            dominant_primary = ClusteringEngine._dominant_for_profiles(buckets[primary.key])
            narrative = build_cluster_narrative(
                lens=lens, members=primary.members, dominant=dominant_primary
            )
            view_score = max(c.readiness_score for c in clusters) if clusters else 0
            view_factors = dict(primary.readiness_factors)
        else:
            narrative = f"lens={lens.value}; empty_view"
            view_score = 0
            view_factors = {}

        return ClusterView(
            lens=lens,
            mode=mode,
            clusters=tuple(clusters),
            narrative=narrative,
            readiness_score=view_score,
            readiness_factors=view_factors,
        )

    def memberships(
        self,
        profiles: tuple[StoryProfileSignals, ...],
        *,
        id_algorithm: str | None = None,
    ) -> dict[str, dict[str, str]]:
        """Map story_id -> {lens: cluster_id} for all active lenses."""
        id_alg = self.id_algorithm if id_algorithm is None else id_algorithm
        result: dict[str, dict[str, str]] = {}
        for lens in self.active_lenses:
            view = self.build_view(
                lens=lens,
                profiles=profiles,
                mode=ClusteringMode.ISSUE_READY,
                id_algorithm=id_alg,
            )
            for cluster in view.clusters:
                for member in cluster.members:
                    result.setdefault(member.story_id, {})[lens.value] = cluster.cluster_id
        return result

    def readiness_for_story(
        self,
        story_id: str,
        profiles: tuple[StoryProfileSignals, ...],
        primary_lens: ClusterLens,
        *,
        id_algorithm: str | None = None,
    ) -> tuple[int, dict[str, int]]:
        id_alg = self.id_algorithm if id_algorithm is None else id_algorithm
        view = self.build_view(
            lens=primary_lens,
            profiles=profiles,
            mode=ClusteringMode.ISSUE_READY,
            id_algorithm=id_alg,
        )
        for cluster in view.clusters:
            if any(m.story_id == story_id for m in cluster.members):
                return cluster.readiness_score, dict(cluster.readiness_factors)
        return 0, {}

    def dominant_signals(self, profiles: tuple[StoryProfileSignals, ...]) -> dict[str, str]:
        return ClusteringEngine._dominant_for_profiles(list(profiles))
