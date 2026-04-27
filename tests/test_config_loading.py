from __future__ import annotations

import pytest  # pyright: ignore[reportMissingImports]

from core.config import ConfigError, DeploymentProfile, ENV_SCHEMA, load_config_from_env


def test_load_config_demo_defaults() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
        }
    )
    assert config.profile is DeploymentProfile.DEMO
    assert config.api_base_url == "https://demo.example/api"
    assert config.request_timeout_s == 15
    assert config.flags.wallet_adapter is False
    assert config.flags.blockchain_adapter is False
    assert config.flags.tokenization_pipeline is False
    assert config.log_level == "INFO"
    assert config.db_backend == "in_memory"
    assert config.db_enabled is False
    assert config.database_url is None
    assert config.cluster_min_size == 8
    assert config.cluster_readiness_threshold == 70
    assert config.cluster_active_lenses
    assert config.cluster_geo_filter == "any"
    assert config.cluster_tie_breaker == "lexical"
    assert config.cluster_type_resolution == "canonical_priority"


def test_load_config_pilot_defaults() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "pilot",
            "API_BASE_URL": "https://pilot.example/api",
            "SERVICE_API_TOKEN": "pilot-secret",
        }
    )
    assert config.profile is DeploymentProfile.PILOT
    assert config.flags.wallet_adapter is True
    assert config.flags.blockchain_adapter is True
    assert config.flags.tokenization_pipeline is True


def test_load_config_feature_flag_override() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "pilot",
            "API_BASE_URL": "https://pilot.example/api",
            "SERVICE_API_TOKEN": "pilot-secret",
            "FF_WALLET_ADAPTER": "false",
            "FF_BLOCKCHAIN_ADAPTER": "0",
            "FF_TOKENIZATION_PIPELINE": "no",
        }
    )
    assert config.flags.wallet_adapter is False
    assert config.flags.blockchain_adapter is False
    assert config.flags.tokenization_pipeline is False


def test_missing_required_api_base_url_raises() -> None:
    with pytest.raises(ConfigError, match="Missing required environment variable: API_BASE_URL"):
        load_config_from_env({"APP_PROFILE": "demo"})


def test_invalid_profile_raises() -> None:
    with pytest.raises(ConfigError, match="Unsupported APP_PROFILE"):
        load_config_from_env(
            {
                "APP_PROFILE": "dev",
                "API_BASE_URL": "https://demo.example/api",
            }
        )


def test_invalid_timeout_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid REQUEST_TIMEOUT_S"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "REQUEST_TIMEOUT_S": "abc",
            }
        )


def test_api_base_url_must_be_http_or_https() -> None:
    with pytest.raises(ConfigError, match="must start with http:// or https://"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "ftp://example/api",
            }
        )


def test_log_level_override() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
            "LOG_LEVEL": "warning",
        }
    )
    assert config.log_level == "WARNING"


def test_invalid_log_level_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid LOG_LEVEL"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "LOG_LEVEL": "verbose",
            }
        )


def test_env_schema_contains_required_fields() -> None:
    names = {field.name for field in ENV_SCHEMA}
    assert "APP_PROFILE" in names
    assert "API_BASE_URL" in names
    assert "REQUEST_TIMEOUT_S" in names
    assert "FF_WALLET_ADAPTER" in names
    assert "FF_BLOCKCHAIN_ADAPTER" in names
    assert "FF_TOKENIZATION_PIPELINE" in names
    assert "LOG_LEVEL" in names
    assert "SERVICE_API_TOKEN" in names
    assert "DB_BACKEND" in names
    assert "DATABASE_URL" in names
    assert "SUPABASE_URL" in names
    assert "SUPABASE_SERVICE_ROLE" in names
    assert "CLUSTER_MIN_SIZE" in names
    assert "CLUSTER_READINESS_THRESHOLD" in names
    assert "CLUSTER_ACTIVE_LENSES" in names
    assert "CLUSTER_GEO_FILTER" in names
    assert "CLUSTER_TIE_BREAKER" in names
    assert "CLUSTER_TYPE_RESOLUTION" in names


def test_invalid_cluster_active_lenses_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid CLUSTER_ACTIVE_LENSES values"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_ACTIVE_LENSES": "topic_micro,invalid_lens",
            }
        )


def test_pilot_profile_requires_service_api_token() -> None:
    with pytest.raises(ConfigError, match="SERVICE_API_TOKEN is required"):
        load_config_from_env(
            {
                "APP_PROFILE": "pilot",
                "API_BASE_URL": "https://pilot.example/api",
            }
        )


def test_sqlite_backend_requires_sqlite_database_url() -> None:
    with pytest.raises(ConfigError, match="DATABASE_URL is required for DB_BACKEND='sqlite'"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "DB_BACKEND": "sqlite",
            }
        )


def test_supabase_backend_requires_supabase_contract() -> None:
    with pytest.raises(ConfigError, match="SUPABASE_URL is required"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "DB_BACKEND": "supabase",
                "DATABASE_URL": "postgresql://postgres:pass@localhost:5432/postgres",
            }
        )


def test_in_memory_backend_rejects_database_url() -> None:
    with pytest.raises(ConfigError, match="DB_BACKEND='in_memory' does not allow"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "DB_BACKEND": "in_memory",
                "DATABASE_URL": "sqlite:////tmp/demo.sqlite3",
            }
        )


def test_sqlite_backend_rejects_supabase_keys() -> None:
    with pytest.raises(
        ConfigError, match="SUPABASE_URL/SUPABASE_SERVICE_ROLE are not allowed"
    ):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "DB_BACKEND": "sqlite",
                "DATABASE_URL": "sqlite:////tmp/demo.sqlite3",
                "SUPABASE_URL": "https://example.supabase.co",
            }
        )

