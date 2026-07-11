"""REQ-41 GAP-41-01: local uvicorn smoke via real HTTP (LS-01..LS-06)."""

from __future__ import annotations

import copy
from typing import Any

import httpx
import pytest

from conftest import (
    SCENARIO_GROUPS,
    build_intake_headers,
    first_scenario_for_group,
    post_intake_via_story_drafts_http,
)
from simulation_runner import _scenario_to_payload


def _assert_error_envelope(body: dict[str, Any]) -> None:
    assert "error" in body or "detail" in body


def test_ls01_health_returns_status(http_client: httpx.Client) -> None:
    response = http_client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert "status" in str(payload)


def test_ls02_intake_infrastructure_scenario_returns_story_id(http_client: httpx.Client) -> None:
    scenario = first_scenario_for_group("infrastructure")
    payload = _scenario_to_payload(scenario)
    response = post_intake_via_story_drafts_http(
        http_client,
        json=payload,
        headers=build_intake_headers(idempotency_key="ls02-infra"),
    )
    assert response.status_code == 202
    body = response.json()
    assert body["data"]["story_id"]


def test_ls03_intake_all_four_canvas_groups_accepted(http_client: httpx.Client) -> None:
    for idx, group in enumerate(SCENARIO_GROUPS):
        scenario = first_scenario_for_group(group)
        payload = _scenario_to_payload(scenario)
        response = post_intake_via_story_drafts_http(
            http_client,
            json=payload,
            headers=build_intake_headers(idempotency_key=f"ls03-{group}-{idx}"),
        )
        assert response.status_code == 202, f"group={group} body={response.text}"


def test_ls04_get_tallinn_issues_json(http_client: httpx.Client) -> None:
    response = http_client.get("/tallinn/issues")
    assert response.status_code == 200
    assert response.headers.get("content-type", "").startswith("application/json")
    assert "issues" in response.json()["data"]


def test_ls05_invalid_payload_returns_client_error_envelope(http_client: httpx.Client) -> None:
    scenario = first_scenario_for_group("infrastructure")
    payload = _scenario_to_payload(scenario)
    invalid = copy.deepcopy(payload)
    invalid["narrative"]["original_text"] = ""
    response = post_intake_via_story_drafts_http(
        http_client,
        json=invalid,
        headers=build_intake_headers(idempotency_key="ls05-invalid"),
    )
    assert response.status_code in (400, 422)
    _assert_error_envelope(response.json())


def test_ls06_intake_response_has_trace_correlation(http_client: httpx.Client) -> None:
    scenario = first_scenario_for_group("infrastructure")
    payload = _scenario_to_payload(scenario)
    trace_id = "ls06-trace-smoke"
    response = post_intake_via_story_drafts_http(
        http_client,
        json=payload,
        headers=build_intake_headers(
            idempotency_key="ls06-trace", trace_id=trace_id
        ),
    )
    assert response.status_code == 202
    request_id = response.headers.get("x-request-id") or response.headers.get("X-Request-Id")
    body = response.json()
    if request_id:
        assert request_id.strip()
    else:
        assert body.get("trace_id") == trace_id


@pytest.mark.parametrize("path", ["/health", "/story-drafts"])
def test_ls_p1_server_header_uvicorn_when_present(
    http_client: httpx.Client, path: str
) -> None:
    if path == "/health":
        response = http_client.get(path)
    else:
        from conftest import intake_auth_token, post_story_draft_stash_http

        scenario = first_scenario_for_group("infrastructure")
        response = post_story_draft_stash_http(
            http_client,
            json=_scenario_to_payload(scenario),
            headers=build_intake_headers(
                idempotency_key=f"ls-p1-{path.strip('/')}",
                bearer_token=intake_auth_token(),
            ),
        )
    server = response.headers.get("server", "")
    if server:
        assert "uvicorn" in server.lower()
