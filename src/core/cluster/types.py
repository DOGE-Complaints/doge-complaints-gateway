from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping


class ClusterLens(StrEnum):
    """Canonical clustering lenses (minimum required set for EPIC-M2-04)."""

    TOPIC_MICRO = "topic_micro"
    NEED_LOCAL = "need_local"
    FAILURE_SYSTEMIC = "failure_systemic"
    FAILURE_MICRO = "failure_micro"
    REPEATABILITY_LOCAL = "repeatability_local"
    RELEVANCE_SYSTEMIC = "relevance_systemic"


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


@dataclass(frozen=True)
class ClusterView:
    lens: ClusterLens
    mode: ClusteringMode
    clusters: tuple[Cluster, ...]
    narrative: str
    readiness_score: int
    readiness_factors: Mapping[str, int]
