"""GW-REQ11-10 — pack-wave replay state JSON (separate from fixture stories.json).

Per fixture_story_id: pending | submitted | failed.
Checkpoint after each complaint; resume skips submitted.
Never write replay status into pack stories.json.
No invent intake APIs / force-cluster.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

ReplayStatus = Literal["pending", "submitted", "failed"]
VALID_STATUSES: frozenset[str] = frozenset({"pending", "submitted", "failed"})


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_replay_state_path(pack_dir: Path, wave_id: str) -> Path:
    """Canonical layout: life_sim_packs/<pack_id>/waves/<wave_id>/replay_state.json."""
    wid = wave_id.strip()
    if not wid or "/" in wid or "\\" in wid or ".." in wid:
        raise ValueError(f"invalid wave_id={wave_id!r}")
    return pack_dir / "waves" / wid / "replay_state.json"


@dataclass
class ReplayWaveStore:
    """In-memory + on-disk checkpoint store for one pack replay wave."""

    pack_dir: Path
    wave_id: str
    path: Path
    entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load_or_create(
        cls,
        pack_dir: Path,
        wave_id: str,
        *,
        fixture_story_ids: list[str] | None = None,
        path: Path | None = None,
    ) -> ReplayWaveStore:
        state_path = path or default_replay_state_path(pack_dir, wave_id)
        store = cls(pack_dir=pack_dir, wave_id=wave_id, path=state_path)
        if state_path.is_file():
            store._load()
        else:
            store.meta = {
                "schema_note": "life-sim pack-wave replay state; not fixture stories.json",
                "wave_id": wave_id,
                "pack_dir": str(pack_dir),
                "created_at_utc": utc_now_iso(),
            }
            if fixture_story_ids:
                for sid in fixture_story_ids:
                    store.ensure_pending(sid)
            store.checkpoint()
        if fixture_story_ids:
            for sid in fixture_story_ids:
                store.ensure_pending(sid)
        return store

    def _load(self) -> None:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RuntimeError("replay wave state root must be a JSON object")
        stories = data.get("stories")
        if not isinstance(stories, dict):
            raise RuntimeError(
                "replay wave state.stories must be an object keyed by fixture_story_id"
            )
        self.meta = {k: v for k, v in data.items() if k != "stories"}
        self.entries = {}
        for sid, entry in stories.items():
            if not isinstance(entry, dict):
                continue
            status = str(entry.get("status") or "pending")
            if status not in VALID_STATUSES:
                status = "pending"
            self.entries[str(sid)] = {
                "status": status,
                "updated_at_utc": entry.get("updated_at_utc") or utc_now_iso(),
                "error": entry.get("error"),
                "gateway_story_id": entry.get("gateway_story_id"),
            }

    def ensure_pending(self, fixture_story_id: str) -> None:
        if fixture_story_id not in self.entries:
            self.entries[fixture_story_id] = {
                "status": "pending",
                "updated_at_utc": utc_now_iso(),
                "error": None,
                "gateway_story_id": None,
            }

    def get_status(self, fixture_story_id: str) -> ReplayStatus:
        entry = self.entries.get(fixture_story_id)
        if not entry:
            return "pending"
        status = str(entry.get("status") or "pending")
        if status not in VALID_STATUSES:
            return "pending"
        return status  # type: ignore[return-value]

    def is_submitted(self, fixture_story_id: str) -> bool:
        return self.get_status(fixture_story_id) == "submitted"

    def set_status(
        self,
        fixture_story_id: str,
        status: ReplayStatus,
        *,
        error: str | None = None,
        gateway_story_id: str | None = None,
        checkpoint: bool = True,
    ) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid replay wave status={status!r}")
        prev = self.entries.get(fixture_story_id) or {}
        self.entries[fixture_story_id] = {
            "status": status,
            "updated_at_utc": utc_now_iso(),
            "error": error,
            "gateway_story_id": gateway_story_id
            if gateway_story_id is not None
            else prev.get("gateway_story_id"),
        }
        if checkpoint:
            self.checkpoint()

    def checkpoint(self) -> Path:
        """Atomic-ish write of replay wave state (never touches stories.json)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        doc = {
            **self.meta,
            "updated_at_utc": utc_now_iso(),
            "stories": self.entries,
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.path)
        return self.path

    def stories_needing_work(self, fixture_story_ids: list[str]) -> list[str]:
        """Resume helper: skip entries already submitted."""
        return [sid for sid in fixture_story_ids if not self.is_submitted(sid)]
