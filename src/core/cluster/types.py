from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Mapping


class ClusterLens(StrEnum):
    """Canonical clustering lenses (EPIC-M2-04 baseline + civic target-state set)."""

    TOPIC_MICRO = "topic_micro"
    NEED_LOCAL = "need_local"
    FAILURE_SYSTEMIC = "failure_systemic"
    FAILURE_MICRO = "failure_micro"
    REPEATABILITY_LOCAL = "repeatability_local"
    RELEVANCE_SYSTEMIC = "relevance_systemic"
    CIVIC_DOMAIN_MICRO = "civic_domain_micro"
    FAILURE_PATTERN_MICRO = "failure_pattern_micro"
    CIVIC_WEIGHT_SYSTEMIC = "civic_weight_systemic"
    DESIRED_OUTCOME_LOCAL = "desired_outcome_local"
    AFFECTED_GROUP_LOCAL = "affected_group_local"
    GEOGRAPHIC_DISTRICT_MICRO = "geographic_district_micro"


class ClusteringMode(StrEnum):
    ANALYTIC = "analytic"
    ISSUE_READY = "issue_ready"


@dataclass(frozen=True)
class StoryProfileSignals:
    story_id: str
    signals: Mapping[str, str]


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
