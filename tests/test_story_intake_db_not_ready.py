from __future__ import annotations

from dataclasses import replace

from core.api.dependencies import build_api_dependencies
from core.api.handlers import handle_story_intake
from tests.intake_v2_fixtures import valid_v2_intake_payload


def test_intake_returns_503_when_supabase_db_not_ready() -> None:
    deps = build_api_dependencies()
    degraded = replace(
        deps,
        db_backend="supabase",
        db_ready=False,
        db_checks={
            "connectivity": True,
            "schema": True,
            "columns": True,
            "columns_geo_admin": False,
            "columns_v2": True,
            "policy_probe": True,
        },
    )
    body, status = handle_story_intake(
        degraded,
        payload=valid_v2_intake_payload(),
        idempotency_key="db-not-ready-test",
    )
    assert status == 503
    assert body["error"]["code"] == "SERVICE_UNAVAILABLE"
    assert body["error"]["details"]["db"]["checks"]["columns_geo_admin"] is False
