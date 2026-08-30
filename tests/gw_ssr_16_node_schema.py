"""Shared NODE_SCHEMA_* pytest helper (GW-SSR-16)."""

from __future__ import annotations

from collections.abc import Mapping

import pytest

NODE_SCHEMA_ID_ENV = "NODE_SCHEMA_ID"
NODE_SCHEMA_VERSION_ENV = "NODE_SCHEMA_VERSION"
DEFAULT_TEST_NODE_SCHEMA_ID = "tallinn_civic"
DEFAULT_TEST_NODE_SCHEMA_VERSION = "v1"


def node_schema_env_pair(
    *,
    schema_id: str = DEFAULT_TEST_NODE_SCHEMA_ID,
    schema_version: str = DEFAULT_TEST_NODE_SCHEMA_VERSION,
) -> dict[str, str]:
    return {
        NODE_SCHEMA_ID_ENV: schema_id,
        NODE_SCHEMA_VERSION_ENV: schema_version,
    }


def with_node_schema(env: Mapping[str, str]) -> dict[str, str]:
    """Copy env and setdefault both required NODE_SCHEMA_* keys."""
    merged = dict(env)
    merged.setdefault(NODE_SCHEMA_ID_ENV, DEFAULT_TEST_NODE_SCHEMA_ID)
    merged.setdefault(NODE_SCHEMA_VERSION_ENV, DEFAULT_TEST_NODE_SCHEMA_VERSION)
    return merged


def monkeypatch_node_schema(
    monkeypatch: pytest.MonkeyPatch,
    *,
    schema_id: str = DEFAULT_TEST_NODE_SCHEMA_ID,
    schema_version: str = DEFAULT_TEST_NODE_SCHEMA_VERSION,
) -> None:
    monkeypatch.setenv(NODE_SCHEMA_ID_ENV, schema_id)
    monkeypatch.setenv(NODE_SCHEMA_VERSION_ENV, schema_version)
