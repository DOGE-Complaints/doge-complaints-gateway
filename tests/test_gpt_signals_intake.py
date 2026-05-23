from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app, get_api_dependencies
from core.application.services import GPT_CLASSIFIER_POLICY_VERSION
from core.infrastructure.db_sqlite import SqliteStorySignalStore
from core.intake import IntakeValidationError, parse_story_intake_request
from tests.intake_v2_fixtures import valid_v2_intake_payload


@pytest.fixture()
def sqlite_client(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'gpt_signals.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


@pytest.fixture()
def demo_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as test_client:
        yield test_client
    _clear_api_dependencies_cache()


def _payload_with_gpt_signals(**gpt_overrides: Any) -> dict[str, Any]:
    return valid_v2_intake_payload(
        gpt_signals={
            "severity": "HIGH",
            "impact_estimation": "DISTRICT",
            "problem_status": "ONGOING",
            **gpt_overrides,
        }
    )


def _signal_store() -> SqliteStorySignalStore:
    store = get_api_dependencies().story_intake_service.story_signal_store
    assert isinstance(store, SqliteStorySignalStore)
    return store


def test_parse_gpt_signals_valid_enums() -> None:
    request = parse_story_intake_request(
        valid_v2_intake_payload(
            gpt_signals={
                "severity": "high",
                "impact_estimation": "city",
                "problem_status": "unknown",
            }
        )
    )
    assert request.gpt_signals is not None
    assert request.gpt_signals.severity == "HIGH"
    assert request.gpt_signals.impact_estimation == "CITY"
    assert request.gpt_signals.problem_status == "UNKNOWN"


def test_parse_gpt_signals_invalid_severity_raises() -> None:
    with pytest.raises(IntakeValidationError, match="gpt_signals.severity"):
        parse_story_intake_request(
            valid_v2_intake_payload(gpt_signals={"severity": "INVALID"})
        )


def test_parse_omits_gpt_signals_when_key_absent() -> None:
    payload = valid_v2_intake_payload()
    assert "gpt_signals" not in payload
    request = parse_story_intake_request(payload)
    assert request.gpt_signals is None


def test_parse_empty_gpt_signals_object_normalized_to_none() -> None:
    request = parse_story_intake_request(valid_v2_intake_payload(gpt_signals={}))
    assert request.gpt_signals is None


def test_intake_empty_gpt_signals_object_no_classifier_row(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=valid_v2_intake_payload(gpt_signals={}),
        headers={"x-trace-id": "trace-gpt-empty", "idempotency-key": "idem-gpt-empty"},
    )
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]
    assert (
        _signal_store().get_signals(story_id, GPT_CLASSIFIER_POLICY_VERSION) is None
    )


def test_intake_with_gpt_signals_returns_202_and_persists_sqlite(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=_payload_with_gpt_signals(),
        headers={"x-trace-id": "trace-gpt-1", "idempotency-key": "idem-gpt-1"},
    )
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]

    row = _signal_store().get_signals(story_id, GPT_CLASSIFIER_POLICY_VERSION)
    assert row is not None
    assert dict(row) == {
        "severity": "HIGH",
        "impact_estimation": "DISTRICT",
        "problem_status": "ONGOING",
        "source": "gpt_intake_v1",
    }


def test_intake_without_gpt_signals_no_classifier_row(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=valid_v2_intake_payload(),
        headers={"x-trace-id": "trace-gpt-none", "idempotency-key": "idem-gpt-none"},
    )
    assert response.status_code == 202
    story_id = response.json()["data"]["story_id"]
    assert (
        _signal_store().get_signals(story_id, GPT_CLASSIFIER_POLICY_VERSION) is None
    )


def test_intake_invalid_gpt_signals_severity_returns_400(
    sqlite_client: TestClient,
) -> None:
    response = sqlite_client.post(
        "/intake/stories",
        json=_payload_with_gpt_signals(severity="INVALID"),
        headers={"x-trace-id": "trace-gpt-bad", "idempotency-key": "idem-gpt-bad"},
    )
    assert response.status_code == 400


def test_intake_gpt_signals_idempotent_single_classifier_row(
    sqlite_client: TestClient,
) -> None:
    payload = _payload_with_gpt_signals()
    headers = {"x-trace-id": "trace-gpt-idem", "idempotency-key": "idem-gpt-repeat"}
    first = sqlite_client.post("/intake/stories", json=payload, headers=headers)
    second = sqlite_client.post("/intake/stories", json=payload, headers=headers)
    assert first.status_code == 202
    assert second.status_code == 202
    story_id = first.json()["data"]["story_id"]
    assert second.json()["data"]["story_id"] == story_id

    store = _signal_store()
    row = store.get_signals(story_id, GPT_CLASSIFIER_POLICY_VERSION)
    assert row is not None
    assert dict(row)["severity"] == "HIGH"

    cursor = store.db.connection.execute(
        """
        SELECT COUNT(*) FROM story_signals
        WHERE story_id = ? AND extraction_policy = ?
        """,
        (story_id, GPT_CLASSIFIER_POLICY_VERSION),
    )
    assert int(cursor.fetchone()[0]) == 1


def test_intake_gpt_signals_persist_failure_still_returns_202(
    demo_client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    deps = get_api_dependencies()
    store = deps.story_intake_service.story_signal_store
    assert store is not None

    def _boom(*_args: object, **_kwargs: object) -> None:
        raise RuntimeError("signals store unavailable")

    monkeypatch.setattr(store, "save_signals", _boom)

    response = demo_client.post(
        "/intake/stories",
        json=_payload_with_gpt_signals(),
        headers={"x-trace-id": "trace-gpt-fail", "idempotency-key": "idem-gpt-fail"},
    )
    assert response.status_code == 202
    assert response.json()["data"]["story_id"]
