"""GW-REQ11-02 — named selectable profiles: local + uus-veerenni (env refs only)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SANDBOX = Path(__file__).resolve().parent / "sandbox"
PROFILES = SANDBOX / "profiles"

# Import loader without requiring sandbox as installed package.
sys.path.insert(0, str(PROFILES))
import demo_life_sim_profiles as profiles  # noqa: E402


def test_ac01_local_profile_selectable_local_five_ports() -> None:
    ids = profiles.list_profile_ids()
    assert "local" in ids
    doc = profiles.select_profile("local")
    assert doc["profile_id"] == "local"
    services = doc["services"]
    assert services["identity"]["port_default"] == 8100
    assert services["gateway"]["port_default"] == 8000
    assert services["threads"]["port_default"] == 8001
    assert services["aibridge"]["port_default"] == 8080
    assert services["spa"]["port_default"] == 5173
    assert services["identity"]["base_url"] == "http://127.0.0.1:8100"
    assert services["gateway"]["base_url"] == "http://127.0.0.1:8000"
    assert services["gateway"]["api_token_env"] == "GATEWAY_API_TOKEN"
    assert "PORT" in doc["description"] or "port" in doc["description"].lower()


def test_ac02_uus_veerenni_profile_selectable_env_refs() -> None:
    assert "uus-veerenni" in profiles.list_profile_ids()
    doc = profiles.select_profile("uus-veerenni")
    assert doc["profile_id"] == "uus-veerenni"
    gw = doc["services"]["gateway"]
    assert gw["url_env"] == "GATEWAY_URL"
    assert gw["api_token_env"] == "GATEWAY_API_TOKEN"
    assert gw["documented_example_url"] == "https://uus-veerenni-civic-gateway.dogestonia.me"
    # No literal token value field
    assert "api_token" not in gw


def test_ac03_env_refs_only_no_secret_literals() -> None:
    for pid in profiles.list_profile_ids():
        doc = profiles.load_profile(pid)
        profiles.assert_no_secret_literals(doc)
        names = profiles.collect_env_ref_names(doc)
        assert "GATEWAY_API_TOKEN" in names
        assert "GATEWAY_USER_PASSWORD" in names
        # Env names are uppercase identifiers, not secret values
        for name in names:
            assert name.isidentifier() or name.replace("_", "").isalnum()
            assert " " not in name


def test_selection_via_env_and_default() -> None:
    by_env = profiles.select_profile(environ={"DEMO_LIFE_SIM_PROFILE": "uus-veerenni"})
    assert by_env["profile_id"] == "uus-veerenni"
    by_default = profiles.select_profile(environ={})
    assert by_default["profile_id"] == "local"
    with pytest.raises(KeyError):
        profiles.select_profile("no-such-profile")
