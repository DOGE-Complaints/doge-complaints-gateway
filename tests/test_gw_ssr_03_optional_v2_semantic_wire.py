"""GW-SSR-03: optional schema_binding on m2.story_intake_envelope.v2."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.api.asgi_app import app
from core.application import StoryIntakeService
from core.cluster.types import ClusterLens
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.infrastructure.db_supabase import REQUIRED_READINESS_TABLES, SupabaseDatabase
from core.intake import (
    INTAKE_SCHEMA_VERSION,
    IntakeValidationError,
    Submitter,
    intake_request_from_stash_and_submitter,
    parse_story_draft_stash_request,
    parse_story_intake_request,
)
from core.schema.payload import payload_hash_for
from tests.intake_v2_fixtures import valid_v2_intake_payload, valid_v2_stash_payload

CLUSTERLENS_BASELINE = (
    "composite_primary_micro",
    "civic_domain_micro",
    "failure_pattern_micro",
    "civic_weight_systemic",
    "desired_outcome_local",
    "affected_group_local",
    "geographic_district_micro",
    "service_object_micro",
    "deep_need_local",
    "ecosystem_signal_systemic",
)
LEGAL_BINDING = {
    "schema_id": "legal_process",
    "schema_version": "v1",
    "profile_id": "legal_access",
    "profile_version": "1",
    "structured_payload": {"institution": {"office_id": "s1", "name": "Tallinn"}},
}


def _intake_service() -> StoryIntakeService:
    return StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
    )


def test_clusterlens_baseline_unchanged() -> None:
    assert tuple(member.value for member in ClusterLens) == CLUSTERLENS_BASELINE


def test_absent_schema_binding_is_civic_legacy() -> None:
    request = parse_story_intake_request(valid_v2_intake_payload())
    assert request.schema_version == INTAKE_SCHEMA_VERSION
    assert request.schema_binding is None
    saved = _intake_service().create_story(request).story
    assert saved.schema_version == INTAKE_SCHEMA_VERSION
    assert saved.schema_id is None
    assert saved.bound_schema_version is None
    assert saved.structured_payload is None
    assert saved.payload_hash is None


def test_empty_schema_binding_object_is_civic() -> None:
    request = parse_story_intake_request(valid_v2_intake_payload(schema_binding={}))
    assert request.schema_binding is None
    saved = _intake_service().create_story(request).story
    assert saved.schema_id is None
    assert saved.structured_payload is None


def test_present_schema_binding_persists_and_hashes_server_side() -> None:
    request = parse_story_intake_request(valid_v2_intake_payload(schema_binding=LEGAL_BINDING))
    assert request.schema_binding is not None
    assert request.schema_binding.schema_id == "legal_process"
    assert request.schema_binding.schema_version == "v1"
    saved = _intake_service().create_story(request).story
    assert saved.schema_version == INTAKE_SCHEMA_VERSION
    assert saved.schema_id == "legal_process"
    assert saved.bound_schema_version == "v1"
    assert saved.profile_id == "legal_access"
    assert saved.profile_version == "1"
    assert saved.structured_payload == LEGAL_BINDING["structured_payload"]
    assert saved.payload_hash == payload_hash_for(LEGAL_BINDING["structured_payload"])


def test_unknown_inner_keys_rejected() -> None:
    with pytest.raises(IntakeValidationError, match="Unknown schema_binding keys"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                schema_binding={**LEGAL_BINDING, "payload_hash": "client-hash"}
            )
        )


def test_inner_schema_version_must_not_equal_envelope() -> None:
    with pytest.raises(IntakeValidationError, match="must not equal envelope"):
        parse_story_intake_request(
            valid_v2_intake_payload(
                schema_binding={
                    **LEGAL_BINDING,
                    "schema_version": INTAKE_SCHEMA_VERSION,
                }
            )
        )


def test_invalid_structured_payload_rejected_not_silent() -> None:
    with pytest.raises(IntakeValidationError):
        _intake_service().create_story(
            parse_story_intake_request(
                valid_v2_intake_payload(
                    schema_binding={
                        **LEGAL_BINDING,
                        "structured_payload": {"not_institution": True},
                    }
                )
            )
        )


def test_stash_and_submit_share_binding() -> None:
    stash = parse_story_draft_stash_request(
        valid_v2_stash_payload(schema_binding=LEGAL_BINDING)
    )
    assert stash.schema_binding is not None
    bridged = intake_request_from_stash_and_submitter(
        stash,
        submitter=Submitter(
            external_user_id="opaque-user-123",
            identity_issuer="https://idp.example.com/eid",
        ),
    )
    assert bridged.schema_binding == stash.schema_binding
    saved = _intake_service().create_story(bridged).story
    assert saved.schema_id == "legal_process"
    assert saved.bound_schema_version == "v1"
    assert saved.payload_hash == payload_hash_for(LEGAL_BINDING["structured_payload"])


def test_get_tallinn_issues_route_stays() -> None:
    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/tallinn/issues" in paths
    assert not any(
        path and ("schema-filter" in path or "story_dimensions" in path)
        for path in paths
        if isinstance(path, str)
    )


def test_required_readiness_tables_unchanged_stories_member() -> None:
    assert "stories" in REQUIRED_READINESS_TABLES
    assert "story_dimensions" not in REQUIRED_READINESS_TABLES


def test_required_columns_ready_omits_binding_names() -> None:
    import inspect

    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for token in ("schema_id", "bound_schema_version", "structured_payload", "payload_hash"):
        assert token not in source


def test_dogeissue_public_dict_has_no_structured_payload() -> None:
    from core.projection.dto import DOGEIssue

    source = Path(__file__).resolve().parents[1] / "src/core/projection/dto.py"
    text = source.read_text(encoding="utf-8")
    assert "structured_payload" not in text
    issue = DOGEIssue(
        id="i1",
        status="open",
        type="complaint",
        labels=(),
        title={"en": "t", "et": "t", "ru": "t"},
        summary={"en": "s", "et": "s", "ru": "s"},
        description={"en": "d", "et": "d", "ru": "d"},
    )
    assert "structured_payload" not in issue.to_public_dict()
