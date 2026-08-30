"""GW-ES-03: Emerging L2 unit + public HTTP smoke + Issues regression + ≠ Issues shape."""

from __future__ import annotations
from tests.civic_pack_overrides import monkeypatch_civic_knobs

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import PUBLIC_ROUTES, _clear_api_dependencies_cache, app
from core.application.emerging_signals import EmergingSignalsService
from core.domain import StoryLabel
from core.infrastructure.repositories import (
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemoryStoryLabelRepository,
    InMemoryStoryRepository,
)
from core.projection.enums import DOGEIssueStatus
from tests.conftest import GAUTH_TEST_IDENTITY_URL, GAUTH_TEST_SERVICE_TOKEN
from tests.intake_v2_fixtures import make_story_record


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("STORY_DRAFT_TTL_SECONDS", "86400")
    monkeypatch.setenv("IDENTITY_BASE_URL", GAUTH_TEST_IDENTITY_URL)
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("CLUSTER_READINESS_THRESHOLD", "1")
    monkeypatch_civic_knobs(monkeypatch, min_size=int("1"), readiness_threshold=int("1"))
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _service() -> tuple[
    EmergingSignalsService,
    InMemoryStoryRepository,
    InMemoryStoryLabelRepository,
    InMemoryIssueStoryLinkStore,
    InMemoryIssueProjectionStore,
]:
    stories = InMemoryStoryRepository()
    labels = InMemoryStoryLabelRepository()
    links = InMemoryIssueStoryLinkStore()
    projections = InMemoryIssueProjectionStore()
    svc = EmergingSignalsService(
        story_repository=stories,
        story_label_repository=labels,
        issue_story_link_store=links,
        issue_projection_read_store=projections,
    )
    return svc, stories, labels, links, projections


def test_emerging_excludes_published_linked_and_ranks_top_n() -> None:
    svc, stories, labels, links, projections = _service()

    stories.save_story(
        make_story_record(
            story_id="es03-a",
            narrative_original_text="secret narrative A",
            submitter_external_user_id="opaque-a",
        )
    )
    stories.save_story(make_story_record(story_id="es03-b"))
    stories.save_story(make_story_record(story_id="es03-c"))

    labels.save_labels(
        (
            StoryLabel(
                story_id="es03-a",
                axis="topic_domain",
                label="transport",
                disposition="canonical",
            ),
            StoryLabel(
                story_id="es03-a",
                axis="topic_domain",
                label="secret_internal",
                disposition="internal",
            ),
            StoryLabel(
                story_id="es03-b",
                axis="topic_domain",
                label="transport",
                disposition="canonical",
            ),
            StoryLabel(
                story_id="es03-c",
                axis="topic_domain",
                label="housing",
                disposition="canonical",
            ),
        )
    )

    # es03-c linked to published Issue — its housing label must not appear
    links.save_issue_story_links(
        issue_id="iss-pub",
        cluster_id="cl-1",
        story_ids=("es03-c",),
    )
    projections.save_projection(
        issue_id="iss-pub",
        status=DOGEIssueStatus.PUBLISHED.value,
        payload={"title": {"et": "x"}, "summary": {"et": "y"}, "description": {"et": "z"}},
        policy_version="test",
    )

    # es03-b linked to in-review — still counts (not published)
    links.save_issue_story_links(
        issue_id="iss-review",
        cluster_id="cl-2",
        story_ids=("es03-b",),
    )
    projections.save_projection(
        issue_id="iss-review",
        status=DOGEIssueStatus.IN_REVIEW.value,
        payload={"title": {"et": "d"}, "summary": {"et": "d"}, "description": {"et": "d"}},
        policy_version="test",
    )

    result = svc.build_emerging(top_n=5)
    assert result["top_n"] == 5
    assert result["signals"] == [
        {"label": "transport", "axis": "topic_domain", "story_count": 2},
    ]
    blob = str(result)
    assert "submitter" not in blob
    assert "secret narrative" not in blob
    assert "opaque-a" not in blob
    assert "secret_internal" not in blob
    assert "housing" not in blob
    assert "stories_until" not in blob.lower()
    assert "issue_id" not in blob
    assert "issues" not in result


def test_emerging_top_n_clamp() -> None:
    svc, stories, labels, _, _ = _service()
    stories.save_story(make_story_record(story_id="solo"))
    labels.save_labels(
        (
            StoryLabel(
                story_id="solo",
                axis="topic_domain",
                label="roads",
                disposition="canonical",
            ),
        )
    )
    assert svc.build_emerging(top_n=0)["top_n"] == 1
    assert svc.build_emerging(top_n=100)["top_n"] == 50


def test_emerging_payload_shape_differs_from_issues_list() -> None:
    """Contract: Emerging data ≠ Issues projection list envelope (no data.issues)."""
    svc, stories, labels, _, _ = _service()
    stories.save_story(make_story_record(story_id="shape-1"))
    labels.save_labels(
        (
            StoryLabel(
                story_id="shape-1",
                axis="topic_domain",
                label="noise",
                disposition="canonical",
            ),
        )
    )
    emerging = svc.build_emerging()
    assert set(emerging.keys()) == {"signals", "top_n"}
    assert "issues" not in emerging
    assert all("issue" not in row for row in emerging["signals"][0])


def test_gw_es_03_public_get_without_auth_returns_200(client: TestClient) -> None:
    assert "/node/emerging-signals" in PUBLIC_ROUTES
    response = client.get("/node/emerging-signals")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    data = body["data"]
    assert "signals" in data
    assert "top_n" in data
    assert "issues" not in data
    assert "submitter" not in str(data)
    assert "stories_until" not in str(data).lower()


def test_gw_es_03_top_n_query_applied(client: TestClient) -> None:
    response = client.get("/node/emerging-signals", params={"top_n": 3})
    assert response.status_code == 200
    assert response.json()["data"]["top_n"] == 3


def test_gw_es_03_issues_list_regression_still_public(client: TestClient) -> None:
    response = client.get("/node/issues")
    assert response.status_code == 200
    assert "issues" in response.json()["data"]


def test_gw_es_03_emerging_http_not_issues_shape(client: TestClient) -> None:
    emerging = client.get("/node/emerging-signals").json()["data"]
    issues = client.get("/node/issues").json()["data"]
    assert "signals" in emerging
    assert "issues" in issues
    assert emerging.keys() != issues.keys()
