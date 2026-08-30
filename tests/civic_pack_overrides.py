"""Test-only civic knob overlay. Not an env dual-source; patches the pack resolver."""

from __future__ import annotations

from dataclasses import replace

import pytest

from core.config import schema as config_schema
from core.schema.contracts import CivicClusteringBlock


def monkeypatch_civic_knobs(
    monkeypatch: pytest.MonkeyPatch,
    *,
    min_size: int | None = None,
    readiness_threshold: int | None = None,
    active_lenses: tuple[str, ...] | None = None,
    primary_lens: str | None = None,
    geo_scope: tuple[str, str] | None | object = ...,
) -> None:
    """Return real active-pack civic with selected fields replaced for one test."""
    original = config_schema.civic_clustering_from_active_node

    def _patched(*, schema_id: str, schema_version: str) -> CivicClusteringBlock:
        civic = original(schema_id=schema_id, schema_version=schema_version)
        updates: dict[str, object] = {}
        if min_size is not None:
            updates["min_size"] = min_size
            updates["min_size_by_lens"] = {}
        if readiness_threshold is not None:
            updates["readiness_threshold"] = readiness_threshold
        if active_lenses is not None:
            updates["active_lenses"] = active_lenses
        if primary_lens is not None:
            updates["primary_lens"] = primary_lens
        if geo_scope is not ...:
            updates["geo_scope"] = geo_scope
        return replace(civic, **updates) if updates else civic

    monkeypatch.setattr(config_schema, "civic_clustering_from_active_node", _patched)
