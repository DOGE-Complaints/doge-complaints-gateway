from __future__ import annotations

from typing import Any, Mapping

from core.evidence.types import EvidencePackRecord, VisibilityTier


def redact_evidence_pack(pack: EvidencePackRecord, tier: VisibilityTier) -> Mapping[str, Any]:
    """Apply visibility tier: public summary vs internal full vs export pilot bundle."""
    if tier == VisibilityTier.INTERNAL:
        return _full_dict(pack)
    if tier == VisibilityTier.PUBLIC:
        if _is_sensitive(pack.privacy_classification):
            return {
                "issue_id": pack.issue_id,
                "story_count": len(pack.story_ids),
                "tokenization_readiness": pack.tokenization_readiness,
                "schema_version": pack.schema_version,
                "privacy_classification": pack.privacy_classification,
            }
        return {
            "issue_id": pack.issue_id,
            "pack_id": pack.pack_id,
            "story_count": len(pack.story_ids),
            "cluster_id": pack.cluster_snapshot.cluster_id,
            "lens": pack.cluster_snapshot.lens,
            "tokenization_readiness": pack.tokenization_readiness,
            "schema_version": pack.schema_version,
        }
    # EXPORT: expanded but still no raw artifact payloads (metadata only)
    return {
        "issue_id": pack.issue_id,
        "pack_id": pack.pack_id,
        "story_ids": list(pack.story_ids),
        "cluster_snapshot": {
            "cluster_id": pack.cluster_snapshot.cluster_id,
            "lens": pack.cluster_snapshot.lens,
            "lens_version": pack.cluster_snapshot.lens_version,
            "captured_at_iso": pack.cluster_snapshot.captured_at_iso,
        },
        "privacy_classification": pack.privacy_classification,
        "tokenization_readiness": pack.tokenization_readiness,
        "supporting_artifact_refs": list(pack.supporting_artifact_refs),
        "schema_version": pack.schema_version,
        "lineage_snapshot_version": pack.lineage_snapshot_version,
    }


def _is_sensitive(privacy_classification: str) -> bool:
    value = privacy_classification.strip().lower()
    return value in {"restricted", "pii", "pii_high", "internal_only"}


def _full_dict(pack: EvidencePackRecord) -> dict[str, Any]:
    return {
        "pack_id": pack.pack_id,
        "issue_id": pack.issue_id,
        "cluster_snapshot": {
            "cluster_id": pack.cluster_snapshot.cluster_id,
            "lens": pack.cluster_snapshot.lens,
            "lens_version": pack.cluster_snapshot.lens_version,
            "captured_at_iso": pack.cluster_snapshot.captured_at_iso,
        },
        "story_ids": list(pack.story_ids),
        "privacy_classification": pack.privacy_classification,
        "tokenization_readiness": pack.tokenization_readiness,
        "supporting_artifact_refs": list(pack.supporting_artifact_refs),
        "schema_version": pack.schema_version,
        "lineage_snapshot_version": pack.lineage_snapshot_version,
    }
