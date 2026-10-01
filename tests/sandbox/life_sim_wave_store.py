"""GW-REQ11-08 — pack-wave state JSON (separate from fixture users.json).

Per fixture_user_id: pending | created | verified | failed.
Checkpoint after each step; resume skips verified.
Never write provision status into pack users.json.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

WaveStatus = Literal["pending", "created", "verified", "failed"]
VALID_STATUSES: frozenset[str] = frozenset({"pending", "created", "verified", "failed"})


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def default_wave_state_path(pack_dir: Path, wave_id: str) -> Path:
    """Canonical layout: life_sim_packs/<pack_id>/waves/<wave_id>/state.json."""
    wid = wave_id.strip()
    if not wid or "/" in wid or "\\" in wid or ".." in wid:
        raise ValueError(f"invalid wave_id={wave_id!r}")
    return pack_dir / "waves" / wid / "state.json"


@dataclass
class WaveStore:
    """In-memory + on-disk checkpoint store for one pack wave."""

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
        fixture_user_ids: list[str] | None = None,
        path: Path | None = None,
    ) -> WaveStore:
        state_path = path or default_wave_state_path(pack_dir, wave_id)
        store = cls(pack_dir=pack_dir, wave_id=wave_id, path=state_path)
        if state_path.is_file():
            store._load()
        else:
            store.meta = {
                "schema_note": "life-sim pack-wave state; not fixture users.json",
                "wave_id": wave_id,
                "pack_dir": str(pack_dir),
                "created_at_utc": utc_now_iso(),
            }
            if fixture_user_ids:
                for fid in fixture_user_ids:
                    store.ensure_pending(fid)
            store.checkpoint()
        if fixture_user_ids:
            for fid in fixture_user_ids:
                store.ensure_pending(fid)
        return store

    def _load(self) -> None:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise RuntimeError("wave state root must be a JSON object")
        users = data.get("users")
        if not isinstance(users, dict):
            raise RuntimeError("wave state.users must be an object keyed by fixture_user_id")
        self.meta = {k: v for k, v in data.items() if k != "users"}
        self.entries = {}
        for fid, entry in users.items():
            if not isinstance(entry, dict):
                continue
            status = str(entry.get("status") or "pending")
            if status not in VALID_STATUSES:
                status = "pending"
            self.entries[str(fid)] = {
                "status": status,
                "updated_at_utc": entry.get("updated_at_utc") or utc_now_iso(),
                "error": entry.get("error"),
            }

    def ensure_pending(self, fixture_user_id: str) -> None:
        if fixture_user_id not in self.entries:
            self.entries[fixture_user_id] = {
                "status": "pending",
                "updated_at_utc": utc_now_iso(),
                "error": None,
            }

    def get_status(self, fixture_user_id: str) -> WaveStatus:
        entry = self.entries.get(fixture_user_id)
        if not entry:
            return "pending"
        status = str(entry.get("status") or "pending")
        if status not in VALID_STATUSES:
            return "pending"
        return status  # type: ignore[return-value]

    def is_verified(self, fixture_user_id: str) -> bool:
        return self.get_status(fixture_user_id) == "verified"

    def set_status(
        self,
        fixture_user_id: str,
        status: WaveStatus,
        *,
        error: str | None = None,
        checkpoint: bool = True,
    ) -> None:
        if status not in VALID_STATUSES:
            raise ValueError(f"invalid wave status={status!r}")
        self.entries[fixture_user_id] = {
            "status": status,
            "updated_at_utc": utc_now_iso(),
            "error": error,
        }
        if checkpoint:
            self.checkpoint()

    def checkpoint(self) -> Path:
        """Atomic-ish write of wave state (never touches users.json)."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        doc = {
            **self.meta,
            "updated_at_utc": utc_now_iso(),
            "users": self.entries,
        }
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        tmp.replace(self.path)
        return self.path

    def users_needing_work(self, fixture_user_ids: list[str]) -> list[str]:
        """Resume helper: skip entries already verified."""
        return [fid for fid in fixture_user_ids if not self.is_verified(fid)]
