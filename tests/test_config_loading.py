from __future__ import annotations

import pytest

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


def test_load_config_pilot_defaults() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "pilot",
            "API_BASE_URL": "https://pilot.example/api",
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

