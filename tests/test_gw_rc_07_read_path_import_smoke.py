"""STORY-GW-RC-07 T07: deploy/packaging drift guard for lazy read-path imports."""

from __future__ import annotations

import importlib
import inspect

import pytest

from core.infrastructure.db_supabase import SupabaseIssueProjectionStore

# Modules lazily imported on hosted read path (db_supabase list/get projection).
# Missing from deploy artifact → runtime ImportError → INTERNAL_ERROR on first list.
_READ_PATH_LAZY_MODULES: tuple[str, ...] = (
    "core.projection.columnar_storage",
    "core.projection.read_filters",
)

_REQUIRED_SYMBOLS: dict[str, tuple[str, ...]] = {
    "core.projection.columnar_storage": (
        "COLUMNAR_ROW_SELECT",
        "assemble_public_issue_from_storage_row",
        "DOGE_ISSUES_COLUMNAR_READINESS_COLUMNS",
        "payload_to_storage_fields",
    ),
    "core.projection.read_filters": (
        "filter_projection_rows",
        "merge_projection_columns",
    ),
}


@pytest.mark.parametrize("module_name", _READ_PATH_LAZY_MODULES)
def test_read_path_lazy_import_module_present(module_name: str) -> None:
    """Packaging guard: lazy-imported read-path modules must exist in artifact."""
    module = importlib.import_module(module_name)
    for symbol in _REQUIRED_SYMBOLS[module_name]:
        assert hasattr(module, symbol), f"{module_name} missing {symbol}"


def test_list_projections_uses_documented_lazy_imports() -> None:
    """Contract: list_projections/get_projection keep lazy imports we guard."""
    list_src = inspect.getsource(SupabaseIssueProjectionStore.list_projections)
    get_src = inspect.getsource(SupabaseIssueProjectionStore.get_projection)
    for fragment in (
        "from core.projection.columnar_storage import",
        "from core.projection.read_filters import",
    ):
        assert fragment in list_src or fragment in get_src
