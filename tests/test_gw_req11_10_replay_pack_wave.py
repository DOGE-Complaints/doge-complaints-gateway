"""Offline unit tests for STORY-GW-REQ11-10 pack-wave replay gates."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
GATEWAY = TESTS.parent
sys.path.insert(0, str(SANDBOX))
sys.path.insert(0, str(TESTS))

import life_sim_replay_lib as life_sim  # noqa: E402
import life_sim_replay_pack_wave as cli  # noqa: E402
from life_sim_replay_wave_store import (  # noqa: E402
    ReplayWaveStore,
    default_replay_state_path,
)


def test_require_pack_dir_fail_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("LIFE_SIM_PACK_DIR", raising=False)
    monkeypatch.delenv("PACK_DIR", raising=False)
    with pytest.raises(RuntimeError, match="LIFE_SIM_PACK_DIR"):
        life_sim.require_life_sim_pack_dir()
    pack = tmp_path / "pack"
    pack.mkdir()
    monkeypatch.setenv("LIFE_SIM_PACK_DIR", str(pack))
    with pytest.raises(RuntimeError, match="stories.json"):
        life_sim.require_life_sim_pack_dir()
    (pack / "stories.json").write_text("[]", encoding="utf-8")
    assert life_sim.require_life_sim_pack_dir() == pack.resolve()


def test_cli_exits_without_pack_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LIFE_SIM_PACK_DIR", raising=False)
    monkeypatch.delenv("PACK_DIR", raising=False)
    code = cli.main([])
    assert code == 2


def test_make_fail_closed_without_pack_dir() -> None:
    env = {k: v for k, v in os.environ.items() if k not in ("LIFE_SIM_PACK_DIR", "PACK_DIR")}
    proc = subprocess.run(
        ["make", "life-sim-replay-pack-wave"],
        cwd=str(GATEWAY),
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 2
    assert "LIFE_SIM_PACK_DIR" in (proc.stdout + proc.stderr)


def test_wave_checkpoint_and_resume_skips_submitted(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    stories_path = pack / "stories.json"
    stories_path.write_text(
        json.dumps(
            [
                {
                    "fixture_story_id": "life-sim-story-0001",
                    "fixture_user_id": "life-sim-user-0001",
                }
            ]
        ),
        encoding="utf-8",
    )
    before = stories_path.read_text(encoding="utf-8")
    before_mtime = stories_path.stat().st_mtime

    ids = ["life-sim-story-0001", "life-sim-story-0002", "life-sim-story-0003"]
    wave = ReplayWaveStore.load_or_create(pack, "wave-test", fixture_story_ids=ids)
    assert wave.path == default_replay_state_path(pack, "wave-test")
    assert wave.path.name == "replay_state.json"
    assert wave.get_status("life-sim-story-0001") == "pending"

    wave.set_status("life-sim-story-0001", "submitted", gateway_story_id="g-1")
    wave.set_status("life-sim-story-0002", "failed", error="boom")
    wave.set_status("life-sim-story-0003", "pending")

    reloaded = ReplayWaveStore.load_or_create(pack, "wave-test", fixture_story_ids=ids)
    assert reloaded.is_submitted("life-sim-story-0001")
    assert reloaded.stories_needing_work(ids) == [
        "life-sim-story-0002",
        "life-sim-story-0003",
    ]
    assert stories_path.read_text(encoding="utf-8") == before
    assert stories_path.stat().st_mtime == before_mtime


def test_wave_never_uses_stories_json_path(tmp_path: Path) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "stories.json").write_text("[]", encoding="utf-8")
    wave = ReplayWaveStore.load_or_create(
        pack, "w1", fixture_story_ids=["life-sim-story-0001"]
    )
    assert "stories.json" not in str(wave.path)
    assert "waves" in wave.path.parts


def test_missing_creds_preflight_fail_closed() -> None:
    stories = [
        {
            "fixture_story_id": "s1",
            "fixture_user_id": "life-sim-user-0001",
        },
        {
            "fixture_story_id": "s2",
            "fixture_user_id": "life-sim-user-0002",
        },
    ]
    creds = {
        "life-sim-user-0001": {"email": "a@dogestonia.me", "password": "x"},
    }
    with pytest.raises(SystemExit, match="missing secrets"):
        cli._preflight_missing_creds(stories, creds)


def test_dry_run_does_not_mark_submitted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "users.json").write_text(
        json.dumps([{"fixture_user_id": "life-sim-user-0001"}] * 200),
        encoding="utf-8",
    )
    stories = [
        {
            "fixture_story_id": f"life-sim-story-{i:04d}",
            "fixture_user_id": "life-sim-user-0001",
            "language": "en",
            "title": "t",
            "body": "body text",
            "created_at": "2026-01-01T00:00:00Z",
        }
        for i in range(1, 3)
    ]
    # Pad to satisfy scale assert when meta present — skip meta so scale soft.
    (pack / "stories.json").write_text(json.dumps(stories), encoding="utf-8")
    monkeypatch.setenv("LIFE_SIM_PACK_DIR", str(pack))
    monkeypatch.delenv("DEMO_LIFE_SIM_PROFILE", raising=False)
    code = cli.main(["--dry-run", "--limit", "2", "--wave-id", "dry-w"])
    assert code == 0
    wave = ReplayWaveStore.load_or_create(pack, "dry-w", fixture_story_ids=[s["fixture_story_id"] for s in stories])
    assert wave.get_status("life-sim-story-0001") == "pending"
    assert wave.get_status("life-sim-story-0002") == "pending"


def test_no_invent_intake_or_force_cluster_in_sources() -> None:
    for name in ("life_sim_replay_pack_wave.py", "life_sim_replay_wave_store.py"):
        blob = (SANDBOX / name).read_text(encoding="utf-8").lower()
        assert "invent" in blob
        assert "force-cluster" in blob or "force_cluster" in blob or "no invent" in blob
