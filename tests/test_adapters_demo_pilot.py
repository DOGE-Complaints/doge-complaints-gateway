from __future__ import annotations

from core.adapters import (
    AdapterBundle,
    adapter_runtime_flags,
    build_adapter_bundle,
)
from core.config import load_config_from_env


def _demo_env() -> dict[str, str]:
    return {
        "APP_PROFILE": "demo",
        "API_BASE_URL": "https://demo.example/api",
    }


def _pilot_env() -> dict[str, str]:
    return {
        "APP_PROFILE": "pilot",
        "API_BASE_URL": "https://pilot.example/api",
    }


def test_build_adapter_bundle_returns_typed_bundle() -> None:
    cfg = load_config_from_env(_demo_env())
    bundle = build_adapter_bundle(cfg)
    assert isinstance(bundle, AdapterBundle)
    mid = bundle.wallet_push.push(channel="email", body="hello")
    assert mid.startswith("push-")
    sid = bundle.sign_request.request_signature(payload_digest_hex="abcd")
    assert sid.startswith("signreq-")
    receipt = bundle.tx_broadcast.broadcast(signed_tx_hex="deadbeef")
    assert receipt.status == "stub_submitted"
    assert receipt.chain_profile == "demo"


def test_pilot_profile_changes_deterministic_ids() -> None:
    demo_cfg = load_config_from_env(_demo_env())
    pilot_cfg = load_config_from_env(_pilot_env())
    d = build_adapter_bundle(demo_cfg).tx_broadcast.broadcast(signed_tx_hex="00")
    p = build_adapter_bundle(pilot_cfg).tx_broadcast.broadcast(signed_tx_hex="00")
    assert d.tx_id != p.tx_id
    assert d.chain_profile == "demo"
    assert p.chain_profile == "pilot"


def test_adapter_runtime_flags_reflects_config() -> None:
    cfg = load_config_from_env(_demo_env())
    flags = adapter_runtime_flags(cfg)
    assert flags["deployment_profile"] == "demo"
    assert flags["wallet_adapter"] is False
