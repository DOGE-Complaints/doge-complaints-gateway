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


def _deps_stub(*, cron_enabled: bool) -> Any:
    return SimpleNamespace(
        config=_ConfigStub(cluster_cron_enabled=cron_enabled),
        story_cluster_orchestrator=object(),
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

