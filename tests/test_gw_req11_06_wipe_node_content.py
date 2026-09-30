"""Offline unit tests for STORY-GW-REQ11-06 wipe helpers + confirm gate."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
GATEWAY_ROOT = TESTS.parent
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_wipe_lib as wipe  # noqa: E402
import life_sim_wipe_node_content as wipe_cli  # noqa: E402


def test_gateway_order_matches_required_readiness() -> None:
    wipe.assert_gateway_order_covers_readiness()
    assert set(wipe.GATEWAY_DELETE_ORDER) == set(wipe.REQUIRED_READINESS_TABLES)
    # Live import from product module when path available
    src = GATEWAY_ROOT / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from core.infrastructure.db_supabase import (  # noqa: E402
        REQUIRED_READINESS_TABLES as PRODUCT,
    )

    assert set(wipe.REQUIRED_READINESS_TABLES) == set(PRODUCT)


def test_threads_order_child_to_parent() -> None:
    assert wipe.THREADS_DELETE_ORDER == (
        "thread_reaction_marks",
        "thread_comments",
        "thread_threads",
    )


def test_plan_has_no_identity_tables() -> None:
    plan = wipe.full_wipe_plan()
    tables = [t for _, t, _ in plan]
    assert wipe.plan_contains_forbidden(tables) == []
    joined = " ".join(tables).lower()
    assert "auth.users" not in joined
    assert "auth_users" not in joined


def test_wipe_confirmed_cli_or_env() -> None:
    assert wipe.wipe_confirmed(cli_confirm=True, env={}) is True
    assert wipe.wipe_confirmed(cli_confirm=False, env={"LIFE_SIM_WIPE_CONFIRMED": "1"}) is True
    assert wipe.wipe_confirmed(cli_confirm=False, env={"LIFE_SIM_WIPE_CONFIRMED": "0"}) is False
    assert wipe.wipe_confirmed(cli_confirm=False, env={}) is False


def test_cli_refuses_without_confirm(capsys: pytest.CaptureFixture[str]) -> None:
    code = wipe_cli.main([])
    assert code == 2
    err = capsys.readouterr().err
    assert "REFUSED" in err
    assert "--confirm-wipe" in err


def test_cli_dry_run_no_confirm(capsys: pytest.CaptureFixture[str]) -> None:
    code = wipe_cli.main(["--dry-run"])
    assert code == 0
    out = capsys.readouterr().out
    assert "DRY-RUN" in out
    assert "story_labels" in out
    assert "stories" in out
    assert "thread_reaction_marks" in out
    assert "thread_threads" in out
    assert "Never deletes Identity" in out
    assert "DELETE auth" not in out


def test_cli_env_confirm_without_flag_attempts_env(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with patch.dict("os.environ", {"LIFE_SIM_WIPE_CONFIRMED": "1"}, clear=False):
        # Missing SUPABASE → exit 3 blocker, but past confirm gate
        code = wipe_cli.main([])
    assert code == 3
    err = capsys.readouterr().err
    assert "BLOCKER env" in err or "SUPABASE" in err


def test_script_source_has_no_auth_users_delete() -> None:
    text = (SANDBOX / "life_sim_wipe_node_content.py").read_text(encoding="utf-8")
    lib = (SANDBOX / "life_sim_wipe_lib.py").read_text(encoding="utf-8")
    for blob in (text, lib):
        assert "DELETE FROM auth" not in blob
        assert "/auth/users" not in blob
        assert "auth.admin" not in blob
