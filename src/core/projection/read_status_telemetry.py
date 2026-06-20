from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

_UNKNOWN_STATUSES_FILENAME = "unknown_issue_statuses.jsonl"
_seen_raw_statuses: set[str] = set()
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
        raw_status = record.get("raw_status")
        if isinstance(raw_status, str) and raw_status:
            seen.add(raw_status)
    return seen


def record_unknown_issue_status(
    *,
    raw_status: str,
    issue_id: str,
    normalized_to: str,
) -> None:
    """Append first-seen unknown issue statuses to LOG_DEBUG_DIR accumulator file."""
    debug_dir = _debug_dir()
    if debug_dir is None:
        return

    with _lock:
        if raw_status in _seen_raw_statuses:
            return
        path = Path(debug_dir) / _UNKNOWN_STATUSES_FILENAME
        path.parent.mkdir(parents=True, exist_ok=True)
        file_seen = _load_seen_from_file(path)
        if raw_status in file_seen:
            _seen_raw_statuses.add(raw_status)
            return

        record = {
            "ts": datetime.now(UTC).isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "raw_status": raw_status,
            "issue_id": issue_id,
            "normalized_to": normalized_to,
        }
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        _seen_raw_statuses.add(raw_status)


def reset_unknown_issue_status_log_state() -> None:
    """Clear in-process dedupe cache (tests only)."""
    with _lock:
        _seen_raw_statuses.clear()
