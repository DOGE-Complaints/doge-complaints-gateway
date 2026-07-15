from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping

from core.domain import StoryGeoSnapshot


class ClusterLens(StrEnum):
    """Civic clustering lenses (canonical_labels-based, multilingual-safe)."""

    COMPOSITE_PRIMARY_MICRO = "composite_primary_micro"
    CIVIC_DOMAIN_MICRO = "civic_domain_micro"
    FAILURE_PATTERN_MICRO = "failure_pattern_micro"
    CIVIC_WEIGHT_SYSTEMIC = "civic_weight_systemic"
    DESIRED_OUTCOME_LOCAL = "desired_outcome_local"
    AFFECTED_GROUP_LOCAL = "affected_group_local"
    GEOGRAPHIC_DISTRICT_MICRO = "geographic_district_micro"
    SERVICE_OBJECT_MICRO = "service_object_micro"
    DEEP_NEED_LOCAL = "deep_need_local"
    ECOSYSTEM_SIGNAL_SYSTEMIC = "ecosystem_signal_systemic"


class ClusteringMode(StrEnum):
    ANALYTIC = "analytic"
    ISSUE_READY = "issue_ready"


@dataclass(frozen=True)
class StoryProfileSignals:
    story_id: str
    signals: Mapping[str, str]
    geo: StoryGeoSnapshot | None = None


@dataclass(frozen=True)
class ClusterMember:
    story_id: str


@dataclass(frozen=True)
class Cluster:
    cluster_id: str
    lens: ClusterLens
    members: tuple[ClusterMember, ...]
    readiness_score: int = 0
    readiness_factors: Mapping[str, int] = field(default_factory=dict)
    key: str = ""


@dataclass(frozen=True)
class ClusterView:
    lens: ClusterLens
    mode: ClusteringMode
    clusters: tuple[Cluster, ...]
    narrative: str
    readiness_score: int
    readiness_factors: Mapping[str, int]
