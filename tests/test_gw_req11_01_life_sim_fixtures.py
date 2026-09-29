"""GW-REQ11-01 — life-sim users+stories fixtures scale / langs / 2026 curve."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import pytest

SANDBOX = Path(__file__).resolve().parent / "sandbox"
USERS = SANDBOX / "dogestonia_life_sim_users_v0_1.json"
STORIES = SANDBOX / "dogestonia_life_sim_stories_v0_1.json"
META = SANDBOX / "dogestonia_life_sim_fixtures_v0_1_meta.json"
BREAKPOINT = datetime(2026, 9, 30, 0, 0, 0, tzinfo=timezone.utc)
YEAR_START = datetime(2026, 1, 1, tzinfo=timezone.utc)
YEAR_END = datetime(2026, 12, 31, 23, 59, 59, tzinfo=timezone.utc)


@pytest.fixture(scope="module")
def fixtures() -> tuple[list[dict], list[dict], dict]:
    users = json.loads(USERS.read_text(encoding="utf-8"))
    stories = json.loads(STORIES.read_text(encoding="utf-8"))
    meta = json.loads(META.read_text(encoding="utf-8"))
    return users, stories, meta


def test_ac01_scale_users_stories_gaussian(fixtures: tuple[list[dict], list[dict], dict]) -> None:
    users, stories, _meta = fixtures
    assert USERS.is_file() and STORIES.is_file()
    assert len(users) == 200
    assert 1500 <= len(stories) <= 1900  # ~1700 order at 200×8.5
    per = Counter(str(s["fixture_user_id"]) for s in stories)
    assert len(per) == 200
    vals = list(per.values())
    assert min(vals) >= 1 and max(vals) <= 20
    mean = sum(vals) / len(vals)
    assert 7.0 <= mean <= 10.0  # Gaussian mean lock 8.5 ± tolerance


def test_ac02_language_mix(fixtures: tuple[list[dict], list[dict], dict]) -> None:
    _users, stories, _meta = fixtures
    langs = Counter(str(s["language"]) for s in stories)
    n = len(stories)
    et, ru, en = langs["et"] / n, langs["ru"] / n, langs["en"] / n
    assert abs(et - 0.60) <= 0.03
    assert abs(ru - 0.30) <= 0.03
    assert abs(en - 0.10) <= 0.03


def test_ac03_timestamps_2026_exp_mass(fixtures: tuple[list[dict], list[dict], dict]) -> None:
    _users, stories, _meta = fixtures
    times = [
        datetime.strptime(str(s["created_at"]), "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
        for s in stories
    ]
    assert min(times) >= YEAR_START
    assert max(times) <= YEAR_END
    pre = sum(1 for t in times if t < BREAKPOINT)
    post = len(times) - pre
    assert abs(pre / len(times) - 0.25) <= 0.02
    assert abs(post / len(times) - 0.75) <= 0.02
    # Exponential intent: post window denser than pre (more stories / shorter span).
    pre_days = (BREAKPOINT - YEAR_START).total_seconds() / 86400.0
    post_days = (YEAR_END - BREAKPOINT).total_seconds() / 86400.0
    assert (post / post_days) > (pre / pre_days)


def test_meta_paths_match_disk(fixtures: tuple[list[dict], list[dict], dict]) -> None:
    _users, _stories, meta = fixtures
    assert meta["paths"]["users"] == USERS.name
    assert meta["paths"]["stories"] == STORIES.name
    assert meta["counts"]["users"] == 200
