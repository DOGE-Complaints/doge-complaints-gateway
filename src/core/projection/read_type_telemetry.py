from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

_UNKNOWN_TYPES_FILENAME = "unknown_issue_types.jsonl"
_seen_raw_types: set[str] = set()
_lock = Lock()


def _debug_dir() -> str | None:
    value = os.environ.get("LOG_DEBUG_DIR", "").strip()
    return value or None


def _load_seen_from_file(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    seen: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        raw_type = record.get("raw_type")
        if isinstance(raw_type, str) and raw_type:
            seen.add(raw_type)
    return seen


def record_unknown_issue_type(
    *,
    raw_type: str,
    issue_id: str,
    normalized_to: str,
) -> None:
    """Append first-seen unknown issue types to LOG_DEBUG_DIR accumulator file."""
    debug_dir = _debug_dir()
    if debug_dir is None:
        return

    with _lock:
        if raw_type in _seen_raw_types:
            return
        path = Path(debug_dir) / _UNKNOWN_TYPES_FILENAME
        path.parent.mkdir(parents=True, exist_ok=True)
        file_seen = _load_seen_from_file(path)
        if raw_type in file_seen:
            _seen_raw_types.add(raw_type)
            return

        record = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "raw_type": raw_type,
            "issue_id": issue_id,
            "normalized_to": normalized_to,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        _seen_raw_types.add(raw_type)


def reset_unknown_issue_type_log_state() -> None:
    """Clear in-process dedupe cache (tests only)."""
    with _lock:
        _seen_raw_types.clear()
