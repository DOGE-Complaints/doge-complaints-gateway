from __future__ import annotations

import os
from collections.abc import Iterator
from uuid import uuid4

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.infrastructure.db_supabase import SupabaseDatabase
from core.intake import INTAKE_SCHEMA_VERSION


def _require_live_http_env() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_TEST_URL", "").strip()
    key = os.environ.get("SUPABASE_TEST_SERVICE_ROLE", "").strip()
    if not url or not key:
        pytest.skip("SUPABASE_TEST_URL/SUPABASE_TEST_SERVICE_ROLE are not configured.")
    return url, key


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    supabase_url, service_role_key = _require_live_http_env()
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "20")
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv("SUPABASE_URL", supabase_url)
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", service_role_key)
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _payload(external_user_id: str, text: str) -> dict[str, object]:
    return {
        "schema_version": INTAKE_SCHEMA_VERSION,
        "submitter": {"external_user_id": external_user_id},
        "narrative": {
            "original_text": text,
            "language": "en",
            "title_hint": "TC100 H01 full pipeline",
        },
        "origin": {"source": "tc100_h01_live_e2e"},
    }


def test_supabase_live_full_pipeline_roundtrip(client: TestClient) -> None:
    supabase_url, service_role_key = _require_live_http_env()
    db = SupabaseDatabase.from_http(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
    )
    run_id = f"tc100-h01-{uuid4()}"
    idem_a = f"{run_id}-idem-a"
    idem_b = f"{run_id}-idem-b"

    response_a = client.post(
        "/intake/stories",
        json=_payload(f"{run_id}-u1", f"{run_id} street lights issue"),
        headers={"idempotency-key": idem_a, "x-trace-id": f"{run_id}-trace-a"},
    )
    response_b = client.post(
        "/intake/stories",
        json=_payload(f"{run_id}-u2", f"{run_id} street lights issue"),
        headers={"idempotency-key": idem_b, "x-trace-id": f"{run_id}-trace-b"},
    )
    assert response_a.status_code == 202
    assert response_b.status_code == 202
    get_api_dependencies().story_cluster_orchestrator.process_all_pending()

    story_id_a = str(response_a.json()["data"]["story_id"])
    story_id_b = str(response_b.json()["data"]["story_id"])
    assert story_id_a != story_id_b

    stories_rows = db._request(
        method="GET",
        path="/rest/v1/stories",
        params={
            "select": "story_id",
            "story_id": f"in.(\"{story_id_a}\",\"{story_id_b}\")",
        },
    )
    assert len(stories_rows) == 2

    embeddings_rows = db._request(
        method="GET",
        path="/rest/v1/story_embeddings",
        params={
            "select": "story_id",
            "story_id": f"in.(\"{story_id_a}\",\"{story_id_b}\")",
        },
    )
    assert len(embeddings_rows) >= 2

    idempotency_rows = db._request(
        method="GET",
        path="/rest/v1/idempotency_keys",
        params={
            "select": "key,story_id",
            "key": f"in.(\"{idem_a}\",\"{idem_b}\")",
        },
    )
    assert len(idempotency_rows) == 2

    link_rows = db._request(
        method="GET",
        path="/rest/v1/issue_story_links",
        params={
            "select": "issue_id,story_id",
            "story_id": f"in.(\"{story_id_a}\",\"{story_id_b}\")",
        },
    )
    assert link_rows
    issue_ids = {str(row["issue_id"]) for row in link_rows}
    assert issue_ids

    first_issue = next(iter(issue_ids))
    candidate_rows = db._request(
        method="GET",
        path="/rest/v1/issue_candidates",
        params={
            "select": "candidate_id,status",
            "candidate_id": db._eq_filter(first_issue),
            "limit": "1",
        },
    )
    assert candidate_rows
    assert candidate_rows[0]["status"] == "promoted"

    audit_rows = db._request(
        method="GET",
        path="/rest/v1/review_audit_log",
        params={
            "select": "candidate_id,decision",
            "candidate_id": db._eq_filter(first_issue),
        },
    )
    assert audit_rows

    projection_rows = db._request(
        method="GET",
        path="/rest/v1/doge_issues",
        params={
            "select": "issue_id,status",
            "issue_id": db._eq_filter(first_issue),
            "limit": "1",
        },
    )
    assert projection_rows
    assert projection_rows[0]["status"] == "PUBLISHED"

    projection_embedding_rows = db._request(
        method="GET",
        path="/rest/v1/doge_issue_embeddings",
        params={
            "select": "issue_id,embedding_policy_version",
            "issue_id": db._eq_filter(first_issue),
        },
    )
    assert projection_embedding_rows
