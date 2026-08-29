"""GW-SSR-09 T02: omit-probe cuts binding only when probe is false.

``stories_binding_columns_ready`` caches ``_stories_binding_columns_ready``.
Live process restart after hosted apply = operator, not overnight DoD (G9).
Civic ``required_columns_ready`` / ``REQUIRED_READINESS_TABLES`` stay without
binding names.
"""

from __future__ import annotations

import inspect
import re

from core.infrastructure.db_supabase import (
    REQUIRED_READINESS_TABLES,
    _STORY_SELECT_FIELDS,
    _story_select_fields_for_db,
    SupabaseDatabase,
)

_BINDING = frozenset(SupabaseDatabase._STORIES_BINDING_COLUMNS)


class _FixedProbe:
    """Duck-typed probe for ``_story_select_fields_for_db`` (no HTTP)."""

    def __init__(self, *, geo_ready: bool, binding_ready: bool) -> None:
        self._geo_ready = geo_ready
        self._binding_ready = binding_ready

    def stories_geo_admin_columns_ready(self) -> bool:
        return self._geo_ready

    def stories_binding_columns_ready(self) -> bool:
        return self._binding_ready


def _stories_required_names() -> set[str]:
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    start = source.index('"stories":')
    chunk = source[start : source.index("},", start)]
    return set(re.findall(r'"([a-z_]+)"', chunk))


def test_omit_probe_cuts_binding_only_when_probe_false() -> None:
    omitted = _story_select_fields_for_db(_FixedProbe(geo_ready=True, binding_ready=False))  # type: ignore[arg-type]
    omitted_parts = {part.strip() for part in omitted.split(",") if part.strip()}
    assert _BINDING.isdisjoint(omitted_parts)

    ready = _story_select_fields_for_db(_FixedProbe(geo_ready=True, binding_ready=True))  # type: ignore[arg-type]
    ready_parts = {part.strip() for part in ready.split(",") if part.strip()}
    assert _BINDING.issubset(ready_parts)
    assert ready == _STORY_SELECT_FIELDS


def test_required_columns_ready_stories_set_excludes_six_binding_names() -> None:
    stories = _stories_required_names()
    assert stories.isdisjoint(_BINDING)
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    for name in _BINDING:
        assert name not in source


def test_civic_ready_path_does_not_require_binding() -> None:
    assert "story_dimensions" not in REQUIRED_READINESS_TABLES
    source = inspect.getsource(SupabaseDatabase.required_columns_ready)
    assert "schema_id" not in source
    assert "bound_schema_version" not in source
    assert "structured_payload" not in source


def test_binding_probe_cache_documented_in_source() -> None:
    """Cache lives on the instance; live restart after apply is operator (G9)."""
    source = inspect.getsource(SupabaseDatabase.stories_binding_columns_ready)
    assert "_stories_binding_columns_ready" in source
    assert "cached" in source
