from __future__ import annotations

from collections.abc import Iterator
import json
import sqlite3
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from tests.intake_v2_fixtures import intake_payload_simple, valid_v2_intake_payload
from tests.story_draft_intake_helpers import (
    patch_identity_me_verified,
    post_intake_via_story_drafts,
    stash_story_draft,
    submit_story_draft,
    submitter_external_id,
)


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
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _sqlite_path_from_url(database_url: str) -> Path:
    return Path(database_url.removeprefix("sqlite:///"))


def _intake_payload(index: int) -> dict[str, object]:
    return intake_payload_simple(
        external_user_id=f"db-e2e-user-{index}",
        original_text=f"Infrastructure issue #{index} in district center with safety impact.",
        title_en=f"Issue #{index}",
    )


def test_db_backed_pipeline_persists_stories_projections_and_embeddings(
    client: TestClient,
    sqlite_db_url: str,
) -> None:
    post_intake_via_story_drafts(
        client, json=_intake_payload(1))
    post_intake_via_story_drafts(
        client, json=_intake_payload(2))
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()

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


def test_sqlite_intake_v2_narrative_i18n_roundtrip(client: TestClient) -> None:
    payload = valid_v2_intake_payload()
    response = post_intake_via_story_drafts(
        client, json=payload)
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]

    record = get_api_dependencies().story_intake_service.repository.get_story(story_id)
    assert record is not None
    assert record.narrative_title == payload["narrative"]["title"]
    assert record.narrative_description == payload["narrative"]["description"]
    assert record.narrative_session_language == payload["narrative"]["session_language"]


def test_http_idempotency_deduplication_sqlite_same_key_different_payload(
    client: TestClient,
    sqlite_db_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """TC-22: resubmitting the same draft yields one story_id and one DB row (sqlite)."""
    idem_key = "tcr-p1-01-idem-dedup-sqlite"
    headers = {"idempotency-key": idem_key, "x-trace-id": "tcr-p1-01-dedup"}
    payload = _intake_payload(101)

    draft_id = stash_story_draft(client, payload, headers=headers)
    patch_identity_me_verified(monkeypatch, sub=submitter_external_id(payload))
    r1 = submit_story_draft(client, draft_id, headers=headers)
    r2 = submit_story_draft(
        client, draft_id, headers={**headers, "x-trace-id": "tcr-p1-01-dedup-2"}
    )
    assert r1.status_code == 202
    assert r2.status_code == 202
    sid1 = r1.json()["data"]["story_id"]
    sid2 = r2.json()["data"]["story_id"]
    assert sid1 == sid2

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        idem_count = connection.execute(
            "SELECT COUNT(*) FROM idempotency_keys WHERE key = ?",
            (draft_id,),
        ).fetchone()[0]
        stories_count = connection.execute("SELECT COUNT(*) FROM stories").fetchone()[0]
    finally:
        connection.close()

    assert idem_count == 1
    assert stories_count == 1


def test_sqlite_living_issue_extend_persists_merged_candidate_and_audit(
    client: TestClient,
    sqlite_db_url: str,
) -> None:
    post_intake_via_story_drafts(
        client, json=_intake_payload(1))
    post_intake_via_story_drafts(
        client, json=_intake_payload(2))
    deps = get_api_dependencies()
    first_issue_ids = deps.story_cluster_orchestrator.process_all_pending()
    assert len(first_issue_ids) == 1
    issue_id = first_issue_ids[0]

    post_intake_via_story_drafts(
        client, json=_intake_payload(3))
    post_intake_via_story_drafts(
        client, json=_intake_payload(4))
    second_issue_ids = deps.story_cluster_orchestrator.process_all_pending()
    assert second_issue_ids == [issue_id]

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        story_ids_json = connection.execute(
            "SELECT story_ids_json FROM issue_candidates WHERE candidate_id = ?",
            (issue_id,),
        ).fetchone()
        assert story_ids_json is not None
        merged_story_ids = set(json.loads(str(story_ids_json[0])))
        assert len(merged_story_ids) == 4

        audit_rows = connection.execute(
            """
            SELECT rationale
            FROM review_audit_log
            WHERE candidate_id = ?
            ORDER BY audit_id ASC
            """,
            (issue_id,),
        ).fetchall()
        assert [str(row[0]) for row in audit_rows] == [
            "http_create_issue_auto_promote",
            "cluster_growth_extend",
        ]

        persisted_description = connection.execute(
            "SELECT description_json FROM doge_issues WHERE issue_id = ?",
            (issue_id,),
        ).fetchone()
        assert persisted_description is not None
        description_payload = json.loads(str(persisted_description[0]))
        description = description_payload.get("en", "")
        # GW-L10N-01: description from dominant_story i18n (oldest on tie), not full aggregate.
        assert "issue #1" in description.lower()
        assert "issue #4" not in description.lower()
    finally:
        connection.close()
