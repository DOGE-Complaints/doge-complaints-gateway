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
            "SELECT COUNT(*) FROM spa_issue_projections"
        ).fetchone()[0]
        projection_embeddings_count = connection.execute(
            "SELECT COUNT(*) FROM spa_issue_projection_embeddings"
        ).fetchone()[0]
        persisted_issue = connection.execute(
            "SELECT issue_id FROM spa_issue_projections LIMIT 1"
        ).fetchone()
    finally:
        connection.close()

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
