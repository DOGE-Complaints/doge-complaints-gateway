from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Protocol, Tuple

from core.evidence.types import EvidencePackRecord


class EvidencePackRepository(Protocol):
    def save(self, record: EvidencePackRecord) -> EvidencePackRecord:
        """Persist evidence pack (immutable update: new snapshot version)."""

    def get_by_issue(self, issue_id: str) -> EvidencePackRecord | None:
        """Fetch latest pack for issue."""

    def list_pack_ids_for_story(self, story_id: str) -> Tuple[str, ...]:
        """Reverse lineage: packs referencing a story."""


@dataclass
class InMemoryEvidencePackRepository:
    _by_issue: Dict[str, EvidencePackRecord] = field(default_factory=dict)
    _by_story: Dict[str, List[str]] = field(default_factory=dict)

    def save(self, record: EvidencePackRecord) -> EvidencePackRecord:
        previous = self._by_issue.get(record.issue_id)
        if previous is not None:
            for sid in previous.story_ids:
                lst = self._by_story.get(sid, [])
                if previous.pack_id in lst:
                    lst.remove(previous.pack_id)
        self._by_issue[record.issue_id] = record
        for sid in record.story_ids:
            lst = self._by_story.setdefault(sid, [])
            if record.pack_id not in lst:
                lst.append(record.pack_id)
        return record

    def get_by_issue(self, issue_id: str) -> EvidencePackRecord | None:
        return self._by_issue.get(issue_id)

    def list_pack_ids_for_story(self, story_id: str) -> Tuple[str, ...]:
        return tuple(self._by_story.get(story_id, []))
