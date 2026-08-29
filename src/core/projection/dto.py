from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


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
    institution: dict[str, str] | None = None
    created_at: str | None = None
    arweave_txid: str | None = None
    image_txid: str | None = None
    image_hash: str | None = None
    geo: dict[str, object] | None = None
    original_locale: tuple[str, ...] = ()

    def to_public_dict(
        self, *, schema_card: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """JSON-serializable shape for contract tests and API mapping.

        Civic card keys stay required as today. Optional ``schema_card`` is a named
        sidecar (flat dotted-path keys) — never a raw payload dump.
        """
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
            out["institution"] = dict(self.institution)
        if self.created_at is not None:
            out["created_at"] = self.created_at
        if self.arweave_txid is not None:
            out["arweave_txid"] = self.arweave_txid
        if self.image_txid is not None:
            out["image_txid"] = self.image_txid
        if self.image_hash is not None:
            out["image_hash"] = self.image_hash
        if self.geo is not None:
            out["geo"] = self.geo
        if self.original_locale:
            out["original_locale"] = list(self.original_locale)
        if schema_card:
            out["schema_card"] = dict(schema_card)
        return out
