from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.intake import INTAKE_SCHEMA_VERSION
from tests.intake_v2_fixtures import intake_payload_simple


@pytest.fixture()
def sqlite_db_url(tmp_path: Path) -> str:
    db_path = tmp_path / "cross-layer-db.sqlite3"
    return f"sqlite:///{db_path}"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, sqlite_db_url: str) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", sqlite_db_url)
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _sqlite_path_from_url(database_url: str) -> Path:
    return Path(database_url.removeprefix("sqlite:///"))


def _intake_payload(user_idx: int) -> dict[str, object]:
    return intake_payload_simple(
        external_user_id=f"cross-layer-user-{user_idx}",
        original_text=f"Cross-layer infra issue #{user_idx} in district center.",
        title_en=f"Cross-layer issue {user_idx}",
        origin={"source": "tc_p1_03_cross_layer"},
    )


def _count(connection: sqlite3.Connection, table: str) -> int:
    return int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])


def test_cross_layer_api_app_infra_side_effects_roundtrip(
    client: TestClient,
    sqlite_db_url: str,
) -> None:
    ok_1 = client.post("/intake/stories", json=_intake_payload(1), headers={"idempotency-key": "cross-1"})
    ok_2 = client.post("/intake/stories", json=_intake_payload(2), headers={"idempotency-key": "cross-2"})
    bad = client.post(
        "/intake/stories",
        json={"schema_version": INTAKE_SCHEMA_VERSION, "submitter": {"external_user_id": "broken"}},
        headers={"idempotency-key": "cross-bad"},
    )

    assert ok_1.status_code == 202
    assert ok_2.status_code == 202
    assert bad.status_code == 400
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        stories_count = _count(connection, "stories")
        story_embeddings_count = _count(connection, "story_embeddings")
        issue_candidates_count = _count(connection, "issue_candidates")
        projections_count = _count(connection, "doge_issues")
        projection_embeddings_count = _count(connection, "doge_issue_embeddings")
        issue_links_count = _count(connection, "issue_story_links")
        review_audit_count = _count(connection, "review_audit_log")
        idempotency_count = _count(connection, "idempotency_keys")
    finally:
        connection.close()

    # Positive side-effects across infra stores after two valid API calls.
    assert stories_count == 2
    assert story_embeddings_count >= 2
    assert issue_candidates_count >= 1
    assert projections_count >= 1
    assert projection_embeddings_count >= 1
    assert issue_links_count >= 2
    assert review_audit_count >= 1
    # Negative branch should not create idempotency for failed payload.
    assert idempotency_count == 2
