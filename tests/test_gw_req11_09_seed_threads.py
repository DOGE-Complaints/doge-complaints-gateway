"""Offline unit tests for STORY-GW-REQ11-09 threads seed helpers."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_seed_threads_lib as seed_lib  # noqa: E402


def test_empty_issues_fail_closed() -> None:
    rows = seed_lib.parse_node_issues_payload({"data": {"issues": []}})
    handoffs = seed_lib.handoffs_from_issue_rows(rows)
    with pytest.raises(RuntimeError, match="fail-closed"):
        seed_lib.require_nonempty_handoffs(handoffs)


def test_handoff_parse_issue_id_and_density() -> None:
    payload = {
        "data": {
            "issues": [
                {"id": "iss-a", "story_count": 8},
                {"issue_id": "iss-b", "story_ids": ["s1", "s2", "s3"]},
                {"id": "iss-c", "density": 1},
                {"title": "no-id"},  # skipped
            ]
        }
    }
    rows = seed_lib.parse_node_issues_payload(payload)
    handoffs = seed_lib.require_nonempty_handoffs(
        seed_lib.handoffs_from_issue_rows(rows)
    )
    assert [h.issue_id for h in handoffs] == ["iss-a", "iss-b", "iss-c"]
    assert handoffs[0].density == 8
    assert handoffs[1].density == 3
    assert handoffs[2].density == 1


def test_density_none_when_absent() -> None:
    rows = [{"id": "iss-x", "status": "PUBLISHED"}]
    handoffs = seed_lib.handoffs_from_issue_rows(rows)
    assert len(handoffs) == 1
    assert handoffs[0].density is None


def test_refuse_service_token_as_actor(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SERVICE_API_TOKEN", "svc-secret-token")
    with pytest.raises(RuntimeError, match="SERVICE_API_TOKEN"):
        seed_lib.refuse_service_token_as_actor("svc-secret-token")
    seed_lib.refuse_service_token_as_actor("user-bearer-ok")


def test_actors_from_bearer_map_refuse_service() -> None:
    environ = {"SERVICE_API_TOKEN": "svc-tok"}
    with pytest.raises(RuntimeError, match="SERVICE_API_TOKEN"):
        seed_lib.actors_from_bearer_map(
            {"life-sim-user-0001": "svc-tok"},
            environ=environ,
        )
    actors = seed_lib.actors_from_bearer_map(
        {"life-sim-user-0001": "user-tok"},
        environ=environ,
    )
    assert len(actors) == 1
    assert actors[0].bearer_token == "user-tok"


def test_load_actor_fixture_ids_hygiene() -> None:
    index = {
        "life-sim-user-0002": {"email": "b@x.me", "password": "pw2"},
        "life-sim-user-0001": {"email": "a@x.me", "password": "pw1"},
        "life-sim-user-0003": {"email": "", "password": "pw3"},
    }
    ids = seed_lib.load_actor_fixture_ids(index, limit_actors=1)
    assert ids == ["life-sim-user-0001"]


def test_cli_imports_seed_representative_issues() -> None:
    blob = (SANDBOX / "life_sim_seed_threads.py").read_text(encoding="utf-8")
    assert "seed_representative_issues" in blob
    assert "SERVICE_API_TOKEN" in blob
    assert "force-cluster" in blob
    closed = seed_lib.import_closed_http_seed()
    assert hasattr(closed, "seed_representative_issues")


def test_make_target_present() -> None:
    makefile = (TESTS.parent / "Makefile").read_text(encoding="utf-8")
    assert "life-sim-seed-threads:" in makefile
    assert "life_sim_seed_threads.py" in makefile


def test_cli_documents_no_pack_mutate() -> None:
    for name in ("life_sim_seed_threads.py", "life_sim_seed_threads_lib.py"):
        blob = (SANDBOX / name).read_text(encoding="utf-8")
        assert "never mutate" in blob.lower() or "Never mutates" in blob or "must not open pack JSON for write" in blob
        assert "users.json" in blob or "pack JSON" in blob
