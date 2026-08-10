"""GW-ES-02: Network Pulse L1 unit + public HTTP smoke + Issues regression."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import PUBLIC_ROUTES, _clear_api_dependencies_cache, app
from core.application.network_pulse import NetworkPulseService
from core.domain import StoryGeoSnapshot, StoryLabel, StoryLifecycleStatus
from core.infrastructure.repositories import (
    InMemoryStoryLabelRepository,
    InMemoryStoryRepository,
)
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
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_network_pulse_service_aggregates_dims_and_excludes_pii() -> None:
    now = datetime(2026, 8, 10, 12, 0, 0, tzinfo=UTC)
    stories = InMemoryStoryRepository()
    labels = InMemoryStoryLabelRepository()

    geo = StoryGeoSnapshot(
        normalized_label="tallinn",
        latitude=59.4,
        longitude=24.7,
        confidence=1.0,
        provider="test",
        admin_district="Kesklinn",
    )
    s1 = make_story_record(
        story_id="es02-1",
        narrative_language="et",
        created_at=now - timedelta(days=1),
        updated_at=now - timedelta(days=1),
        geo=geo,
        narrative_original_text="secret narrative",
        submitter_external_user_id="opaque-a",
    )
    s2 = make_story_record(
        story_id="es02-2",
        narrative_language="et",
        created_at=now - timedelta(days=10),
        updated_at=now - timedelta(days=10),
        geo=StoryGeoSnapshot(
            normalized_label="tallinn",
            latitude=59.4,
            longitude=24.7,
            confidence=1.0,
            provider="test",
            admin_settlement="Mustamäe",
        ),
        lifecycle_status=StoryLifecycleStatus.READY_FOR_PROFILE,
    )
    s3 = make_story_record(
        story_id="es02-3",
        narrative_language="",
        created_at=now - timedelta(days=2),
        updated_at=now - timedelta(days=2),
    )
    stories.save_story(s1)
    stories.save_story(s2)
    stories.save_story(s3)
    labels.save_labels(
        (
            StoryLabel(
                story_id="es02-1",
                axis="topic_domain",
                label="transport",
                disposition="canonical",
            ),
            StoryLabel(
                story_id="es02-1",
                axis="topic_domain",
                label="secret_internal",
                disposition="internal",
            ),
            StoryLabel(
                story_id="es02-2",
                axis="topic_domain",
                label="transport",
                disposition="canonical",
            ),
        )
    )

    pulse = NetworkPulseService(
        story_repository=stories,
        story_label_repository=labels,
    ).build_pulse(now=now)

    assert pulse["stories_collected"] == 3
    assert pulse["recent_stories_7d"] == 2
    assert pulse["languages"] == [{"key": "et", "count": 2}]
    assert {"key": "Kesklinn", "count": 1} in pulse["areas"]
    assert {"key": "Mustamäe", "count": 1} in pulse["areas"]
    assert pulse["topics"] == [
        {"label": "transport", "axis": "topic_domain", "count": 2}
    ]
    blob = str(pulse)
    assert "submitter" not in blob
    assert "secret narrative" not in blob
    assert "opaque-a" not in blob
    assert "secret_internal" not in blob
    assert "stories_until" not in blob.lower()
    assert all("issue" not in row for row in ("stories_collected", "languages", "areas", "topics", "recent_stories_7d"))
    assert all(t["label"] != "secret_internal" for t in pulse["topics"])
    assert "Issue" not in {k for row in pulse["topics"] for k in row}


def test_network_pulse_service_topics_empty_without_label_repo() -> None:
    stories = InMemoryStoryRepository()
    stories.save_story(make_story_record(story_id="solo"))
    pulse = NetworkPulseService(story_repository=stories).build_pulse()
    assert pulse["stories_collected"] == 1
    assert pulse["topics"] == []


def test_gw_es_02_public_get_without_auth_returns_200(client: TestClient) -> None:
    assert "/tallinn/network-pulse" in PUBLIC_ROUTES
    response = client.get("/tallinn/network-pulse")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    data = body["data"]
    assert "stories_collected" in data
    assert "languages" in data
    assert "areas" in data
    assert "topics" in data
    assert "recent_stories_7d" in data
    assert "submitter" not in str(data)
    assert "stories_until" not in str(data).lower()


def test_gw_es_02_issues_list_regression_still_public(client: TestClient) -> None:
    response = client.get("/tallinn/issues")
    assert response.status_code == 200
    assert "issues" in response.json()["data"]
