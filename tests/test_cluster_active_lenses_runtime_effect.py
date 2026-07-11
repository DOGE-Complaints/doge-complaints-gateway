from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.intake import INTAKE_SCHEMA_VERSION
from tests.intake_v2_fixtures import intake_payload_simple, make_story_record, narrative_dict
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


@pytest.fixture()
def sqlite_db_url(tmp_path: Path) -> str:
    db_path = tmp_path / "cluster-active-lenses.sqlite3"
    return f"sqlite:///{db_path}"


def _sqlite_path_from_url(database_url: str) -> Path:
    return Path(database_url.removeprefix("sqlite:///"))


def _payload(idx: int) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": f"cluster-lens-user-{idx}", "identity_issuer": "https://idp.example.com/eid"},
        "narrative": {
            "original_text": "Street lights are broken and unsafe in district center.",
            "language": "en",
            "session_language": "en",
            "title": {"et": "t", "ru": "t", "en": "Street lights issue"},
            "description": {"et": "d", "ru": "d", "en": "Street lights are broken and unsafe in district center."},
            "canonical_type": "complaint",
            "canonical_labels": ["roads", "broken_infrastructure", "safety"],
        },
    }


def _run_for_lens(
    monkeypatch: pytest.MonkeyPatch, sqlite_db_url: str, cluster_active_lenses: str
) -> str:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", sqlite_db_url)
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    monkeypatch.setenv("CLUSTER_ACTIVE_LENSES", cluster_active_lenses)
    primary = cluster_active_lenses.split(",")[0].strip()
    monkeypatch.setenv("CLUSTER_PRIMARY_LENS", primary)
    monkeypatch.setenv("CLUSTER_SIGNAL_SOURCE", "canonical")
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        r1 = post_intake_via_story_drafts(
        client, json=_payload(1))
        r2 = post_intake_via_story_drafts(
        client, json=_payload(2))
    _clear_api_dependencies_cache()
    assert r1.status_code == 202
    assert r2.status_code == 202
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()

    db_path = _sqlite_path_from_url(sqlite_db_url)
    connection = sqlite3.connect(db_path)
    try:
        row = connection.execute(
            "SELECT cluster_id FROM issue_story_links ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    finally:
        connection.close()
    assert row is not None
    return str(row[0])


def test_cluster_active_lenses_changes_runtime_cluster_id_prefix(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    domain_db = f"sqlite:///{tmp_path / 'lens-domain.sqlite3'}"
    failure_db = f"sqlite:///{tmp_path / 'lens-failure.sqlite3'}"

    domain_cluster_id = _run_for_lens(monkeypatch, domain_db, "civic_domain_micro")
    failure_cluster_id = _run_for_lens(monkeypatch, failure_db, "failure_pattern_micro")

    assert domain_cluster_id.startswith("cluster:civic_domain_micro:")
    assert failure_cluster_id.startswith("cluster:failure_pattern_micro:")
    assert domain_cluster_id != failure_cluster_id
