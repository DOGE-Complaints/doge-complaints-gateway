from __future__ import annotations

from datetime import UTC, datetime

from core.evidence.types import EvidenceExportMetadata, EvidencePackRecord

BUNDLE_FORMAT = "m2.evidence_bundle.v1"


def build_export_metadata(pack: EvidencePackRecord) -> EvidenceExportMetadata:
    """Export-ready header for pilot adapters (off-chain in demo)."""
    return EvidenceExportMetadata(
        pack_id=pack.pack_id,
        issue_id=pack.issue_id,
        schema_version=pack.schema_version,
        bundle_format=BUNDLE_FORMAT,
        generated_at_iso=datetime.now(tz=UTC).replace(microsecond=0).isoformat(),
        story_count=len(pack.story_ids),
    )
