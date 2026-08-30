"""GW-SSR-17: intake requires schema_binding == NODE_SCHEMA_*; mismatch/absent → 4xx."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.application import StoryIntakeService
from core.cluster.types import ClusterLens
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.intake import IntakeValidationError, parse_story_draft_stash_request, parse_story_intake_request
from gw_ssr_16_node_schema import (
    DEFAULT_TEST_NODE_SCHEMA_ID,
    DEFAULT_TEST_NODE_SCHEMA_VERSION,
    active_node_schema_binding,
)
from tests.intake_v2_fixtures import valid_v2_intake_payload, valid_v2_stash_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts

LEGAL_BINDING = {
    "schema_id": "legal_process",
    "schema_version": "v1",
    "profile_id": "legal_access",
    "profile_version": "1",
    "structured_payload": {"institution": {"office_id": "s1", "name": "Tallinn"}},
}


def _omit_binding(payload: dict) -> dict:
    body = dict(payload)
    body.pop("schema_binding", None)
    return body


def _service(*, schema_id: str, schema_version: str) -> StoryIntakeService:
    return StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        node_schema_id=schema_id,
        node_schema_version=schema_version,
    )


def test_parse_absent_binding_raises() -> None:
    with pytest.raises(IntakeValidationError, match="schema_binding"):
        parse_story_intake_request(_omit_binding(valid_v2_intake_payload()))


def test_parse_empty_and_null_binding_raise() -> None:
    with pytest.raises(IntakeValidationError, match="schema_binding"):
        parse_story_intake_request(valid_v2_intake_payload(schema_binding={}))
    with pytest.raises(IntakeValidationError, match="schema_binding"):
        parse_story_intake_request(valid_v2_intake_payload(schema_binding=None))


def test_stash_absent_binding_raises() -> None:
    with pytest.raises(IntakeValidationError, match="schema_binding"):
        parse_story_draft_stash_request(_omit_binding(valid_v2_stash_payload()))


def test_mismatch_id_or_version_raises() -> None:
    service = _service(
        schema_id=DEFAULT_TEST_NODE_SCHEMA_ID,
        schema_version=DEFAULT_TEST_NODE_SCHEMA_VERSION,
    )
    request = parse_story_intake_request(valid_v2_intake_payload(schema_binding=LEGAL_BINDING))
    with pytest.raises(IntakeValidationError, match="NODE_SCHEMA"):
        service.create_story(request)
    request_v = parse_story_intake_request(
        valid_v2_intake_payload(
            schema_binding=active_node_schema_binding(schema_version="v9-missing")
        )
    )
    with pytest.raises(IntakeValidationError, match="NODE_SCHEMA"):
        service.create_story(request_v)


def test_match_validates_active_pack_and_persists() -> None:
    service = _service(
        schema_id=DEFAULT_TEST_NODE_SCHEMA_ID,
        schema_version=DEFAULT_TEST_NODE_SCHEMA_VERSION,
    )
    binding = active_node_schema_binding()
    request = parse_story_intake_request(valid_v2_intake_payload(schema_binding=binding))
    saved = service.create_story(request).story
    assert saved.schema_id == DEFAULT_TEST_NODE_SCHEMA_ID
    assert saved.bound_schema_version == DEFAULT_TEST_NODE_SCHEMA_VERSION
    assert saved.structured_payload == binding["structured_payload"]
    assert saved.payload_hash


def test_http_absent_binding_is_4xx() -> None:
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        response = post_intake_via_story_drafts(client, json=_omit_binding(valid_v2_intake_payload()))
    _clear_api_dependencies_cache()
    assert response.status_code == 400


def test_http_mismatch_is_4xx() -> None:
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        response = post_intake_via_story_drafts(
            client, json=valid_v2_intake_payload(schema_binding=LEGAL_BINDING)
        )
    _clear_api_dependencies_cache()
    assert response.status_code == 400


def test_http_match_is_202() -> None:
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        response = post_intake_via_story_drafts(
            client, json=valid_v2_intake_payload(schema_binding=active_node_schema_binding())
        )
    _clear_api_dependencies_cache()
    assert response.status_code == 202, response.text
    assert response.json()["data"]["story_id"]


def test_clusterlens_baseline_ten() -> None:
    assert len(tuple(ClusterLens)) == 10
