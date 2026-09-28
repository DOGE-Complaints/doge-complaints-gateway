"""GW-REQ10-02: slim lifecycle parse — no RECEIVED map, fail-closed, no debug I/O."""

from __future__ import annotations

from pathlib import Path

import pytest

from core.domain import StoryLifecycleStatus
from core.infrastructure.db_supabase import _parse_lifecycle_status

_SRC = Path(__file__).resolve().parents[1] / "src"


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("accepted", StoryLifecycleStatus.ACCEPTED),
        ("partial_ready", StoryLifecycleStatus.PARTIAL_READY),
        ("ready_for_profile", StoryLifecycleStatus.READY_FOR_PROFILE),
        ("clustered", StoryLifecycleStatus.CLUSTERED),
    ],
)
def test_parse_lifecycle_status_accepts_enum_values(
    raw: str, expected: StoryLifecycleStatus
) -> None:
    assert _parse_lifecycle_status(raw, story_id="s1") is expected


@pytest.mark.parametrize("raw", ["RECEIVED", "received", "pending", "", "OPEN"])
def test_parse_lifecycle_status_unknown_fail_closed(raw: str) -> None:
    with pytest.raises(ValueError):
        _parse_lifecycle_status(raw, story_id="s-legacy")


def test_src_has_no_cursor_debug_lifecycle_writes() -> None:
    hits: list[str] = []
    for path in _SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        if "debug-ba94c7" in text or ".cursor/debug" in text:
            hits.append(str(path.relative_to(_SRC.parent)))
        if "#region agent log" in text and "lifecycle" in text.lower():
            hits.append(f"{path.relative_to(_SRC.parent)}:#region")
    assert hits == [], f"debug I/O residue under src: {hits}"


def test_parse_lifecycle_status_source_has_no_received_special_case() -> None:
    src = (
        Path(__file__).resolve().parents[1]
        / "src/core/infrastructure/db_supabase.py"
    ).read_text(encoding="utf-8")
    # Function body must not keep permanent RECEIVED→ACCEPTED map keys.
    assert '"RECEIVED"' not in src
    assert '"received"' not in src
    assert "debug-ba94c7" not in src
