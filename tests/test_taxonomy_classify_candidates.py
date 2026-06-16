"""Unit tests for taxonomy cycle classify/apply helpers."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from core.projection.extraction_policy import _CANONICAL_TO_SPA_LABEL  # noqa: PLC2701
from core.taxonomy.cycle_lib import (
    CanonicalSnapshot,
    Decision,
    LabelAggregate,
    aggregate_miss_rows,
    classify_all,
    classify_label,
    decisions_from_manifest,
    is_valid_label_key,
    load_canonical_snapshot,
    parse_decisions_yaml,
    patch_canonical_mapping,
    read_canonical_dict_from_source,
    write_decisions_yaml,
)


def test_invalid_label_key_pattern_ignored() -> None:
    agg = LabelAggregate(label_key="Bad-Key", max_miss_count=10, locales=("en",))
    decision = classify_label(agg, snapshot=load_canonical_snapshot())
    assert decision.action == "ignore"
    assert "pattern" in decision.reason


def test_low_miss_count_ignored() -> None:
    agg = LabelAggregate(label_key="sidewalk", max_miss_count=2, locales=("en",))
    decision = classify_label(agg, snapshot=load_canonical_snapshot(), min_miss_count=3)
    assert decision.action == "ignore"


def test_already_mapped_canonical_is_translate_only() -> None:
    agg = LabelAggregate(label_key="roads", max_miss_count=5, locales=("et", "ru"))
    decision = classify_label(agg, snapshot=load_canonical_snapshot())
    assert decision.action == "translate_only"
    assert decision.spa_label == _CANONICAL_TO_SPA_LABEL["roads"]


def test_doge_issue_label_value_is_translate_only() -> None:
    snapshot = CanonicalSnapshot(
        canonical_keys=frozenset(),
        canonical_to_spa={},
        doge_issue_label_values=frozenset({"infrastructure"}),
    )
    agg = LabelAggregate(label_key="infrastructure", max_miss_count=4, locales=("en",))
    decision = classify_label(agg, snapshot=snapshot)
    assert decision.action == "translate_only"
    assert decision.spa_label == "infrastructure"


def test_new_token_is_pending() -> None:
    agg = LabelAggregate(label_key="sidewalk", max_miss_count=5, locales=("en",))
    decision = classify_label(agg, snapshot=load_canonical_snapshot())
    assert decision.action == "pending"


def test_aggregate_miss_rows_groups_by_key() -> None:
    rows = [
        {"label_key": "roads", "locale": "et", "miss_count": 4},
        {"label_key": "roads", "locale": "ru", "miss_count": 6},
        {"label_key": "roads", "locale": "en", "miss_count": 1},
    ]
    aggregates = aggregate_miss_rows(rows, min_miss_count=3)
    assert len(aggregates) == 1
    assert aggregates[0].max_miss_count == 6
    assert aggregates[0].locales == ("et", "ru")


def test_is_valid_label_key() -> None:
    assert is_valid_label_key("ab")
    assert is_valid_label_key("sidewalk")
    assert not is_valid_label_key("A")
    assert not is_valid_label_key("bad-key")


def test_yaml_roundtrip() -> None:
    decisions = [
        Decision(
            label_key="roads",
            action="translate_only",
            spa_label="infrastructure",
            locales=("et", "ru"),
            reason="mapped",
        )
    ]
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "decisions.yaml"
        write_decisions_yaml(path, cycle_id="20260615", decisions=decisions)
        parsed = parse_decisions_yaml(path.read_text(encoding="utf-8"))
        restored = decisions_from_manifest(parsed)
        assert restored[0].label_key == "roads"
        assert restored[0].action == "translate_only"
        assert restored[0].spa_label == "infrastructure"


def test_patch_canonical_mapping_idempotent() -> None:
    source = Path("src/core/projection/extraction_policy.py").read_text(encoding="utf-8")
    current = read_canonical_dict_from_source(source)
    sample_key = "zz_taxonomy_test_key"
    sample_val = "infrastructure"
    if sample_key in current:
        pytest.skip("test key already present")
    patched = patch_canonical_mapping(source, canonical=sample_key, spa_label=sample_val)
    again = patch_canonical_mapping(patched, canonical=sample_key, spa_label=sample_val)
    assert again == patched
    updated = read_canonical_dict_from_source(patched)
    assert updated[sample_key] == sample_val


def test_classify_all_from_misses_json_fixture() -> None:
    rows = [
        {"label_key": "roads", "locale": "et", "miss_count": 5},
        {"label_key": "sidewalk", "locale": "en", "miss_count": 1},
        {"label_key": "!!", "locale": "en", "miss_count": 99},
    ]
    aggregates = aggregate_miss_rows(rows, min_miss_count=3)
    decisions = classify_all(aggregates)
    by_key = {d.label_key: d.action for d in decisions}
    assert by_key["roads"] == "translate_only"
    assert by_key["sidewalk"] == "ignore"
    assert by_key["!!"] == "ignore"


def test_apply_gateway_smoke_import() -> None:
    from core.projection.extraction_policy import spa_labels_from_canonical

    assert spa_labels_from_canonical(("roads",)) == ("infrastructure",)


def test_manifest_json_compat() -> None:
    payload = {
        "cycle_id": "20260615",
        "thresholds": {"min_miss_count": 3},
        "decisions": [
            {
                "label_key": "roads",
                "action": "translate_only",
                "spa_label": "infrastructure",
                "locales": ["et"],
                "auto": True,
                "reason": "test",
            }
        ],
    }
    # decisions_from_manifest accepts parsed dict directly
    restored = decisions_from_manifest(payload)
    assert len(restored) == 1


def test_taxonomy_cli_scripts_do_not_touch_readiness_tables() -> None:
    scripts = Path("scripts")
    for name in (
        "taxonomy_fetch_misses.py",
        "taxonomy_classify_candidates.py",
        "taxonomy_apply_gateway.py",
        "taxonomy_apply_spa_i18n.py",
    ):
        text = (scripts / name).read_text(encoding="utf-8")
        assert "REQUIRED_READINESS_TABLES" not in text
        assert "db_supabase.py" not in text


def test_taxonomy_cli_scripts_do_not_invoke_backfill_write() -> None:
    """TC6b gate: taxonomy cycle scripts never call reproject (operator runs it separately)."""
    scripts = Path("scripts")
    for name in (
        "taxonomy_fetch_misses.py",
        "taxonomy_classify_candidates.py",
        "taxonomy_apply_gateway.py",
        "taxonomy_apply_spa_i18n.py",
    ):
        text = (scripts / name).read_text(encoding="utf-8")
        assert "reproject_issue_i18n" not in text


def test_apply_gateway_rejects_new_board_label_without_manifest_flag(
    tmp_path: Path,
) -> None:
    manifest = tmp_path / "taxonomy-decisions.yaml"
    write_decisions_yaml(
        manifest,
        cycle_id="20260529",
        decisions=[
            Decision(
                label_key="sidewalk",
                action="new_board_label",
                target_label="transport",
                new_board_label=False,
                reason="missing flag",
            )
        ],
    )
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "scripts/taxonomy_apply_gateway.py",
            "--manifest",
            str(manifest),
            "--dry-run",
        ],
        cwd=Path.cwd(),
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "new_board_label: true" in result.stderr + result.stdout
