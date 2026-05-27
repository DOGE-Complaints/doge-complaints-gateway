"""REQ-41 GAP-41-06: async httpx read against local server (AC-01..AC-03)."""

from __future__ import annotations

import asyncio

import httpx
import pytest

from conftest import build_intake_headers, load_simulation_canvas
from simulation_runner import _scenario_to_payload


@pytest.fixture(scope="module")
def seeded_issue_list_base(http_client: httpx.Client, local_server_url: str) -> str:
    """Pre-seed five infrastructure scenarios via sync client (REQ-41 §3 GAP-41-06)."""
    infra = [s for s in load_simulation_canvas() if s.get("scenario_group") == "infrastructure"][:5]
    assert len(infra) >= 1, "canvas must contain infrastructure scenarios"
    for idx, scenario in enumerate(infra):
        payload = _scenario_to_payload(scenario)
        response = http_client.post(
            "/intake/stories",
            json=payload,
            headers=build_intake_headers(idempotency_key=f"async-seed-{idx}"),
        )
        assert response.status_code == 202, response.text
    return local_server_url


@pytest.mark.asyncio
async def test_ac01_async_get_tallinn_issues_returns_json(
    seeded_issue_list_base: str,
) -> None:
    async with httpx.AsyncClient(base_url=seeded_issue_list_base, timeout=30.0) as client:
        response = await client.get("/tallinn/issues")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "data" in body


@pytest.mark.asyncio
async def test_ac02_async_get_published_filter_returns_200(
    seeded_issue_list_base: str,
) -> None:
    async with httpx.AsyncClient(base_url=seeded_issue_list_base, timeout=30.0) as client:
        response = await client.get("/tallinn/issues", params={"status": "PUBLISHED"})
    assert response.status_code == 200
    issues = response.json()["data"]["issues"]
    assert isinstance(issues, list)


@pytest.mark.asyncio
async def test_ac03_parallel_async_gets_return_identical_bodies(
    seeded_issue_list_base: str,
) -> None:
    async with httpx.AsyncClient(base_url=seeded_issue_list_base, timeout=30.0) as client:
        responses = await asyncio.gather(
            client.get("/tallinn/issues"),
            client.get("/tallinn/issues"),
            client.get("/tallinn/issues"),
        )
    assert all(r.status_code == 200 for r in responses)
    issue_payloads = [r.json()["data"] for r in responses]
    assert issue_payloads[0] == issue_payloads[1] == issue_payloads[2]
