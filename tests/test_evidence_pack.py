from __future__ import annotations

from core.application import StoryIntakeService
from core.evidence import (
    BUNDLE_FORMAT,
    ClusterSnapshotRef,
    EvidencePackService,
    InMemoryEvidencePackRepository,
    VisibilityTier,
)
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import INTAKE_SCHEMA_VERSION
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict


def _snapshot() -> ClusterSnapshotRef:
    return ClusterSnapshotRef(
        cluster_id="c-1",
        lens="civic_domain_micro",
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


def test_public_view_for_sensitive_pack_is_more_restricted() -> None:
    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    svc.upsert_pack(
        issue_id="issue-2",
        cluster_snapshot=_snapshot(),
        story_ids=("s1",),
        privacy_classification="restricted",
        tokenization_readiness=False,
        supporting_artifact_refs=("secret-ref",),
    )
    public = svc.view("issue-2", VisibilityTier.PUBLIC)
    assert public is not None
    assert "pack_id" not in public
    assert "cluster_id" not in public
    assert public["privacy_classification"] == "restricted"


def test_lineage_story_ids_allow_fetching_submitter_identity() -> None:
    story_repo = InMemoryStoryRepository()
    intake_service = StoryIntakeService(
        repository=story_repo,
        idempotency_repository=InMemoryIdempotencyRepository(),
    )
    req = parse_story_intake_request(
        {
            "schema_version": INTAKE_SCHEMA_VERSION,
            "submitter": {
                "external_user_id": "author-1",
                "identity_issuer": "idp://partner",
            },
            "narrative": {
            "original_text": "Story for lineage proof.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Lineage proof story"},
            "description": {"et": "d", "ru": "d", "en": "Story for lineage proof."},
            },
        }
    )
    story = intake_service.create_story(req).story

    repo = InMemoryEvidencePackRepository()
    svc = EvidencePackService(repository=repo)
    svc.upsert_pack(
        issue_id="issue-lineage",
        cluster_snapshot=_snapshot(),
        story_ids=(story.story_id,),
        privacy_classification="pii_min",
        tokenization_readiness=True,
    )
    linked_story_ids = svc.lineage_stories("issue-lineage")
    assert linked_story_ids == (story.story_id,)

    linked_story = story_repo.get_story(linked_story_ids[0])
    assert linked_story is not None
    assert linked_story.submitter_external_user_id == "author-1"
