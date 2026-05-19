"""Shared fixtures for local real-HTTP smoke tests (REQ-41 GAP-41-01 / GAP-41-06)."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import httpx
import pytest

_CANVAS_PATH = Path(__file__).resolve().parent.parent / "sandbox" / "dogestonia_simulation_canvas_v0_1.json"
_SCENARIO_GROUPS = ("infrastructure", "environment", "digital", "conflict")


def load_simulation_canvas() -> list[dict[str, Any]]:
    raw = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise TypeError(f"expected canvas list in {_CANVAS_PATH}")
    return raw


def first_scenario_for_group(group: str) -> dict[str, Any]:
    for scenario in load_simulation_canvas():
        if scenario.get("scenario_group") == group:
            return scenario
    raise LookupError(f"no scenario for group {group!r} in {_CANVAS_PATH}")


@pytest.fixture(scope="module")
def local_server_url() -> str:
    configured = os.environ.get("LOCAL_SERVER_URL", "").strip()
    if not configured:
        pytest.skip("LOCAL_SERVER_URL not set")
    base = configured.rstrip("/")
    try:
        health = httpx.get(f"{base}/health", timeout=3.0)
    except httpx.HTTPError as exc:
        pytest.skip(f"server not reachable: {exc}")
    if health.status_code != 200:
        pytest.skip(f"server not reachable: /health returned {health.status_code}")
    return base


@pytest.fixture(scope="module")
def http_client(local_server_url: str) -> Iterator[httpx.Client]:
    with httpx.Client(base_url=local_server_url, timeout=30.0) as client:
        yield client
