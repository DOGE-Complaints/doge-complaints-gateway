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
from core.geo.scope import geo_filter_bucket, parse_cluster_geo_filter


CIVIC_LENSES: tuple[ClusterLens, ...] = (
    ClusterLens.COMPOSITE_PRIMARY_MICRO,
    ClusterLens.CIVIC_DOMAIN_MICRO,
    ClusterLens.FAILURE_PATTERN_MICRO,
    ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
    ClusterLens.DESIRED_OUTCOME_LOCAL,
    ClusterLens.AFFECTED_GROUP_LOCAL,
    ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
    ClusterLens.SERVICE_OBJECT_MICRO,
    ClusterLens.DEEP_NEED_LOCAL,
    ClusterLens.ECOSYSTEM_SIGNAL_SYSTEMIC,
)

# Backward-compat alias (deprecated name; same as CIVIC_LENSES).
CANONICAL_LENSES: tuple[ClusterLens, ...] = CIVIC_LENSES

_SYSTEMIC_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC,
        ClusterLens.ECOSYSTEM_SIGNAL_SYSTEMIC,
    }
)
_LOCAL_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.DESIRED_OUTCOME_LOCAL,
        ClusterLens.AFFECTED_GROUP_LOCAL,
        ClusterLens.DEEP_NEED_LOCAL,
    }
)
_MICRO_LENSES: frozenset[ClusterLens] = frozenset(
    {
        ClusterLens.COMPOSITE_PRIMARY_MICRO,
        ClusterLens.CIVIC_DOMAIN_MICRO,
        ClusterLens.FAILURE_PATTERN_MICRO,
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO,
        ClusterLens.SERVICE_OBJECT_MICRO,
    }
)


def merged_signals(profile: StoryProfileSignals) -> dict[str, str]:
    merged: dict[str, str] = {}
    merged.update(profile.signals)
    return merged


def lens_dimension(lens: ClusterLens) -> SignalDimension:
    mapping: dict[ClusterLens, SignalDimension] = {
        ClusterLens.COMPOSITE_PRIMARY_MICRO: SignalDimension.CIVIC_DOMAIN,
        ClusterLens.CIVIC_DOMAIN_MICRO: SignalDimension.CIVIC_DOMAIN,
        ClusterLens.FAILURE_PATTERN_MICRO: SignalDimension.FAILURE_PATTERN,
        ClusterLens.CIVIC_WEIGHT_SYSTEMIC: SignalDimension.CIVIC_WEIGHT,
        ClusterLens.DESIRED_OUTCOME_LOCAL: SignalDimension.DESIRED_OUTCOME,
        ClusterLens.AFFECTED_GROUP_LOCAL: SignalDimension.AFFECTED_GROUP,
        ClusterLens.GEOGRAPHIC_DISTRICT_MICRO: SignalDimension.GEOGRAPHIC_DISTRICT,
        ClusterLens.SERVICE_OBJECT_MICRO: SignalDimension.SERVICE_OBJECT,
        ClusterLens.DEEP_NEED_LOCAL: SignalDimension.NEED,
        ClusterLens.ECOSYSTEM_SIGNAL_SYSTEMIC: SignalDimension.ECOSYSTEM_SIGNAL,
    }
    return mapping[lens]


def composite_primary_signal_pair(signals: Mapping[str, str]) -> tuple[str, str]:
    civic_domain = str(signals.get(SignalDimension.CIVIC_DOMAIN.value, "unknown")).strip() or "unknown"
    failure_pattern = (
        str(signals.get(SignalDimension.FAILURE_PATTERN.value, "unknown")).strip() or "unknown"
    )
    return civic_domain, failure_pattern


def composite_primary_cluster_key(
    profile: StoryProfileSignals,
    *,
    geo_filter: str = "country",
) -> str:
    signals = merged_signals(profile)
    civic_domain, failure_pattern = composite_primary_signal_pair(signals)
    base = (
        f"{ClusterLens.COMPOSITE_PRIMARY_MICRO.value}:"
        f"civic_domain+failure_pattern:{civic_domain}+{failure_pattern}:micro"
    )
    geo_part = geo_filter_bucket(profile.geo, geo_filter)
    return f"{base}|{geo_part}"


def cluster_key_for_lens(
    profile: StoryProfileSignals,
    lens: ClusterLens,
    *,
    geo_filter: str = "country",
) -> str:
    if lens == ClusterLens.COMPOSITE_PRIMARY_MICRO:
        return composite_primary_cluster_key(profile, geo_filter=geo_filter)

    signals = merged_signals(profile)
    dimension = lens_dimension(lens)
    raw_value = str(signals.get(dimension.value, "unknown")).strip() or "unknown"

    if lens in _SYSTEMIC_LENSES:
        base = f"{lens.value}:{dimension.value}:{raw_value}:systemic"
    elif lens in _LOCAL_LENSES:
        base = f"{lens.value}:{dimension.value}:{raw_value}:local"
    elif lens in _MICRO_LENSES:
        base = f"{lens.value}:{dimension.value}:{raw_value}:micro"
    else:
        base = f"{lens.value}:{dimension.value}:{raw_value}:micro"
    geo_part = geo_filter_bucket(profile.geo, geo_filter)
    return f"{base}|{geo_part}"


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
        "service_object",
        "need",
        "ecosystem_signal",
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
    """Cluster view builder. Product dominant StoryRecord selection uses
    ``projection.extraction_policy.select_dominant_story`` (REQ-36 alpha_score).
    ``tie_breaker`` is config contract only until signal-level dominant wiring."""

    active_lenses: tuple[ClusterLens, ...] = CIVIC_LENSES
    primary_lens: ClusterLens | None = None
    id_algorithm: str = "sha256"
    signal_source: str = "canonical"
    geo_filter: str = "country"
    tie_breaker: str = "alpha"
    type_resolution: str = "canonical_priority"

    def resolved_primary_lens(self) -> ClusterLens:
        if self.primary_lens is not None:
            return self.primary_lens
        if self.active_lenses:
            return self.active_lenses[0]
        return ClusterLens.COMPOSITE_PRIMARY_MICRO

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
        resolved_geo_filter = parse_cluster_geo_filter(self.geo_filter)
        buckets: dict[str, list[StoryProfileSignals]] = defaultdict(list)
        for profile in sorted(profiles, key=lambda item: item.story_id):
            buckets[
                cluster_key_for_lens(profile, lens, geo_filter=resolved_geo_filter)
            ].append(profile)

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
