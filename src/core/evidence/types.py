from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class VisibilityTier(StrEnum):
    """Who may consume evidence payloads (architecture/08)."""

    PUBLIC = "public"
    INTERNAL = "internal"
    EXPORT = "export"


@dataclass(frozen=True)
class ClusterSnapshotRef:
    cluster_id: str
    lens: str
    lens_version: str
    captured_at_iso: str


@dataclass(frozen=True)
class EvidencePackRecord:
    """Evidence pack stored separately from SPA issue card (EPIC-M2-07)."""

    pack_id: str
    issue_id: str
    cluster_snapshot: ClusterSnapshotRef
    story_ids: tuple[str, ...]
    privacy_classification: str
    tokenization_readiness: bool
    supporting_artifact_refs: tuple[str, ...]
    schema_version: str
    lineage_snapshot_version: int


@dataclass(frozen=True)
class EvidenceExportMetadata:
    """Pilot/export bundle header (no on-chain anchoring in demo)."""

    pack_id: str
    issue_id: str
    schema_version: str
    bundle_format: str
    generated_at_iso: str
    story_count: int
