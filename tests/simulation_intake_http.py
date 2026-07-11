"""Live HTTP stash+submit helpers for simulation runner (no pytest deps)."""

from __future__ import annotations

import json
from copy import deepcopy
from typing import Any
from urllib import error, request

_SUPABASE_AUTH_ENV = (
    "GATEWAY_USER_EMAIL",
    "GATEWAY_USER_PASSWORD",
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
)

_cached_user_bearer_token: str | None = None


def intake_payload_to_stash(payload: dict[str, Any]) -> dict[str, Any]:
    stash = deepcopy(payload)
    stash.pop("submitter", None)
    return stash


def _required_env(name: str) -> str:
    import os

    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required env variable: {name}")
    return value


def fetch_supabase_access_token(
    *,
    email: str,
    password: str,
    supabase_url: str,
    anon_key: str,
) -> str:
    """Exchange email+password for Supabase access_token (in-memory only; never logged)."""
    base = supabase_url.rstrip("/")
    url = f"{base}/auth/v1/token?grant_type=password"
    body = json.dumps({"email": email, "password": password}).encode("utf-8")
    headers = {
        "apikey": anon_key,
        "Content-Type": "application/json",
    }
    req = request.Request(url=url, data=body, method="POST", headers=headers)
    try:
        with request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        error_text = exc.read().decode("utf-8") if exc.fp else str(exc)
        detail = error_text.strip() or "invalid credentials"
        msg = (
            f"Supabase login rejected (HTTP {exc.code}): check GATEWAY_USER_EMAIL "
            f"and GATEWAY_USER_PASSWORD — {detail}"
        )
        raise RuntimeError(msg) from exc
    except error.URLError as exc:
        msg = f"Supabase login failed: cannot reach SUPABASE_URL ({base}): {exc.reason}"
        raise RuntimeError(msg) from exc

    if not isinstance(payload, dict):
        raise RuntimeError(
            "Supabase login response invalid — check SUPABASE_URL and SUPABASE_ANON_KEY"
        )
    access_token = payload.get("access_token")
    if not isinstance(access_token, str) or not access_token.strip():
        raise RuntimeError(
            "Supabase login response missing access_token — "
            "check SUPABASE_URL and SUPABASE_ANON_KEY"
        )
    return access_token.strip()


def resolve_user_bearer_token() -> str:
    """Resolve user Bearer via Supabase password grant; cached in-memory for one runner run."""
    global _cached_user_bearer_token
    if _cached_user_bearer_token is not None:
        return _cached_user_bearer_token

    import os

    missing = [name for name in _SUPABASE_AUTH_ENV if not os.getenv(name, "").strip()]
    if missing:
        raise RuntimeError(
            "Missing required env for Supabase user auth: "
            + ", ".join(missing)
            + " (set in .env.test — see .env.test.example)"
        )

    _cached_user_bearer_token = fetch_supabase_access_token(
        email=_required_env("GATEWAY_USER_EMAIL"),
        password=_required_env("GATEWAY_USER_PASSWORD"),
        supabase_url=_required_env("SUPABASE_URL"),
        anon_key=_required_env("SUPABASE_ANON_KEY"),
    )
    return _cached_user_bearer_token


def format_submit_failure(status: int, response_text: str) -> str:
    """Map submit HTTP errors to operator-facing messages (fail-closed)."""
    if status == 403:
        return (
            "демо-пользователь не phone_verified — верифицируй телефон один раз в SPA, "
            "затем повтори"
        )
    if status == 401:
        return "Supabase-токен невалиден/просрочен"
    detail = response_text.strip()
    if len(detail) > 200:
        detail = detail[:200] + "..."
    return detail or f"submit failed with HTTP {status}"


def _post_bytes(
    url: str,
    *,
    bearer_token: str,
    body: bytes,
    method: str = "POST",
) -> tuple[int, str]:
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    req = request.Request(url=url, data=body, method=method, headers=headers)
    try:
        with request.urlopen(req, timeout=30) as resp:
            return int(resp.status), resp.read().decode("utf-8")
    except error.HTTPError as exc:
        error_text = exc.read().decode("utf-8") if exc.fp else str(exc)
        return int(exc.code), error_text


def post_json_with_bearer(
    url: str,
    payload: dict[str, Any],
    bearer_token: str,
) -> tuple[int, str]:
    return _post_bytes(
        url,
        bearer_token=bearer_token,
        body=json.dumps(payload).encode("utf-8"),
    )


def post_submit_with_bearer(url: str, bearer_token: str) -> tuple[int, str]:
    return _post_bytes(url, bearer_token=bearer_token, body=b"{}")


def extract_draft_id(body: Any) -> str:
    if not isinstance(body, dict):
        return "n/a"
    data = body.get("data")
    if isinstance(data, dict):
        draft_id = data.get("draft_id")
        if isinstance(draft_id, str) and draft_id.strip():
            return draft_id.strip()
    draft_id = body.get("draft_id")
    if isinstance(draft_id, str) and draft_id.strip():
        return draft_id.strip()
    return "n/a"


def extract_story_id(body: Any) -> str:
    if not isinstance(body, dict):
        return "n/a"
    data = body.get("data")
    if isinstance(data, dict):
        story_id = data.get("story_id")
        if isinstance(story_id, str) and story_id.strip():
            return story_id.strip()
    story_id = body.get("story_id")
    if isinstance(story_id, str) and story_id.strip():
        return story_id.strip()
    return "n/a"


def post_stash_and_submit_http(
    *,
    gateway_url: str,
    service_token: str,
    user_token: str,
    payload: dict[str, Any],
) -> tuple[int, str, str, str]:
    """Returns (final_status, response_text, draft_id, story_id). final_status 202 = success."""
    stash_status, stash_text = post_json_with_bearer(
        f"{gateway_url.rstrip('/')}/story-drafts",
        intake_payload_to_stash(payload),
        service_token,
    )
    if stash_status != 201:
        return stash_status, stash_text, "n/a", "n/a"
    try:
        stash_body = json.loads(stash_text)
    except json.JSONDecodeError:
        stash_body = {}
    draft_id = extract_draft_id(stash_body)
    submit_status, submit_text = post_submit_with_bearer(
        f"{gateway_url.rstrip('/')}/story-drafts/{draft_id}/submit",
        user_token,
    )
    story_id = "n/a"
    if submit_status == 202:
        try:
            submit_body = json.loads(submit_text)
        except json.JSONDecodeError:
            submit_body = {}
        story_id = extract_story_id(submit_body)
    elif submit_status in (401, 403):
        submit_text = format_submit_failure(submit_status, submit_text)
    return submit_status, submit_text, draft_id, story_id
