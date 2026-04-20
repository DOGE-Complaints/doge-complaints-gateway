from __future__ import annotations

from core.evidence import (
    BUNDLE_FORMAT,
    ClusterSnapshotRef,
    EvidencePackService,
    InMemoryEvidencePackRepository,
    VisibilityTier,
)


def _snapshot() -> ClusterSnapshotRef:
    return ClusterSnapshotRef(
        cluster_id="c-1",
        lens="topic_micro",
        lens_version="v1",
        captured_at_iso="2026-04-20T12:00:00+00:00",
    )


def test_upsert_and_lineage() -> None:
    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    svc.upsert_pack(
        issue_id="issue-1",
        cluster_snapshot=_snapshot(),
        story_ids=("s1", "s2"),
        privacy_classification="pii_min",
        tokenization_readiness=True,
        supporting_artifact_refs=("ref-a",),
    )
    assert svc.lineage_stories("issue-1") == ("s1", "s2")
    assert svc.reverse_lineage("s1") != ()


def test_public_view_omits_artifacts() -> None:
    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    svc.upsert_pack(
        issue_id="issue-1",
        cluster_snapshot=_snapshot(),
        story_ids=("s1",),
        privacy_classification="pii_min",
        tokenization_readiness=False,
        supporting_artifact_refs=("secret-ref",),
    )
    public = svc.view("issue-1", VisibilityTier.PUBLIC)
    assert public is not None
    assert "supporting_artifact_refs" not in public
    assert public["story_count"] == 1


def test_export_metadata_shape() -> None:
    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    svc.upsert_pack(
        issue_id="issue-1",
        cluster_snapshot=_snapshot(),
        story_ids=("s1", "s2"),
        privacy_classification="pii_min",
        tokenization_readiness=True,
    )
    meta = svc.export_metadata("issue-1")
    assert meta is not None
    assert meta.bundle_format == BUNDLE_FORMAT
    assert meta.story_count == 2
    assert meta.issue_id == "issue-1"


def test_lineage_snapshot_version_increments() -> None:
    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    a = svc.upsert_pack(
        issue_id="issue-1",
        cluster_snapshot=_snapshot(),
        story_ids=("s1",),
        privacy_classification="pii_min",
        tokenization_readiness=False,
    )
    b = svc.upsert_pack(
        issue_id="issue-1",
        cluster_snapshot=_snapshot(),
        story_ids=("s1", "s2"),
        privacy_classification="pii_min",
        tokenization_readiness=True,
    )
    assert b.lineage_snapshot_version == a.lineage_snapshot_version + 1
    assert a.pack_id == b.pack_id
