"""GW-SSR-11 T03: public dict named sidecar; no payload dump; private paths filtered."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from core.application.issue_create import (
    IssueCreateCommand,
    IssueCreateService,
    StoryPromotionProjectionBridge,
)
from core.infrastructure.repositories import InMemoryStoryRepository
from core.projection import IssueProjectionService, project_card_fields
from core.projection.dto import DOGEIssue
from core.promotion import IssuePromotionService
from core.promotion.gates import PromotionGatePolicy
from core.promotion.repositories import (
    InMemoryIssueCandidateStore,
    InMemoryReviewAuditLogRepository,
)
from core.schema import LocalSchemaRuntime, SchemaRef
from tests.test_gw_ssr_04_schema_driven_cluster_lens import _pack_story

GATEWAY_ROOT = Path(__file__).resolve().parents[1]
PACKS_ROOT = GATEWAY_ROOT / "schema-packs"

CIVIC_REQUIRED = frozenset(
    {"id", "status", "type", "labels", "title", "summary", "description"}
)


def _civic_issue() -> DOGEIssue:
    return DOGEIssue(
        id="i1",
        status="NEW",
        type="IMPROVEMENT",
        labels=("waste",),
        title={"et": "t", "ru": "t", "en": "t"},
        summary={"et": "s", "ru": "s", "en": "s"},
        description={"et": "d", "ru": "d", "en": "d"},
    )


def test_dto_source_has_no_structured_payload_token() -> None:
    text = (GATEWAY_ROOT / "src/core/projection/dto.py").read_text(encoding="utf-8")
    assert "structured_payload" not in text


def test_civic_to_public_dict_unchanged_without_sidecar() -> None:
    public = _civic_issue().to_public_dict()
    assert CIVIC_REQUIRED.issubset(public.keys())
    assert "schema_card" not in public
    assert "structured_payload" not in public
    assert public["type"] == "IMPROVEMENT"
    assert public["status"] == "NEW"


def test_named_sidecar_is_not_payload_dump() -> None:
    public = _civic_issue().to_public_dict(
        schema_card={"institution.office_id": "station-1"}
    )
    assert public["schema_card"] == {"institution.office_id": "station-1"}
    assert "structured_payload" not in public
    assert set(public["schema_card"].keys()) == {"institution.office_id"}


def test_forbidden_and_node_private_filtered_even_if_listed() -> None:
    payload = {
        "institution": {"office_id": "station-1", "name": "HQ"},
        "secret_note": "do-not-leak",
        "internal": {"note": "node-only"},
    }
    card_fields = (
        "institution.office_id",
        "secret_note",
        "internal.note",
        "missing.path",
    )
    field_policy = {
        "secret_note": "forbidden",
        "internal.note": "node_private",
    }
    card = project_card_fields(payload, card_fields, field_policy)
    assert card == {"institution.office_id": "station-1"}
    assert "secret_note" not in card
    assert "internal.note" not in card
    public = _civic_issue().to_public_dict(schema_card=card)
    assert "structured_payload" not in public
    assert "secret_note" not in public
    assert "do-not-leak" not in json.dumps(public)


def test_absent_allowlist_projects_empty_civic_form() -> None:
    payload = {"institution": {"office_id": "station-1"}, "secret_note": "x"}
    assert project_card_fields(payload, (), {"secret_note": "forbidden"}) == {}


def test_public_read_path_is_node_issues() -> None:
    text = (GATEWAY_ROOT / "src/core/api/asgi_app.py").read_text(encoding="utf-8")
    assert '@app.get("/node/issues")' in text
    assert "/tallinn/issues" not in text


def test_schema_runtime_project_stays_stub() -> None:
    runtime = LocalSchemaRuntime(packs_root=PACKS_ROOT)
    with pytest.raises(NotImplementedError):
        runtime.project({}, SchemaRef("legal_process", "v1"))


def test_civic_gate_factory_default_stays_true() -> None:
    assert PromotionGatePolicy.require_actionable_canonical_type is True
    factory = (
        GATEWAY_ROOT / "src/core/infrastructure/service_factory.py"
    ).read_text(encoding="utf-8")
    assert "require_actionable_canonical_type=False" not in factory
    gates = (GATEWAY_ROOT / "src/core/promotion/gates.py").read_text(encoding="utf-8")
    assert "require_actionable_canonical_type: bool = True" in gates


def test_legal_process_without_key_issue_stays_civic_form() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(_pack_story("p1", office_id="station-card"))
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(
                min_readiness_score=40,
                min_stories=1,
                require_actionable_canonical_type=False,
            ),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        packs_root=PACKS_ROOT,
    )
    result = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:legal:card",
            story_ids=("p1",),
            readiness_score=40,
            title="legal",
            min_stories=1,
            gate_policy=PromotionGatePolicy(
                min_readiness_score=40,
                min_stories=1,
                require_actionable_canonical_type=False,
            ),
        )
    )
    assert "structured_payload" not in result.projection
    assert "schema_card" not in result.projection
    assert CIVIC_REQUIRED.issubset(result.projection.keys())


def test_pack_allowlist_named_leaves_on_created_issue(tmp_path: Path) -> None:
    dest = tmp_path / "legal_process" / "v1"
    dest.mkdir(parents=True)
    src = PACKS_ROOT / "legal_process" / "v1"
    shutil.copy(src / "payload.schema.json", dest / "payload.schema.json")
    manifest = json.loads((src / "pack.json").read_text())
    manifest["card_fields"] = [
        "institution.office_id",
        "secret_note",
        "internal.note",
    ]
    manifest["field_policy"]["internal.note"] = "node_private"
    (dest / "pack.json").write_text(json.dumps(manifest), encoding="utf-8")
    ctx = LocalSchemaRuntime(packs_root=tmp_path).resolve(SchemaRef("legal_process", "v1"))
    assert ctx.card_fields == (
        "institution.office_id",
        "secret_note",
        "internal.note",
    )

    stories = InMemoryStoryRepository()
    stories.save_story(
        _pack_story(
            "p1",
            office_id="station-allow",
            extra_payload={
                "secret_note": "do-not-leak",
                "internal": {"note": "node-only"},
            },
        )
    )
    service = IssueCreateService(
        promotion_service=IssuePromotionService(
            candidates=InMemoryIssueCandidateStore(),
            audit_log=InMemoryReviewAuditLogRepository(),
            gate_policy=PromotionGatePolicy(
                min_readiness_score=40,
                min_stories=1,
                require_actionable_canonical_type=False,
            ),
        ),
        projection_service=IssueProjectionService(),
        bridge=StoryPromotionProjectionBridge(story_repository=stories),
        packs_root=tmp_path,
    )
    result = service.create_issue(
        IssueCreateCommand(
            cluster_id="cluster:legal:allow",
            story_ids=("p1",),
            readiness_score=40,
            title="legal",
            min_stories=1,
            gate_policy=PromotionGatePolicy(
                min_readiness_score=40,
                min_stories=1,
                require_actionable_canonical_type=False,
            ),
        )
    )
    public = result.projection
    assert "structured_payload" not in public
    assert public["schema_card"] == {"institution.office_id": "station-allow"}
    assert "secret_note" not in public
    assert "do-not-leak" not in json.dumps(public)
    assert "node-only" not in json.dumps(public)
    assert CIVIC_REQUIRED.issubset(public.keys())
