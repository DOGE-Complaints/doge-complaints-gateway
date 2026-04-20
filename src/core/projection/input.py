from __future__ import annotations

from dataclasses import dataclass

from core.projection.i18n import I18nText


@dataclass(frozen=True)
class ProjectionInput:
    """Domain-side payload consumed by the projection engine before SPA mapping."""

    issue_id: str
    status: str
    issue_type: str
    labels: tuple[str, ...]
    title: I18nText
    summary: I18nText | None
    description: I18nText
    institution: str | None = None
    created_at: str | None = None
    arweave_txid: str | None = None
    image_txid: str | None = None
    image_hash: str | None = None
