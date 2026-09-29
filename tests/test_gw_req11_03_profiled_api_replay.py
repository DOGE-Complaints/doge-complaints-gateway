"""GW-REQ11-03 — profiled API replay + pool M=20 map (unit/contract)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import mock

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
PROFILES = SANDBOX / "profiles"
sys.path.insert(0, str(PROFILES))
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_replay_lib as life_sim  # noqa: E402
import demo_life_sim_profiles as profiles  # noqa: E402
import simulation_intake_http as intake_http  # noqa: E402


def test_ac02_fixture_scale_from_req11_01() -> None:
    life_sim.assert_fixture_scale()
    users = life_sim.load_life_sim_users()
    stories = life_sim.load_life_sim_stories()
    assert len(users) == 200
    assert len(stories) == 1661
    profile = profiles.select_profile("local")
    assert profile["profile_id"] == "local"


def test_ac03_pool_m20_manifest_env_refs_only() -> None:
    pool = life_sim.load_pool_manifest()
    assert pool["pool_size"] == 20
    assert len(pool["slots"]) == 20
    raw = json.dumps(pool)
    assert "sk-" not in raw
    assert "eyJ" not in raw
    assert "Bearer " not in raw
    for slot in pool["slots"]:
        assert slot["email_env"].startswith("LIFE_SIM_POOL_")
        assert slot["password_env"].startswith("LIFE_SIM_POOL_")
        assert slot["email_env"].endswith("_EMAIL")
        assert slot["password_env"].endswith("_PASSWORD")


def test_ac03_map_200_to_pool_20() -> None:
    fmap = life_sim.load_fixture_to_pool_map()
    assert fmap["pool_size"] == 20
    assert fmap["fixture_user_count"] == 200
    assert len(fmap["entries"]) == 200
    slots = {e["pool_slot"] for e in fmap["entries"]}
    assert slots == set(range(20))
    assert life_sim.map_fixture_user_to_pool_slot("life-sim-user-0001") == 0
    assert life_sim.map_fixture_user_to_pool_slot("life-sim-user-0020") == 19
    assert life_sim.map_fixture_user_to_pool_slot("life-sim-user-0021") == 0
    assert life_sim.map_fixture_user_to_pool_slot("life-sim-user-0200") == 19
    # each slot gets exactly 10 fixture users
    from collections import Counter

    counts = Counter(e["pool_slot"] for e in fmap["entries"])
    assert all(v == 10 for v in counts.values())


def test_payload_conversion_contract() -> None:
    story = life_sim.load_life_sim_stories()[0]
    payload = life_sim.life_sim_story_to_intake_payload(
        story,
        intake_schema_version="test-schema",
        schema_binding={"node_schema_id": "tallinn_civic", "node_schema_version": "v1"},
        location_query="Tallinn",
    )
    assert payload["schema_version"] == "test-schema"
    assert payload["origin"]["source"] == "simulation"
    assert payload["origin"]["conversation_id"] == story["fixture_story_id"]
    assert payload["narrative"]["original_text"]
    assert payload["narrative"]["location_query"] == "Tallinn"
    stash = intake_http.intake_payload_to_stash(payload)
    assert "submitter" not in stash


def test_resolve_pool_slot_bearer_uses_env_and_password_grant() -> None:
    intake_http.clear_bearer_token_caches()
    environ = {
        "LIFE_SIM_POOL_03_EMAIL": "pool03@example.com",
        "LIFE_SIM_POOL_03_PASSWORD": "secret-not-logged",
        "SUPABASE_URL": "https://example.supabase.co",
        "SUPABASE_ANON_KEY": "anon-key",
    }
    with mock.patch.dict("os.environ", environ, clear=False):
        with mock.patch.object(
            intake_http,
            "fetch_supabase_access_token",
            return_value="token-slot-03",
        ) as fetch:
            token = intake_http.resolve_pool_slot_bearer_token(3)
            assert token == "token-slot-03"
            fetch.assert_called_once_with(
                email="pool03@example.com",
                password="secret-not-logged",
                supabase_url="https://example.supabase.co",
                anon_key="anon-key",
            )
            # cached
            assert intake_http.resolve_pool_slot_bearer_token(3) == "token-slot-03"
            assert fetch.call_count == 1
    intake_http.clear_bearer_token_caches()


def test_pool_slot_missing_env_fail_closed() -> None:
    intake_http.clear_bearer_token_caches()
    with mock.patch.dict("os.environ", {}, clear=True):
        with pytest.raises(RuntimeError, match="LIFE_SIM_POOL_00_EMAIL"):
            intake_http.resolve_pool_slot_bearer_token(0)


def test_count_pool_slots_with_credentials() -> None:
    env = {f"LIFE_SIM_POOL_{i:02d}_EMAIL": f"u{i}@x.test" for i in range(5)}
    env.update({f"LIFE_SIM_POOL_{i:02d}_PASSWORD": f"p{i}" for i in range(5)})
    assert life_sim.count_pool_slots_with_credentials(env) == 5
    assert life_sim.count_pool_slots_with_credentials({}) == 0


def test_ac04_no_spa_in_pass_path_code() -> None:
    """Pass path is API+JSON helpers; runner life-sim mode does not open SPA."""
    runner = (TESTS / "simulation_runner.py").read_text(encoding="utf-8")
    assert "--life-sim" in runner
    assert "resolve_pool_slot_bearer_token" in runner
    assert "demo/auth-page" not in runner
    assert "SPA" in runner  # documents no SPA login
    http = (TESTS / "simulation_intake_http.py").read_text(encoding="utf-8")
    assert "resolve_pool_slot_bearer_token" in http
    assert "/auth/v1/token?grant_type=password" in http
