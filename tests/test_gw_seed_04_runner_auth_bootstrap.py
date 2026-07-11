"""GW-SEED-04: runner auth bootstrap (Supabase password grant)."""

from __future__ import annotations

import io
import json
from unittest.mock import MagicMock, patch
from urllib import error

import pytest

import simulation_intake_http as intake_http
from simulation_intake_http import (
    fetch_supabase_access_token,
    format_submit_failure,
    post_stash_and_submit_http,
    resolve_user_bearer_token,
)


@pytest.fixture(autouse=True)
def _reset_cached_user_token() -> None:
    intake_http._cached_user_bearer_token = None


def _supabase_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GATEWAY_USER_EMAIL", "demo@example.com")
    monkeypatch.setenv("GATEWAY_USER_PASSWORD", "secret")
    monkeypatch.setenv("SUPABASE_URL", "https://proj.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon-key")


def test_fetch_supabase_access_token_success() -> None:
    body = json.dumps({"access_token": "jwt-token", "token_type": "bearer"}).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.__enter__.return_value = mock_resp
    mock_resp.read.return_value = body

    with patch("simulation_intake_http.request.urlopen", return_value=mock_resp) as urlopen:
        token = fetch_supabase_access_token(
            email="demo@example.com",
            password="secret",
            supabase_url="https://proj.supabase.co",
            anon_key="anon-key",
        )

    assert token == "jwt-token"
    req = urlopen.call_args[0][0]
    assert req.full_url.endswith("/auth/v1/token?grant_type=password")
    assert req.headers["Apikey"] == "anon-key"


def test_fetch_supabase_access_token_bad_creds() -> None:
    err = error.HTTPError(
        url="https://proj.supabase.co/auth/v1/token?grant_type=password",
        code=400,
        msg="Bad Request",
        hdrs=None,
        fp=io.BytesIO(b'{"error":"invalid_grant"}'),
    )
    with patch("simulation_intake_http.request.urlopen", side_effect=err):
        with pytest.raises(RuntimeError, match="Supabase login rejected"):
            fetch_supabase_access_token(
                email="bad@example.com",
                password="wrong",
                supabase_url="https://proj.supabase.co",
                anon_key="anon-key",
            )


def test_resolve_user_bearer_token_missing_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in intake_http._SUPABASE_AUTH_ENV:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(RuntimeError, match="Missing required env for Supabase user auth"):
        resolve_user_bearer_token()


def test_resolve_user_bearer_token_success(monkeypatch: pytest.MonkeyPatch) -> None:
    _supabase_env(monkeypatch)
    with patch(
        "simulation_intake_http.fetch_supabase_access_token",
        return_value="cached-jwt",
    ) as fetch:
        assert resolve_user_bearer_token() == "cached-jwt"
        assert resolve_user_bearer_token() == "cached-jwt"
        fetch.assert_called_once()


def test_format_submit_failure_messages() -> None:
    assert "phone_verified" in format_submit_failure(403, '{"code":"VERIFICATION_REQUIRED"}')
    assert format_submit_failure(401, "") == "Supabase-токен невалиден/просрочен"


def test_post_stash_and_submit_http_maps_submit_403(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_post_json(url: str, payload: dict, bearer_token: str) -> tuple[int, str]:
        return 201, json.dumps({"data": {"draft_id": "draft-1"}})

    def fake_submit(url: str, bearer_token: str) -> tuple[int, str]:
        return 403, '{"code":"VERIFICATION_REQUIRED"}'

    monkeypatch.setattr(intake_http, "post_json_with_bearer", fake_post_json)
    monkeypatch.setattr(intake_http, "post_submit_with_bearer", fake_submit)

    status, text, draft_id, story_id = post_stash_and_submit_http(
        gateway_url="https://gw.example",
        service_token="svc",
        user_token="user-jwt",
        payload={"schema_version": "1"},
    )
    assert status == 403
    assert "phone_verified" in text
    assert draft_id == "draft-1"
    assert story_id == "n/a"


def test_post_stash_and_submit_http_maps_submit_401(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        intake_http,
        "post_json_with_bearer",
        lambda *args, **kwargs: (201, json.dumps({"data": {"draft_id": "d2"}})),
    )
    monkeypatch.setattr(
        intake_http,
        "post_submit_with_bearer",
        lambda *args, **kwargs: (401, "Unauthorized"),
    )

    status, text, _, _ = post_stash_and_submit_http(
        gateway_url="https://gw.example",
        service_token="svc",
        user_token="user-jwt",
        payload={"schema_version": "1"},
    )
    assert status == 401
    assert text == "Supabase-токен невалиден/просрочен"
