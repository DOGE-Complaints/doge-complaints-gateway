from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

from core.evidence.export_meta import build_export_metadata
from core.evidence.redaction import redact_evidence_pack
from core.evidence.repositories import EvidencePackRepository
from core.evidence.types import (
    ClusterSnapshotRef,
    EvidenceExportMetadata,
    EvidencePackRecord,
    VisibilityTier,
)


@dataclass(frozen=True)
class EvidencePackService:
    repository: EvidencePackRepository

    def upsert_pack(
        self,
        *,
        issue_id: str,
        cluster_snapshot: ClusterSnapshotRef,
        story_ids: tuple[str, ...],
        privacy_classification: str,
        tokenization_readiness: bool,
        supporting_artifact_refs: tuple[str, ...] = (),
        schema_version: str = "m2.evidence_pack.v1",
        lineage_snapshot_version: int = 1,
    ) -> EvidencePackRecord:
        existing = self.repository.get_by_issue(issue_id)
        version = (
            lineage_snapshot_version
            if existing is None
            else existing.lineage_snapshot_version + 1
        )
        pack_id = existing.pack_id if existing is not None else str(uuid4())
        pack = EvidencePackRecord(
            pack_id=pack_id,
            issue_id=issue_id,
            cluster_snapshot=cluster_snapshot,
            story_ids=story_ids,
            privacy_classification=privacy_classification,
            tokenization_readiness=tokenization_readiness,
            supporting_artifact_refs=supporting_artifact_refs,
            schema_version=schema_version,
            lineage_snapshot_version=version,
        )
        return self.repository.save(pack)

    def get_pack(self, issue_id: str) -> EvidencePackRecord | None:
        return self.repository.get_by_issue(issue_id)

    def lineage_stories(self, issue_id: str) -> tuple[str, ...]:
        pack = self.repository.get_by_issue(issue_id)
        if pack is None:
            return ()
        return pack.story_ids

    def reverse_lineage(self, story_id: str) -> tuple[str, ...]:
        return self.repository.list_pack_ids_for_story(story_id)

    def view(self, issue_id: str, tier: VisibilityTier):
        pack = self.repository.get_by_issue(issue_id)
        if pack is None:
            return None
        return redact_evidence_pack(pack, tier)

    def export_metadata(self, issue_id: str) -> EvidenceExportMetadata | None:
        pack = self.repository.get_by_issue(issue_id)
        if pack is None:
            return None
        return build_export_metadata(pack)
