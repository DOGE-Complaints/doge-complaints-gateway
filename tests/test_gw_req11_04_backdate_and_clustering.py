"""GW-REQ11-04 — lock-B created_at backdate + clustering handoff docs (contract)."""

from __future__ import annotations

import sys
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.domain import StoryLifecycleStatus
from core.infrastructure.db_sqlite import SqliteDatabase, SqliteStoryRepository
from core.infrastructure.repositories import InMemoryStoryRepository
from tests.conftest import GAUTH_TEST_SERVICE_TOKEN, gauth_intake_headers
from tests.intake_v2_fixtures import make_story_record

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import simulation_intake_http as intake_http  # noqa: E402


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("SERVICE_API_TOKEN", GAUTH_TEST_SERVICE_TOKEN)
    monkeypatch.setenv("NODE_SCHEMA_ID", "tallinn_civic")
    monkeypatch.setenv("NODE_SCHEMA_VERSION", "v1")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def test_ac01_repo_update_created_at_inmemory_and_sqlite() -> None:
    target = datetime(2026, 12, 10, 13, 3, 3, tzinfo=UTC)
    sqlite_db = SqliteDatabase.from_url("sqlite:///:memory:")
    sqlite_db.ensure_schema()
    for repo in (InMemoryStoryRepository(), SqliteStoryRepository(sqlite_db)):
        story = make_story_record(
            story_id=f"req11-04-backdate-{repo.__class__.__name__}",
            lifecycle_status=StoryLifecycleStatus.ACCEPTED,
        )
        repo.save_story(story)
        assert story.created_at != target
        repo.update_created_at(story.story_id, target)
        fetched = repo.get_story(story.story_id)
        assert fetched is not None
        assert fetched.created_at == target


def test_ac01_ops_backdate_requires_service_auth(client: TestClient) -> None:
    response = client.patch(
        "/ops/stories/missing/created-at",
        json={"created_at": "2026-12-10T13:03:03Z"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "UNAUTHORIZED"


def test_ac01_ops_backdate_happy_path(client: TestClient) -> None:
    from core.api.asgi_app import get_api_dependencies

    deps = get_api_dependencies()
    story = make_story_record(
        story_id="req11-04-http-1",
        lifecycle_status=StoryLifecycleStatus.ACCEPTED,
    )
    deps.story_intake_service.repository.save_story(story)
    target = "2026-06-22T03:13:46Z"
    response = client.patch(
        f"/ops/stories/{story.story_id}/created-at",
        headers=gauth_intake_headers(),
        json={"created_at": target},
    )
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["story_id"] == story.story_id
    assert data["created_at"] == target
    fetched = deps.story_intake_service.repository.get_story(story.story_id)
    assert fetched is not None
    assert fetched.created_at == datetime(2026, 6, 22, 3, 13, 46, tzinfo=UTC)


def test_ac01_ops_backdate_not_public_intake_field() -> None:
    """Lock B: stash/submit bodies must not grow a public created_at invent."""
    from core.api.asgi_app import PUBLIC_ROUTES

    assert "/ops/stories/{story_id}/created-at" not in PUBLIC_ROUTES
    assert "/intake/stories" not in PUBLIC_ROUTES


def test_ac01_helper_patch_story_created_at_http_wires_lock_b(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, str, bytes]] = []

    def _fake_post(
        url: str,
        *,
        bearer_token: str,
        body: bytes,
        method: str = "POST",
    ) -> tuple[int, str]:
        calls.append((method, url, body))
        return 200, '{"data":{"story_id":"s1","created_at":"2026-01-01T00:00:00Z"}}'

    monkeypatch.setattr(intake_http, "_post_bytes", _fake_post)
    status, text = intake_http.patch_story_created_at_http(
        gateway_url="http://gw.test",
        service_token="svc-token",
        story_id="s1",
        created_at="2026-01-01T00:00:00Z",
    )
    assert status == 200
    assert "created_at" in text
    assert calls[0][0] == "PATCH"
    assert calls[0][1].endswith("/ops/stories/s1/created-at")
    assert b'"created_at": "2026-01-01T00:00:00Z"' in calls[0][2] or (
        b'"created_at":"2026-01-01T00:00:00Z"' in calls[0][2]
    )


def test_ac02_ac03_clustering_handoff_docs_present() -> None:
    note = (
        Path(__file__).resolve().parents[1]
        / "docs"
        / "analysis"
        / "note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md"
    )
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert "CLUSTER_MIN_SIZE" in text
    assert "CLUSTER_CRON" in text
    assert "K3" in text
    assert "threads" in text.lower()
    assert "no invent" in text.lower() or "do not invent" in text.lower()
    assert "/ops/stories/" in text
    assert "lock B" in text or "lock-B" in text or "Lock B" in text
