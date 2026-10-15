"""GW-REQ57-03: sense-brief sweep / retry (HTTP double, no live aibridge)."""

from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

import httpx
from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

import core.api.asgi_app as asgi_app
from core.application.sense_brief_nudge import (
    ACCEPT_PATH,
    INITIAL_GENERATION_VERSION,
    SenseBriefNudgeService,
    SenseBriefNudgeSettings,
)
from core.application.sense_brief_sweep import (
    SenseBriefSweepService,
    assert_ready_payload_unchanged,
    is_sweep_eligible,
    list_sweep_eligible_issues,
)
from core.application.issue_create import DERIVATION_POLICY_VERSION
from core.infrastructure.repositories import InMemoryIssueProjectionStore
from core.scheduler.sense_brief_sweep_cron import SenseBriefSweepCronJob

_S2S = "req57-03-worker-s2s-token"


@dataclass(frozen=True)
class _LifespanConfigStub:
    cluster_cron_enabled: bool = False
    cluster_cron_interval_s: int = 60
    aibridge_sense_brief_nudge_enabled: bool = False
    log_level: str = "INFO"
    log_format: str = "text"
    log_debug_dir: str | None = None
    db_backend: str = "in_memory"
    node_schema_id: str = "tallinn_civic"
    node_schema_version: str = "v1"
    schema_pack_ready: bool = True


def _sweep_lifespan_deps(*, nudge_enabled: bool) -> Any:
    nudge_svc = object() if nudge_enabled else None
    return SimpleNamespace(
        config=_LifespanConfigStub(aibridge_sense_brief_nudge_enabled=nudge_enabled),
        story_cluster_orchestrator=object(),
        issue_create_service=SimpleNamespace(sense_brief_nudge_service=nudge_svc),
        issue_projection_read_store=InMemoryIssueProjectionStore(),
        db_ready=True,
        db_checks={},
    )


class _RecordingTransport:
    def __init__(self, *, status_code: int = 200) -> None:
        self.status_code = status_code
        self.calls: list[dict[str, Any]] = []

    def post_json(
        self,
        *,
        url: str,
        headers: dict[str, str],
        body: dict[str, Any],
        timeout_s: float,
    ) -> httpx.Response:
        self.calls.append(
            {"url": url, "headers": dict(headers), "body": dict(body), "timeout_s": timeout_s}
        )
        return httpx.Response(self.status_code, json={"ok": True, "idempotent": True})


def _save(
    store: InMemoryIssueProjectionStore,
    *,
    issue_id: str,
    generation_status: str,
    generation_version: str = INITIAL_GENERATION_VERSION,
    poster_url: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": issue_id,
        "title": {"en": f"Issue {issue_id}"},
        "generation_status": generation_status,
        "generation_version": generation_version,
    }
    if poster_url is not None:
        payload["poster_url"] = poster_url
    store.save_projection(
        issue_id=issue_id,
        status="OPEN",
        payload=payload,
        policy_version=DERIVATION_POLICY_VERSION,
    )
    saved = store.get_projection(issue_id)
    assert saved is not None
    return saved


def _nudge(*, enabled: bool = True, transport: _RecordingTransport | None = None) -> tuple[
    SenseBriefNudgeService, _RecordingTransport
]:
    transport = transport or _RecordingTransport()
    service = SenseBriefNudgeService(
        settings=SenseBriefNudgeSettings(
            enabled=enabled,
            base_url="https://aibridge.test" if enabled else None,
            s2s_token=_S2S if enabled else None,
            timeout_s=5.0,
        ),
        transport=transport,
    )
    return service, transport


def test_req57_03_eligible_pending_and_failed_not_ready() -> None:
    assert is_sweep_eligible({"generation_status": "pending"}) is True
    assert is_sweep_eligible({"generation_status": "failed"}) is True
    assert is_sweep_eligible({"generation_status": "ready", "poster_url": "https://x"}) is False
    assert is_sweep_eligible({}) is False

    store = InMemoryIssueProjectionStore()
    _save(store, issue_id="i-pending", generation_status="pending")
    _save(store, issue_id="i-failed", generation_status="failed", generation_version="v1")
    _save(
        store,
        issue_id="i-ready",
        generation_status="ready",
        poster_url="https://cdn.example/poster.png",
    )
    eligible = list_sweep_eligible_issues(store)
    ids = {item.issue_id for item in eligible}
    assert ids == {"i-pending", "i-failed"}
    assert all(item.generation_status in {"pending", "failed"} for item in eligible)


def test_req57_03_sweep_renudges_pending_and_failed() -> None:
    store = InMemoryIssueProjectionStore()
    _save(store, issue_id="i-pending", generation_status="pending")
    _save(store, issue_id="i-failed", generation_status="failed", generation_version="v1")
    nudge, transport = _nudge(enabled=True)
    result = SenseBriefSweepService(store=store, nudge_service=nudge).run_once()
    assert result.eligible_count == 2
    assert result.nudged_count == 2
    assert len(transport.calls) == 2
    issue_ids = {call["body"]["issue_id"] for call in transport.calls}
    assert issue_ids == {"i-pending", "i-failed"}
    for call in transport.calls:
        assert call["url"] == f"https://aibridge.test{ACCEPT_PATH}"
        assert call["headers"]["Authorization"] == f"Bearer {_S2S}"
        assert call["body"]["generation_version"] == INITIAL_GENERATION_VERSION


def test_req57_03_ready_not_overwritten_by_sweep() -> None:
    store = InMemoryIssueProjectionStore()
    before = _save(
        store,
        issue_id="i-ready",
        generation_status="ready",
        generation_version="v3",
        poster_url="https://cdn.example/keep.png",
    )
    _save(store, issue_id="i-pending", generation_status="pending")
    nudge, transport = _nudge(enabled=True)
    SenseBriefSweepService(store=store, nudge_service=nudge).run_once()
    after = store.get_projection("i-ready")
    assert after is not None
    assert_ready_payload_unchanged(before, after)
    nudged_ids = {call["body"]["issue_id"] for call in transport.calls}
    assert "i-ready" not in nudged_ids
    assert nudged_ids == {"i-pending"}


def test_req57_03_disabled_nudge_fail_closed_no_http() -> None:
    store = InMemoryIssueProjectionStore()
    _save(store, issue_id="i-pending", generation_status="pending")
    nudge, transport = _nudge(enabled=False)
    result = SenseBriefSweepService(store=store, nudge_service=nudge).run_once()
    assert result.eligible_count == 1
    assert result.nudged_count == 0
    assert transport.calls == []
    assert result.nudge_results[0].skip_reason == "disabled"


def test_req57_03_cron_run_once_uses_sweep_service() -> None:
    store = InMemoryIssueProjectionStore()
    _save(store, issue_id="i-failed", generation_status="failed")
    nudge, transport = _nudge(enabled=True)
    cron = SenseBriefSweepCronJob(
        sweep_service=SenseBriefSweepService(store=store, nudge_service=nudge),
        interval_s=60,
    )
    cron.run_once()
    assert len(transport.calls) == 1
    assert transport.calls[0]["body"]["issue_id"] == "i-failed"


def test_req57_03_lifespan_starts_and_stops_sweep_when_nudge_enabled(
    monkeypatch: Any,
) -> None:
    """G1: ASGI lifespan wires SenseBriefSweepCronJob when nudge enabled."""
    events: list[str] = []

    class _SweepCronSpy:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            events.append("init")

        def start(self) -> None:
            events.append("start")

        def stop(self) -> None:
            events.append("stop")

    monkeypatch.setattr(asgi_app, "SenseBriefSweepCronJob", _SweepCronSpy)
    monkeypatch.setattr(
        asgi_app, "get_api_dependencies", lambda: _sweep_lifespan_deps(nudge_enabled=True)
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        assert events == ["init", "start"]
    asgi_app._clear_api_dependencies_cache()
    assert events == ["init", "start", "stop"]


def test_req57_03_lifespan_skips_sweep_when_nudge_disabled(monkeypatch: Any) -> None:
    """G1: disabled nudge → no SenseBriefSweepCronJob start."""
    events: list[str] = []

    class _SweepCronSpy:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            events.append("init")

        def start(self) -> None:
            events.append("start")

        def stop(self) -> None:
            events.append("stop")

    monkeypatch.setattr(asgi_app, "SenseBriefSweepCronJob", _SweepCronSpy)
    monkeypatch.setattr(
        asgi_app, "get_api_dependencies", lambda: _sweep_lifespan_deps(nudge_enabled=False)
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        pass
    asgi_app._clear_api_dependencies_cache()
    assert events == []
