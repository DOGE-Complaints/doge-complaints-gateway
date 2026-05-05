from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DOGEIssue:
    """SPA-compatible issue card payload (required + optional fields per requirements/09)."""

    id: str
    status: str
    type: str
    labels: tuple[str, ...]
    title: dict[str, str]
    summary: dict[str, str]
    description: dict[str, str]
    institution: str | None = None
    created_at: str | None = None
    arweave_txid: str | None = None
    image_txid: str | None = None
    image_hash: str | None = None

    def to_public_dict(self) -> dict[str, Any]:
        """JSON-serializable shape for contract tests and API mapping."""
        out: dict[str, Any] = {
            "id": self.id,
            "status": self.status,
            "type": self.type,
            "labels": list(self.labels),
            "title": dict(self.title),
            "summary": dict(self.summary),
            "description": dict(self.description),
        }
        if self.institution is not None:
            out["institution"] = self.institution
        if self.created_at is not None:
            out["created_at"] = self.created_at
        if self.arweave_txid is not None:
            out["arweave_txid"] = self.arweave_txid
        if self.image_txid is not None:
            out["image_txid"] = self.image_txid
        if self.image_hash is not None:
            out["image_hash"] = self.image_hash
        return out
