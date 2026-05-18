"""Shared helpers for REQ-39 zone J–N contract tests (STORY-M2-18-01)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from core.infrastructure.db_sqlite import SqliteDatabase, SqliteIssueProjectionStore
from core.infrastructure.repositories import InMemoryIssueProjectionStore

PolicyVersion = "m3.doge_issue_derivation.v1"


def projection_payload(
    issue_id: str,
    *,
    status: str = "PUBLISHED",
    issue_type: str = "INCIDENT",
    labels: list[str] | None = None,
    institution: str | None = None,
    geo: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "id": issue_id,
        "status": status,
        "type": issue_type,
        "labels": labels or ["infrastructure"],
        "title": {"et": "t", "ru": "t", "en": "t"},
        "summary": {"et": "s", "ru": "s", "en": "s"},
        "description": {"et": "d", "ru": "d", "en": "d"},
    }
    if institution is not None:
        payload["institution"] = institution
    if geo is not None:
        payload["geo"] = geo
    return payload


def inmemory_store_factory() -> InMemoryIssueProjectionStore:
    return InMemoryIssueProjectionStore()


def sqlite_store_factory(tmp_path: Path) -> SqliteIssueProjectionStore:
    db = SqliteDatabase.from_url(f"sqlite:///{tmp_path / 'contract.sqlite'}")
    db.ensure_schema()
    return SqliteIssueProjectionStore(db)


StoreFactory = Callable[[], InMemoryIssueProjectionStore | SqliteIssueProjectionStore]
