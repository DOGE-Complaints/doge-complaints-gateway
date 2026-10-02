"""Offline tests for STORY-GW-REQ11-12 rich stories generator + adapter v2."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

TESTS = Path(__file__).resolve().parent
SANDBOX = TESTS / "sandbox"
GATEWAY = TESTS.parent
sys.path.insert(0, str(SANDBOX))

import life_sim_replay_lib as life_sim  # noqa: E402
import life_sim_stories_v2_lib as v2  # noqa: E402

REF_PACK = SANDBOX / "life_sim_packs" / "ls-20261002T0906Z-veerenni-v2-rich"
LEGACY_PACK = (
    SANDBOX / "life_sim_packs" / "ls-20260930T0938Z-veerenni-yard-construction"
)


def test_build_v2_schema_and_scale_locks() -> None:
    payload = v2.build(seed=v2.SEED, params={})
    stories = payload["stories"]
    meta = payload["meta"]
    assert meta["counts"]["users"] == 200
    assert meta["counts"]["stories"] == 1661
    assert abs(meta["counts"]["pre_fraction"] - 0.25) < 0.02
    assert abs(meta["counts"]["post_fraction"] - 0.75) < 0.02
    langs = meta["counts"]["lang_fractions"]
    assert abs(langs["et"] - 0.60) < 0.05
    assert abs(langs["ru"] - 0.30) < 0.05
    assert abs(langs["en"] - 0.10) < 0.05
    row = stories[0]
    for key in v2.V2_REQUIRED_KEYS:
        assert key in row, key
    assert "narrative" not in row
    assert "gpt_signals" not in row
    assert "story_id" not in row
    assert isinstance(row["title_i18n"], dict)
    assert set(row["title_i18n"]) >= {"et", "ru", "en"}
    assert row["canonical_type"] == "complaint"


def test_diversity_full_uniqueness() -> None:
    payload = v2.build(seed=v2.SEED, params=v2.default_params_snapshot())
    bodies = [str(s["body"]) for s in payload["stories"]]
    n = len(bodies)
    unique = len(set(bodies))
    assert unique == n
    assert payload["meta"]["diversity"]["pass_full_uniqueness"] is True
    assert payload["meta"]["diversity"]["llm"] is False


def test_params_foci_consumed_vs_defaults() -> None:
    empty = v2.build(seed=v2.SEED, params={})
    assert empty["meta"]["params_consumed"]["location_query"] == v2.DEFAULT_LOCATION
    assert empty["meta"]["params_consumed"]["story_foci_themes"] == list(
        v2.DEFAULT_THEME_IDS
    )

    params = {
        "node_social_direction": "construction noise near school",
        "user_context": {"neighbourhood_tags": ["Uus Veerenni", "Tallinn"]},
        "story_foci": {"themes": [{"id": "construction", "weight": 1.0}]},
    }
    focused = v2.build(seed=v2.SEED, params=params)
    assert focused["meta"]["params_consumed"]["story_foci_themes"] == ["construction"]
    assert focused["meta"]["params_consumed"]["location_query"] == "Uus Veerenni, Tallinn"
    assert focused["meta"]["params_consumed"]["node_social_direction_present"] is True
    assert all("construction" in s["canonical_labels"] for s in focused["stories"][:20])
    assert "construction noise" in focused["stories"][0]["body"]


def test_adapter_prefer_v2_and_thin_six_key() -> None:
    binding = {"pack": "test"}
    thin = {
        "fixture_story_id": "life-sim-story-00001",
        "language": "en",
        "title": "Short title",
        "body": "Thin six-key body.",
    }
    thin_out = life_sim.life_sim_story_to_intake_payload(
        thin,
        intake_schema_version="1",
        schema_binding=binding,
        location_query="Caller Loc",
    )
    narr = thin_out["narrative"]
    assert narr["original_text"] == "Thin six-key body."
    assert narr["session_language"] == "en"
    assert narr["title"]["en"] == "Short title"
    assert narr["description"]["et"] == "Thin six-key body."
    assert narr["canonical_type"] == "complaint"
    assert narr["canonical_labels"] == []
    assert narr["location_query"] == "Caller Loc"
    assert "institution" not in narr

    rich = {
        "fixture_story_id": "life-sim-story-00002",
        "language": "et",
        "title": "ignored-when-i18n",
        "body": "fallback-body",
        "title_i18n": {"et": "ET pealkiri", "ru": "RU title", "en": "EN title"},
        "description_i18n": {
            "et": "ET kirjeldus",
            "ru": "RU описание",
            "en": "EN description",
        },
        "summary_i18n": {"et": "ET kokkuvõte", "ru": "RU summary", "en": "EN summary"},
        "session_language": "et",
        "location_query": "Uus Veerenni, Tallinn",
        "canonical_type": "complaint",
        "canonical_labels": ["construction", "uus-veerenni"],
        "institution_i18n": {
            "et": "Tallinna Linnavalitsus",
            "ru": "Таллиннская городская управа",
            "en": "Tallinn City Government",
        },
    }
    rich_out = life_sim.life_sim_story_to_intake_payload(
        rich,
        intake_schema_version="1",
        schema_binding=binding,
        location_query="ShouldNotWin",
    )
    rn = rich_out["narrative"]
    assert rn["original_text"] == "ET kirjeldus"
    assert rn["title"]["et"] == "ET pealkiri"
    assert rn["title"]["en"] == "EN title"
    assert rn["description"]["ru"] == "RU описание"
    assert rn["summary"]["et"] == "ET kokkuvõte"
    assert rn["session_language"] == "et"
    assert rn["location_query"] == "Uus Veerenni, Tallinn"
    assert rn["canonical_labels"] == ["construction", "uus-veerenni"]
    assert rn["institution"]["en"] == "Tallinn City Government"
    assert rich_out["origin"]["conversation_id"] == "life-sim-story-00002"


def test_fail_closed_pack_dir_still_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LIFE_SIM_PACK_DIR", raising=False)
    monkeypatch.delenv("PACK_DIR", raising=False)
    with pytest.raises(RuntimeError, match="LIFE_SIM_PACK_DIR"):
        life_sim.require_life_sim_pack_dir()


def test_req11_10_pack_read_smoke_accepts_v2_pack(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """REQ11-10 pack reader still accepts pack with stories.json Present."""
    pack = tmp_path / "pack"
    pack.mkdir()
    tiny = [
        {
            "fixture_story_id": "life-sim-story-00001",
            "fixture_user_id": "life-sim-user-0001",
            "language": "en",
            "created_at": "2026-06-01T00:00:00Z",
            "title": "t",
            "body": "b [life-sim#00001]",
            "title_i18n": {"et": "t", "ru": "t", "en": "t"},
            "description_i18n": {"et": "b", "ru": "b", "en": "b"},
            "summary_i18n": {"et": "b", "ru": "b", "en": "b"},
            "session_language": "en",
            "location_query": "Uus Veerenni, Tallinn",
            "canonical_type": "complaint",
            "canonical_labels": ["waste"],
        }
    ]
    (pack / "stories.json").write_text(
        json.dumps(tiny, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (pack / "users.json").write_text("[]\n", encoding="utf-8")
    monkeypatch.setenv("LIFE_SIM_PACK_DIR", str(pack))
    resolved = life_sim.require_life_sim_pack_dir()
    assert resolved == pack.resolve()
    stories = json.loads((resolved / "stories.json").read_text(encoding="utf-8"))
    assert len(stories) == 1
    assert stories[0]["fixture_story_id"] == "life-sim-story-00001"
    assert "title_i18n" in stories[0]


def test_reference_pack_on_disk_v2_if_present() -> None:
    if not REF_PACK.is_dir():
        pytest.skip("reference v2 pack not generated yet")
    stories = json.loads((REF_PACK / "stories.json").read_text(encoding="utf-8"))
    assert len(stories) == 1661
    bodies = {str(s["body"]) for s in stories}
    assert len(bodies) == 1661
    row = stories[0]
    for key in v2.V2_REQUIRED_KEYS:
        assert key in row
    assert (REF_PACK / "params.json").is_file()
    # Legacy 6-key pack remains Partial SSOT for prior waves — not overwritten.
    if LEGACY_PACK.is_dir():
        legacy = json.loads((LEGACY_PACK / "stories.json").read_text(encoding="utf-8"))
        assert "title_i18n" not in legacy[0]
