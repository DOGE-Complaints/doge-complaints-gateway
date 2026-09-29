"""Offline unit tests for STORY-GW-REQ11-05 provision helpers + 1:1 wire."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

from simulation_intake_http import clear_bearer_token_caches, resolve_fixture_user_bearer_token

import life_sim_provision_lib as provision  # noqa: E402
import life_sim_replay_lib as life_sim  # noqa: E402



def test_derive_email_and_phone_deterministic() -> None:
    fid = "life-sim-user-0001"
    assert provision.derive_email(fid) == "life.sim.user.0001@dogestonia.com"
    assert provision.derive_phone_e164(fid) == "+37251000001"
    assert provision.derive_phone_e164("life-sim-user-0200") == "+37251000200"
    # uniqueness across 200
    phones = {provision.derive_phone_e164(f"life-sim-user-{i:04d}") for i in range(1, 201)}
    assert len(phones) == 200


def test_generate_password_csprng_strength() -> None:
    pw = provision.generate_password()
    assert len(pw) >= 24
    assert provision.password_is_strong(pw)
    assert not provision.password_is_strong("short")
    # two draws unlikely identical
    assert provision.generate_password() != provision.generate_password()


def test_secrets_path_hygiene(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Point SECRETS_DIR at tmp via monkeypatch of module constant
    secrets_dir = tmp_path / ".secrets"
    secrets_dir.mkdir()
    monkeypatch.setattr(provision, "SECRETS_DIR", secrets_dir)
    path = provision.secrets_path_for_generation("20260929T120000Z", secrets_dir=secrets_dir)
    provision.assert_secrets_path_hygiene(path)
    with pytest.raises(ValueError):
        provision.assert_secrets_path_hygiene(tmp_path / "creds.json")
    with pytest.raises(ValueError):
        provision.secrets_path_for_generation("../evil", secrets_dir=secrets_dir)


def test_extract_otp_from_outbox_text() -> None:
    text = (
        "2026-06-12T12:00:00Z\tYour Dogestonia verification code is 111111.\n"
        "2026-06-12T12:01:00Z\tYour Dogestonia verification code is 654321.\n"
    )
    assert provision.extract_otp_from_outbox_text(text) == "654321"
    assert provision.extract_otp_from_outbox_text("no code here") is None


def test_read_latest_otp_from_outbox(tmp_path: Path) -> None:
    phone = "+37251000001"
    log = tmp_path / "+37251000001.log"
    log.write_text(
        "2026-09-29T18:00:00Z\tYour Dogestonia verification code is 424242.\n",
        encoding="utf-8",
    )
    assert provision.read_latest_otp_from_outbox(tmp_path, phone) == "424242"


def test_write_and_load_creds_roundtrip(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    secrets_dir = tmp_path / ".secrets"
    secrets_dir.mkdir()
    monkeypatch.setattr(provision, "SECRETS_DIR", secrets_dir)
    path = provision.secrets_path_for_generation("gen1", secrets_dir=secrets_dir)
    doc = provision.build_creds_document(
        generation_id="gen1",
        entries=[
            {
                "fixture_user_id": "life-sim-user-0001",
                "email": "life.sim.user.0001@dogestonia.com",
                "password": "x" * 24 + "A1!",
                "phone_e164": "+37251000001",
                "generation_id": "gen1",
                "created_at_utc": "2026-09-29T18:00:00Z",
            }
        ],
        created_at_utc="2026-09-29T18:00:00Z",
    )
    provision.write_creds_document(path, doc)
    loaded = provision.load_users_creds(path)
    assert loaded["generation_id"] == "gen1"
    idx = provision.index_creds_by_fixture_user_id(loaded)
    assert "life-sim-user-0001" in idx


def test_resolve_fixture_user_bearer_uses_password_grant(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_bearer_token_caches()
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_ANON_KEY", "anon-key")
    with patch(
        "simulation_intake_http.fetch_supabase_access_token",
        return_value="token-fixture-1",
    ) as mocked:
        token = resolve_fixture_user_bearer_token(
            "life-sim-user-0001",
            email="u@example.com",
            password="p" * 24,
        )
        assert token == "token-fixture-1"
        mocked.assert_called_once()
        # cache hit — no second fetch
        assert (
            resolve_fixture_user_bearer_token(
                "life-sim-user-0001",
                email="u@example.com",
                password="p" * 24,
            )
            == "token-fixture-1"
        )
        assert mocked.call_count == 1
    clear_bearer_token_caches()


def test_pool_m20_deprecated_flag_default_off(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LIFE_SIM_USE_POOL_M20", raising=False)
    assert life_sim.use_pool_m20_legacy() is False
    monkeypatch.setenv("LIFE_SIM_USE_POOL_M20", "1")
    assert life_sim.use_pool_m20_legacy() is True


def test_runner_imports_fixture_bearer_resolver() -> None:
    runner = Path("tests/simulation_runner.py").read_text(encoding="utf-8")
    assert "resolve_fixture_user_bearer_token" in runner
    assert "use_pool_m20_legacy" in runner
    assert Path("tests/sandbox/life_sim_provision_users.py").is_file()
    assert Path("tests/sandbox/life_sim_provision_lib.py").is_file()


def test_gitignore_covers_secrets() -> None:
    text = Path(".gitignore").read_text(encoding="utf-8")
    assert "tests/sandbox/.secrets/" in text
