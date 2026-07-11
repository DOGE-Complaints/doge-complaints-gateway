from __future__ import annotations

import logging
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from pathlib import Path

import pytest  # pyright: ignore[reportMissingImports]
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

from core.api.asgi_app import _clear_api_dependencies_cache, app
from core.application import StoryIntakeService
from core.geo import GeoResolverChain, GeoResolverPolicy, GeoService, default_provider_chain
from core.geo.metrics import InMemoryGeoMetrics
from core.geo.repositories import InMemoryGeoCacheRepository
from core.infrastructure import InMemoryIdempotencyRepository, InMemoryStoryRepository
from core.infrastructure.repositories import InMemoryStorySignalStore
from core.intake import parse_story_intake_request
from tests.intake_v2_fixtures import valid_v2_intake_payload
from tests.story_draft_intake_helpers import post_intake_via_story_drafts


@pytest.fixture()
def demo_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    _clear_api_dependencies_cache()
    with TestClient(app) as client:
        yield client
    _clear_api_dependencies_cache()


def _geo_service() -> GeoService:
    metrics = InMemoryGeoMetrics()
    chain = GeoResolverChain(
        providers=default_provider_chain(),
        policy=GeoResolverPolicy(max_attempts_per_provider=2),
        metrics=metrics,
    )
    return GeoService(
        cache=InMemoryGeoCacheRepository(),
        resolver=chain,
        metrics=metrics,
    )


def test_http_intake_response_includes_intake_notes(demo_client: TestClient) -> None:
    response = post_intake_via_story_drafts(
        demo_client,
        json=valid_v2_intake_payload(narrative={"location_query": "Tallinn"}),
    )
    assert response.status_code == 202
    notes = response.json()["data"]["intake_notes"]
    assert notes["geo_resolved"] is True
    assert notes["gpt_signals_persisted"] is True


def test_intake_notes_geo_false_without_location_query() -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=_geo_service(),
    )
    result = service.create_story(parse_story_intake_request(valid_v2_intake_payload()))
    assert result.geo_resolved is False
    assert result.gpt_signals_persisted is True


@dataclass
class _FailingStorySignalStore:
    def save_signals(
        self, story_id: str, policy: str, signals: Mapping[str, str]
    ) -> None:
        del story_id, policy, signals
        raise RuntimeError("simulated persist failure")

    def get_signals(self, story_id: str, policy: str) -> Mapping[str, str] | None:
        del story_id, policy
        return None


def test_intake_notes_gpt_signals_persist_failed_when_save_raises(
    caplog: pytest.LogCaptureFixture,
) -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
        story_signal_store=_FailingStorySignalStore(),
    )
    with caplog.at_level(logging.WARNING):
        result = service.create_story(
            parse_story_intake_request(
                valid_v2_intake_payload(
                    gpt_signals={
                        "severity": "HIGH",
                        "impact_estimation": "DISTRICT",
                        "problem_status": "ONGOING",
                    }
                )
            )
        )
    assert result.story.story_id
    assert result.gpt_signals_persisted is False
    assert any(
        record.getMessage() == "intake.gpt_signals_persist_failed"
        for record in caplog.records
    )


def test_idempotent_replay_gpt_signals_persisted_true_when_signals_stored() -> None:
    signal_store = InMemoryStorySignalStore()
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
        story_signal_store=signal_store,
    )
    payload = valid_v2_intake_payload(
        gpt_signals={
            "severity": "MEDIUM",
            "impact_estimation": "CITY",
            "problem_status": "UNKNOWN",
        }
    )
    request = parse_story_intake_request(payload)
    first = service.create_story(request, idempotency_key="idem-req46-g1")
    assert first.gpt_signals_persisted is True
    second = service.create_story(request, idempotency_key="idem-req46-g1")
    assert second.story.story_id == first.story.story_id
    assert second.gpt_signals_persisted is True


def test_intake_notes_gpt_signals_drop_when_store_missing(
    caplog: pytest.LogCaptureFixture,
) -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=None,
        story_signal_store=None,
    )
    with caplog.at_level(logging.WARNING):
        result = service.create_story(
            parse_story_intake_request(
                valid_v2_intake_payload(
                    gpt_signals={
                        "severity": "HIGH",
                        "impact_estimation": "DISTRICT",
                        "problem_status": "ONGOING",
                    }
                )
            )
        )
    assert result.gpt_signals_persisted is False
    assert any(
        "intake.gpt_signals_drop" in record.message for record in caplog.records
    )


def test_geo_not_resolved_logs_info_for_unknown_location(
    caplog: pytest.LogCaptureFixture,
) -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=_geo_service(),
    )
    with caplog.at_level(logging.INFO):
        result = service.create_story(
            parse_story_intake_request(
                valid_v2_intake_payload(
                    narrative={"location_query": "unknown-place-xyz-123"}
                )
            )
        )
    assert result.geo_resolved is False
    assert any(
        "intake.geo_not_resolved" in record.message for record in caplog.records
    )


def test_geo_skip_debug_when_no_location_query(
    caplog: pytest.LogCaptureFixture,
) -> None:
    service = StoryIntakeService(
        repository=InMemoryStoryRepository(),
        idempotency_repository=InMemoryIdempotencyRepository(),
        geo_service=_geo_service(),
    )
    with caplog.at_level(logging.DEBUG):
        service.create_story(parse_story_intake_request(valid_v2_intake_payload()))
    assert any(
        record.message == "intake.geo_skip" for record in caplog.records
    )


def test_sqlite_intake_persists_gpt_signals_when_store_configured(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("REQUEST_TIMEOUT_S", "15")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'req46.sqlite'}")
    monkeypatch.setenv("SUPABASE_URL", "")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "")
    _clear_api_dependencies_cache()
    try:
        with TestClient(app) as client:
            response = post_intake_via_story_drafts(
        client,
                json=valid_v2_intake_payload(
                    gpt_signals={
                        "severity": "MEDIUM",
                        "impact_estimation": "CITY",
                        "problem_status": "UNKNOWN",
                    },
                    narrative={"location_query": "Tallinn"},
                ),
            )
    finally:
        _clear_api_dependencies_cache()
    assert response.status_code == 202
    notes = response.json()["data"]["intake_notes"]
    assert notes["geo_resolved"] is True
    assert notes["gpt_signals_persisted"] is True
