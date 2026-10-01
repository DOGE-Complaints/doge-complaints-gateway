"""Offline unit tests for STORY-GW-REQ11-08 pack-wave config + wave-state."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_provision_config as cfg  # noqa: E402
import life_sim_provision_lib as lib  # noqa: E402
from life_sim_wave_store import WaveStore, default_wave_state_path  # noqa: E402


def test_email_domain_hard_dogestonia_me() -> None:
    assert cfg.EMAIL_DOMAIN == "dogestonia.me"
    assert lib.EMAIL_DOMAIN == "dogestonia.me"
    assert lib.derive_email("life-sim-user-0001").endswith("@dogestonia.me")
    cfg.assert_email_domain("dogestonia.me")
    with pytest.raises(cfg.ProvisionConfigError):
        cfg.assert_email_domain("dogestonia.com")


def test_sms_provider_fail_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SMS_PROVIDER", "telnyx")
    with pytest.raises(cfg.ProvisionConfigError, match="SMS_PROVIDER"):
        cfg.require_sms_provider_file()
    monkeypatch.setenv("SMS_PROVIDER", "file")
    assert cfg.require_sms_provider_file() == "file"


def test_outbox_fail_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    missing = tmp_path / "no-outbox"
    monkeypatch.setenv("LIFE_SIM_FILE_SMS_OUTBOX_DIR", str(missing))
    with pytest.raises(cfg.ProvisionConfigError, match="outbox"):
        cfg.require_readable_outbox()
    outbox = tmp_path / "outbox"
    outbox.mkdir()
    monkeypatch.setenv("LIFE_SIM_FILE_SMS_OUTBOX_DIR", str(outbox))
    assert cfg.require_readable_outbox() == outbox.resolve()


def test_wave_checkpoint_and_resume_skips_verified(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    # Fixture users.json present but must not be written by wave store.
    users_path = pack / "users.json"
    users_path.write_text(
        json.dumps([{"fixture_user_id": "life-sim-user-0001"}]),
        encoding="utf-8",
    )
    before = users_path.read_text(encoding="utf-8")
    before_mtime = users_path.stat().st_mtime

    ids = ["life-sim-user-0001", "life-sim-user-0002", "life-sim-user-0003"]
    wave = WaveStore.load_or_create(pack, "wave-test", fixture_user_ids=ids)
    assert wave.path == default_wave_state_path(pack, "wave-test")
    assert wave.path.is_file()
    assert wave.get_status("life-sim-user-0001") == "pending"

    wave.set_status("life-sim-user-0001", "verified")
    wave.set_status("life-sim-user-0002", "failed", error="boom")
    wave.set_status("life-sim-user-0003", "created")

    reloaded = WaveStore.load_or_create(pack, "wave-test", fixture_user_ids=ids)
    assert reloaded.is_verified("life-sim-user-0001")
    assert reloaded.users_needing_work(ids) == [
        "life-sim-user-0002",
        "life-sim-user-0003",
    ]
    assert users_path.read_text(encoding="utf-8") == before
    assert users_path.stat().st_mtime == before_mtime


def test_wave_never_uses_users_json_path(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "users.json").write_text("[]", encoding="utf-8")
    wave = WaveStore.load_or_create(pack, "w1", fixture_user_ids=["life-sim-user-0001"])
    assert "users.json" not in str(wave.path)
    assert wave.path.name == "state.json"
    assert "waves" in wave.path.parts


def test_no_invent_last_otp_http_backdoor() -> None:
    """Source documents refuse invent last-otp; no callable path to invent endpoint."""
    for name in (
        "life_sim_provision_pack_wave.py",
        "life_sim_provision_config.py",
    ):
        blob = (SANDBOX / name).read_text(encoding="utf-8")
        assert "invent" in blob.lower() and "last-otp" in blob
        assert 'f"{identity_url}/dev/last-otp"' not in blob
        assert '"/dev/last-otp"' not in blob
        assert "'/dev/last-otp'" not in blob
