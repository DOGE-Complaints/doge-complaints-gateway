from __future__ import annotations

from dataclasses import dataclass
from types import SimpleNamespace
from typing import Any

from fastapi.testclient import TestClient  # pyright: ignore[reportMissingImports]

import core.api.asgi_app as asgi_app


@dataclass(frozen=True)
class _ConfigStub:
    cluster_cron_enabled: bool
    cluster_cron_interval_s: int = 1
    cluster_min_size: int = 2
    log_level: str = "INFO"
    log_format: str = "text"
    log_debug_dir: str | None = None
    db_backend: str = "in_memory"
    cluster_active_lenses: tuple[str, ...] = ("civic_domain_micro",)
    cluster_primary_lens: str = "civic_domain_micro"
    cluster_readiness_threshold: int = 60
    node_schema_id: str = "tallinn_civic"
    node_schema_version: str = "v1"


def _deps_stub(*, cron_enabled: bool, db_backend: str = "in_memory") -> Any:
    return SimpleNamespace(
        config=_ConfigStub(cluster_cron_enabled=cron_enabled, db_backend=db_backend),
        story_cluster_orchestrator=object(),
        db_ready=False,
        db_checks={"connectivity": False},
    )


def test_lifespan_does_not_start_cron_when_disabled(monkeypatch: Any) -> None:
    events: list[str] = []

    class _CronSpy:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            events.append("init")

        def start(self) -> None:
            events.append("start")

        def stop(self) -> None:
            events.append("stop")

    monkeypatch.setattr(asgi_app, "ClusterCronJob", _CronSpy)
    monkeypatch.setattr(
        asgi_app, "get_api_dependencies", lambda: _deps_stub(cron_enabled=False)
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        pass
    asgi_app._clear_api_dependencies_cache()

    assert events == []


def test_lifespan_emits_shutdown_reason_log(
    monkeypatch: Any, capsys: Any
) -> None:
    class _CronSpy:
        def __init__(self, *_args: Any, **_kwargs: Any) -> None:
            return None

        def start(self) -> None:
            return None

        def stop(self) -> None:
            return None

    monkeypatch.setattr(asgi_app, "ClusterCronJob", _CronSpy)
    monkeypatch.setattr(
        asgi_app, "get_api_dependencies", lambda: _deps_stub(cron_enabled=False)
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        pass
    asgi_app._clear_api_dependencies_cache()
    captured = capsys.readouterr()
    assert "shutdown.lifecycle" in captured.out


def test_lifespan_emits_startup_persistence_backend_log_in_memory(
    monkeypatch: Any, capsys: Any
) -> None:
    monkeypatch.setattr(
        asgi_app,
        "get_api_dependencies",
        lambda: _deps_stub(cron_enabled=False, db_backend="in_memory"),
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        pass
    asgi_app._clear_api_dependencies_cache()
    captured = capsys.readouterr()
    assert "startup.persistence_backend backend=in_memory" in captured.out


def test_lifespan_emits_startup_persistence_backend_log_supabase(
    monkeypatch: Any, capsys: Any
) -> None:
    monkeypatch.setattr(
        asgi_app,
        "get_api_dependencies",
        lambda: _deps_stub(cron_enabled=False, db_backend="supabase"),
    )
    asgi_app._clear_api_dependencies_cache()
    with TestClient(asgi_app.app):
        pass
    asgi_app._clear_api_dependencies_cache()
    captured = capsys.readouterr()
    assert "startup.persistence_backend backend=supabase" in captured.out

