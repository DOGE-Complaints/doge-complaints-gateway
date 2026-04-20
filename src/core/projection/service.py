from __future__ import annotations

from dataclasses import dataclass

from core.projection.dto import SpaIssueProjection
from core.projection.input import ProjectionInput
from core.projection.mapper import project_distinct_issue
from core.projection.policy import PROJECTION_POLICY_VERSION


@dataclass(frozen=True)
class IssueProjectionService:
    """Application service: SPA-compatible projection (isolated from cluster/promotion engines)."""

    policy_version: str = PROJECTION_POLICY_VERSION

    def project(self, data: ProjectionInput) -> SpaIssueProjection:
        return project_distinct_issue(data)
