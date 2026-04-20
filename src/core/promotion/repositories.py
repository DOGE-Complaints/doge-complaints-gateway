from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Protocol

from core.promotion.types import IssueCandidateRecord, ReviewAuditEntry


class IssueCandidateStore(Protocol):
    def save(self, record: IssueCandidateRecord) -> IssueCandidateRecord:
        """Persist or replace a candidate record."""

    def get(self, candidate_id: str) -> IssueCandidateRecord | None:
        """Fetch candidate by id."""

    def delete(self, candidate_id: str) -> None:
        """Remove candidate by id."""


class ReviewAuditLogRepository(Protocol):
    def append(self, entry: ReviewAuditEntry) -> ReviewAuditEntry:
        """Append audit entry for a candidate."""

    def list_for_candidate(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        """Return ordered audit trail for candidate."""


@dataclass
class InMemoryIssueCandidateStore:
    _records: Dict[str, IssueCandidateRecord] | None = None

    def __post_init__(self) -> None:
        if self._records is None:
            self._records = {}

    def save(self, record: IssueCandidateRecord) -> IssueCandidateRecord:
        assert self._records is not None
        self._records[record.candidate_id] = record
        return record

    def get(self, candidate_id: str) -> IssueCandidateRecord | None:
        assert self._records is not None
        return self._records.get(candidate_id)

    def delete(self, candidate_id: str) -> None:
        assert self._records is not None
        self._records.pop(candidate_id, None)


@dataclass
class InMemoryReviewAuditLogRepository:
    _entries: Dict[str, List[ReviewAuditEntry]] | None = None

    def __post_init__(self) -> None:
        if self._entries is None:
            self._entries = {}

    def append(self, entry: ReviewAuditEntry) -> ReviewAuditEntry:
        assert self._entries is not None
        self._entries.setdefault(entry.candidate_id, []).append(entry)
        return entry

    def list_for_candidate(self, candidate_id: str) -> tuple[ReviewAuditEntry, ...]:
        assert self._entries is not None
        return tuple(self._entries.get(candidate_id, []))
