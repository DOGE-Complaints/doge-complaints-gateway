from __future__ import annotations

from collections.abc import Iterator
import sqlite3
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.intake import INTAKE_SCHEMA_VERSION


@pytest.fixture()
def sqlite_db_url(tmp_path: Path) -> str:
    db_path = tmp_path / "gateway-db.sqlite3"
    return f"sqlite:///{db_path}"


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, sqlite_db_url: str) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", sqlite_db_url)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _sqlite_path_from_url(database_url: str) -> Path:
    return Path(database_url.removeprefix("sqlite:///"))


def _intake_payload(index: int) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": f"db-e2e-user-{index}"},
        "narrative": {
            "original_text": f"Infrastructure issue #{index} in district center with safety impact.",
            "language": "en",
            "title_hint": f"Issue #{index}",
        },
    }


def test_db_backed_pipeline_persists_stories_projections_and_embeddings(
    client: TestClient,
    sqlite_db_url: str,
) -> None:
    client.post("/intake/stories", json=_intake_payload(1))
    client.post("/intake/stories", json=_intake_payload(2))

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        stories_count = connection.execute("SELECT COUNT(*) FROM stories").fetchone()[0]
        story_embeddings_count = connection.execute(
            "SELECT COUNT(*) FROM story_embeddings"
        ).fetchone()[0]
        projections_count = connection.execute(
            "SELECT COUNT(*) FROM doge_issues"
        ).fetchone()[0]
        projection_embeddings_count = connection.execute(
            "SELECT COUNT(*) FROM doge_issue_embeddings"
        ).fetchone()[0]
        persisted_issue = connection.execute(
            "SELECT issue_id FROM doge_issues LIMIT 1"
        ).fetchone()
    finally:
        connection.close()

    connection = sqlite3.connect(db_path)
    try:
        table_names = {
            str(row[0])
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        story_cols = {str(row[1]) for row in connection.execute("PRAGMA table_info(stories)")}
    finally:
        connection.close()

    assert "story_signals" in table_names
    assert "cluster_memberships" in table_names
    assert "geo_latitude" in story_cols
    assert "geo_longitude" in story_cols
    assert "geo_normalized_label" in story_cols

    assert stories_count == 2
    assert story_embeddings_count >= 2
    assert projections_count >= 1
    assert projection_embeddings_count >= 1
    assert persisted_issue is not None


def test_readiness_reports_sqlite_backend(client: TestClient) -> None:
    response = client.get("/ready")
    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["db"]["backend"] == "sqlite"
    assert payload["db"]["ready"] is True
    assert payload["db"]["checks"]["connectivity"] is True


def test_http_idempotency_deduplication_sqlite_same_key_different_payload(
    client: TestClient,
    sqlite_db_url: str,
) -> None:
    """TC-22: same idempotency-key must yield one story_id and one DB row (HTTP + sqlite)."""
    idem_key = "tcr-p1-01-idem-dedup-sqlite"
    headers = {"idempotency-key": idem_key, "x-trace-id": "tcr-p1-01-dedup"}

    r1 = client.post("/intake/stories", json=_intake_payload(101), headers=headers)
    r2 = client.post(
        "/intake/stories",
        json=_intake_payload(202),
        headers={**headers, "x-trace-id": "tcr-p1-01-dedup-2"},
    )
    assert r1.status_code == 200
    assert r2.status_code == 200
    sid1 = r1.json()["data"]["story_id"]
    sid2 = r2.json()["data"]["story_id"]
    assert sid1 == sid2

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        idem_count = connection.execute(
            "SELECT COUNT(*) FROM idempotency_keys WHERE key = ?",
            (idem_key,),
        ).fetchone()[0]
        stories_count = connection.execute("SELECT COUNT(*) FROM stories").fetchone()[0]
    finally:
        connection.close()

    assert idem_count == 1
    assert stories_count == 1
