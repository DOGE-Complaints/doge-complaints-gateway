"""GW-SSR-16: NODE_SCHEMA_ID / NODE_SCHEMA_VERSION required + boot resolve_pack."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from core.config import ConfigError, ENV_SCHEMA, load_config_from_env
from core.config.schema import AppConfig
from gw_ssr_16_node_schema import (
    DEFAULT_TEST_NODE_SCHEMA_ID,
    DEFAULT_TEST_NODE_SCHEMA_VERSION,
    NODE_SCHEMA_ID_ENV,
    NODE_SCHEMA_VERSION_ENV,
    monkeypatch_node_schema,
    with_node_schema,
)

_BASE = {
    "APP_PROFILE": "demo",
    "API_BASE_URL": "https://demo.example/api",
}


def test_env_specs_both_required_no_default() -> None:
    by_name = {spec.name: spec for spec in ENV_SCHEMA}
    assert NODE_SCHEMA_ID_ENV in by_name
    assert NODE_SCHEMA_VERSION_ENV in by_name
    assert by_name[NODE_SCHEMA_ID_ENV].required is True
    assert by_name[NODE_SCHEMA_ID_ENV].default is None
    assert by_name[NODE_SCHEMA_VERSION_ENV].required is True
    assert by_name[NODE_SCHEMA_VERSION_ENV].default is None
    assert "SCHEMA_PACKS_ROOT" not in by_name
    assert "node_schema_id" in AppConfig.__dataclass_fields__
    assert "node_schema_version" in AppConfig.__dataclass_fields__
    assert "schema_packs_root" not in AppConfig.__dataclass_fields__


def test_missing_node_schema_id_raises_config_error() -> None:
    env = dict(_BASE)
    env[NODE_SCHEMA_VERSION_ENV] = DEFAULT_TEST_NODE_SCHEMA_VERSION
    with pytest.raises(ConfigError, match="Missing required environment variable: NODE_SCHEMA_ID"):
        load_config_from_env(env)


def test_missing_node_schema_version_raises_config_error() -> None:
    env = dict(_BASE)
    env[NODE_SCHEMA_ID_ENV] = DEFAULT_TEST_NODE_SCHEMA_ID
    with pytest.raises(
        ConfigError, match="Missing required environment variable: NODE_SCHEMA_VERSION"
    ):
        load_config_from_env(env)


def test_empty_node_schema_id_raises_config_error() -> None:
    env = with_node_schema(_BASE)
    env[NODE_SCHEMA_ID_ENV] = "   "
    with pytest.raises(ConfigError, match="Missing required environment variable: NODE_SCHEMA_ID"):
        load_config_from_env(env)


def test_existing_pack_loads() -> None:
    config = load_config_from_env(with_node_schema(_BASE))
    assert config.node_schema_id == DEFAULT_TEST_NODE_SCHEMA_ID
    assert config.node_schema_version == DEFAULT_TEST_NODE_SCHEMA_VERSION


def test_unknown_schema_id_raises_config_error() -> None:
    env = with_node_schema(_BASE)
    env[NODE_SCHEMA_ID_ENV] = "no_such_pack"
    with pytest.raises(ConfigError, match="does not resolve to a pack catalog"):
        load_config_from_env(env)


def test_missing_version_dir_raises_config_error() -> None:
    env = with_node_schema(_BASE)
    env[NODE_SCHEMA_VERSION_ENV] = "v9-missing"
    with pytest.raises(ConfigError, match="does not resolve to a pack catalog"):
        load_config_from_env(env)


def test_lifespan_logs_active_pair(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch_node_schema(monkeypatch)
    from core.api.asgi_app import _clear_api_dependencies_cache, app

    _clear_api_dependencies_cache()
    with TestClient(app):
        pass
    captured = capsys.readouterr()
    text = f"{captured.out}\n{captured.err}"
    assert "startup.config" in text
    assert "node_schema_id=tallinn_civic" in text
    assert "node_schema_version=v1" in text
    assert "structured_payload" not in text
