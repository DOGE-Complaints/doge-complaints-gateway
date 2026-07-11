"""Smoke: GPT-generated Pirita demo intake payload vs local server (TODO.md spec)."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4
from typing import Any

import httpx
import pytest

from conftest import build_intake_headers, intake_auth_token

_FIXTURE_PATH = (
    Path(__file__).resolve().parent / "fixtures" / "gpt_pirita_demo_intake.json"
)
_INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"
_I18N_LANGS = frozenset({"et", "ru", "en"})
_GPT_SIGNALS_ENUMS = {
    "severity": frozenset({"LOW", "MEDIUM", "HIGH", "CRITICAL"}),
    "impact_estimation": frozenset({"LOCAL", "DISTRICT", "CITY", "NATIONAL"}),
    "problem_status": frozenset({"ONGOING", "RESOLVED", "RECURRING", "UNKNOWN"}),
}
_LOGGER = logging.getLogger(__name__)


def _mask_headers(headers: dict[str, str]) -> dict[str, str]:
    masked = dict(headers)
    auth = masked.get("Authorization")
    if auth:
        masked["Authorization"] = "Bearer ***"
    return masked


def _load_gpt_pirita_payload() -> dict[str, Any]:
    raw = json.loads(_FIXTURE_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError(f"expected object in {_FIXTURE_PATH}")
    return raw


def assert_payload_matches_api_reference(payload: dict[str, Any]) -> None:
    """Static wire check vs API_REFERENCE.md §6.2 before HTTP."""
    if payload.get("schema_version") != _INTAKE_SCHEMA_VERSION:
        pytest.fail(
            f"schema_version must be {_INTAKE_SCHEMA_VERSION!r}, "
            f"got {payload.get('schema_version')!r}"
        )
    for key in ("submitter", "narrative"):
        if key not in payload:
            pytest.fail(f"missing required top-level key {key!r} (API_REFERENCE §6.2)")

    submitter = payload["submitter"]
    if not isinstance(submitter, dict):
        pytest.fail("submitter must be an object")
    for field in ("external_user_id", "identity_issuer"):
        if not str(submitter.get(field, "")).strip():
            pytest.fail(f"submitter.{field} must be non-empty")

    narrative = payload["narrative"]
    if not isinstance(narrative, dict):
        pytest.fail("narrative must be an object")
    for field in ("original_text", "language", "session_language", "title", "description"):
        if field not in narrative:
            pytest.fail(f"missing narrative.{field} (API_REFERENCE §6.2)")
    for lang_field in ("title", "description"):
        block = narrative[lang_field]
        if not isinstance(block, dict):
            pytest.fail(f"narrative.{lang_field} must be i18n object")
        for lang in _I18N_LANGS:
            if not str(block.get(lang, "")).strip():
                pytest.fail(f"narrative.{lang_field}.{lang} must be non-empty")

    for lang in ("language", "session_language"):
        if narrative[lang] not in _I18N_LANGS:
            pytest.fail(f"narrative.{lang} must be one of {_I18N_LANGS}")

    gpt_signals = payload.get("gpt_signals")
    if gpt_signals is not None:
        if not isinstance(gpt_signals, dict):
            pytest.fail("gpt_signals must be an object when present")
        for field, allowed in _GPT_SIGNALS_ENUMS.items():
            value = gpt_signals.get(field)
            if value is None:
                continue
            if str(value).upper() not in allowed:
                pytest.fail(
                    f"gpt_signals.{field}={value!r} not in documented enum {sorted(allowed)}"
                )


@pytest.fixture
def gpt_pirita_intake_payload() -> dict[str, Any]:
    return _load_gpt_pirita_payload()


def test_gpt_pirita_payload_static_contract_check(gpt_pirita_intake_payload: dict[str, Any]) -> None:
    """Runs offline — validates GPT wire shape against API_REFERENCE §6.2."""
    assert_payload_matches_api_reference(gpt_pirita_intake_payload)


def test_ls_gpt_pirita_demo_intake_returns_202_with_story_id(
    http_client: httpx.Client,
    local_server_url_source: str,
    gpt_pirita_intake_payload: dict[str, Any],
) -> None:
    assert_payload_matches_api_reference(gpt_pirita_intake_payload)
    token = intake_auth_token()
    endpoint = "/story-drafts"
    stash_payload = dict(gpt_pirita_intake_payload)
    stash_payload.pop("submitter", None)
    idempotency_key = (
        f"gpt-pirita-demo-smoke-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:8]}"
    )
    headers = build_intake_headers(
        idempotency_key=idempotency_key,
        bearer_token=token,
    )
    request_url = f"{str(http_client.base_url).rstrip('/')}{endpoint}"
    _LOGGER.info("pirita_smoke.url_source=%s base_url=%s", local_server_url_source, http_client.base_url)
    _LOGGER.info("pirita_smoke.start url=%s method=POST", request_url)
    _LOGGER.info("pirita_smoke.request_headers=%s", _mask_headers(headers))
    _LOGGER.info("pirita_smoke.idempotency_key=%s", idempotency_key)
    _LOGGER.info(
        "pirita_smoke.request_payload=%s",
        json.dumps(gpt_pirita_intake_payload, ensure_ascii=False, indent=2),
    )
    response = http_client.post(
        endpoint,
        json=stash_payload,
        headers=headers,
    )
    _LOGGER.info("pirita_smoke.response_status=%s", response.status_code)
    _LOGGER.info("pirita_smoke.response_headers=%s", dict(response.headers))
    _LOGGER.info("pirita_smoke.response_body=%s", response.text)
    assert response.status_code == 201, (
        "expected HTTP 201 for GPT Pirita story-drafts stash; "
        f"url={request_url}; status={response.status_code}; body={response.text}"
    )
    body = response.json()
    draft_id = body.get("data", {}).get("draft_id")
    _LOGGER.info(
        "pirita_smoke.parsed_response draft_id=%s trace_id=%s",
        draft_id,
        body.get("trace_id"),
    )
    assert draft_id and str(draft_id).strip(), f"missing data.draft_id in {body!r}"
