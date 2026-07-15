from __future__ import annotations

import inspect

import pytest  # pyright: ignore[reportMissingImports]

from core.config import ConfigError, DeploymentProfile, ENV_SCHEMA, load_config_from_env
from core.config import schema as config_schema
from core.infrastructure.providers import provide_app_config, provide_service_factory
from core.infrastructure.repositories import InMemoryStoryRepository


def test_db_backend_env_default_matches_schema() -> None:
    """GAP-11 §5.5: omitted DB_BACKEND must stay aligned with ENV_SCHEMA default (in_memory)."""
    db_specs = [s for s in ENV_SCHEMA if s.name == "DB_BACKEND"]
    assert len(db_specs) == 1
    assert db_specs[0].default == "in_memory"
    env = {"APP_PROFILE": "demo", "API_BASE_URL": "https://demo.example/api"}
    assert "DB_BACKEND" not in env
    config = load_config_from_env(env)
    assert config.db_backend == "in_memory"
    assert config.db_enabled is False


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
    assert config.log_debug_dir is None
    assert config.log_format == "text"
    assert config.db_backend == "in_memory"
    assert config.db_enabled is False
    assert config.database_url is None
    assert config.cluster_min_size == 5
    assert config.cluster_readiness_threshold == 60
    assert config.cluster_active_lenses
    assert config.cluster_active_lenses == (
        "composite_primary_micro",
        "civic_domain_micro",
        "failure_pattern_micro",
        "civic_weight_systemic",
        "desired_outcome_local",
        "affected_group_local",
        "geographic_district_micro",
        "service_object_micro",
        "deep_need_local",
        "ecosystem_signal_systemic",
    )
    assert "topic_micro" not in config.cluster_active_lenses
    assert config.cluster_primary_lens == "composite_primary_micro"
    assert config.cluster_min_size_by_lens["composite_primary_micro"] == 8
    assert config.cluster_signal_source == "canonical"
    assert config.cluster_geo_filter == "country"
    assert config.cluster_geo_scope is None
    assert config.cluster_tie_breaker == "alpha"
    assert config.cluster_type_resolution == "canonical_priority"
    assert config.cluster_id_algorithm == "sha256"
    assert config.cluster_cron_interval_s == 60
    assert config.cluster_cron_enabled is True


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


def test_cluster_tie_breaker_non_alpha_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid CLUSTER_TIE_BREAKER"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_TIE_BREAKER": "lexical",
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


def test_log_format_override() -> None:
    config = load_config_from_env(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
            "LOG_FORMAT": "json",
        }
    )
    assert config.log_format == "json"


def test_invalid_log_format_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid LOG_FORMAT"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "LOG_FORMAT": "xml",
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
    assert "LOG_DEBUG_DIR" in names
    assert "LOG_FORMAT" in names
    assert "SERVICE_API_TOKEN" in names
    assert "DB_BACKEND" in names
    assert "DATABASE_URL" in names
    assert "SUPABASE_URL" in names
    assert "SUPABASE_SERVICE_ROLE" in names
    assert "CLUSTER_MIN_SIZE" in names
    assert "CLUSTER_READINESS_THRESHOLD" in names
    assert "CLUSTER_ACTIVE_LENSES" in names
    assert "CLUSTER_PRIMARY_LENS" in names
    assert "CLUSTER_SIGNAL_SOURCE" in names
    assert "CLUSTER_ID_ALGORITHM" in names
    assert "CLUSTER_GEO_FILTER" in names
    assert "CLUSTER_TIE_BREAKER" in names
    assert "CLUSTER_TYPE_RESOLUTION" in names
    assert "CLUSTER_CRON_INTERVAL_S" in names
    assert "CLUSTER_CRON_ENABLED" in names


def test_invalid_cluster_active_lenses_raises() -> None:
    with pytest.raises(ConfigError, match="Invalid CLUSTER_ACTIVE_LENSES values"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_ACTIVE_LENSES": "civic_domain_micro,invalid_lens",
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
            }
        )


def test_in_memory_backend_rejects_supabase_env_with_operator_hint() -> None:
    with pytest.raises(ConfigError, match="uvicorn"):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "DB_BACKEND": "in_memory",
                "SUPABASE_URL": "https://example.supabase.co",
                "SUPABASE_SERVICE_ROLE": "secret",
            }
        )


def test_in_memory_backend_rejects_database_url() -> None:
    with pytest.raises(ConfigError, match="DB_BACKEND is 'in_memory'"):
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


def test_cluster_primary_lens_must_appear_in_cluster_active_lenses() -> None:
    """H4: primary lens must be a member of CLUSTER_ACTIVE_LENSES (fail-fast contract)."""
    with pytest.raises(
        ConfigError,
        match=r"CLUSTER_PRIMARY_LENS=.*must appear in CLUSTER_ACTIVE_LENSES=",
    ):
        load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.example/api",
                "CLUSTER_ACTIVE_LENSES": "civic_domain_micro,failure_pattern_micro,civic_weight_systemic",
                "CLUSTER_PRIMARY_LENS": "geographic_district_micro",
            }
        )


def test_provide_app_config_merges_dotenv_when_env_is_none(tmp_path, monkeypatch) -> None:
    """GAP-02: cwd `.env` fills gaps; keys already in os.environ are not overridden."""
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("LOG_LEVEL=ERROR\n", encoding="utf-8")
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    cfg = provide_app_config(None)
    assert cfg.log_level == "ERROR"


def test_provide_app_config_os_environ_overrides_dotenv(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("LOG_LEVEL=ERROR\n", encoding="utf-8")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    cfg = provide_app_config(None)
    assert cfg.log_level == "DEBUG"


def test_db_backend_defaults_to_in_memory_via_provide_app_config() -> None:
    """REQ-39 I-01: empty explicit env → in_memory backend."""
    config = provide_app_config(env={})
    assert config.db_backend == "in_memory"
    assert config.db_enabled is False


def test_db_backend_supabase_from_env() -> None:
    """REQ-39 I-02: DB_BACKEND=supabase with contract env keys."""
    config = provide_app_config(
        env={
            "DB_BACKEND": "supabase",
            "SUPABASE_URL": "https://example.supabase.co",
            "SUPABASE_SERVICE_ROLE": "service-role-secret",
        }
    )
    assert config.db_backend == "supabase"
    assert config.db_enabled is True


def test_factory_in_memory_uses_inmemory_repos() -> None:
    """REQ-39 I-03: provide_service_factory wires InMemoryStoryRepository."""
    config = provide_app_config(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
            "DB_BACKEND": "in_memory",
        }
    )
    factory = provide_service_factory(config)
    service = factory.get_story_intake_service()
    assert isinstance(service.repository, InMemoryStoryRepository)


def test_in_memory_default_is_explicit_in_config_schema() -> None:
    """REQ-39 I-04: default backend literal visible in config schema source."""
    src = inspect.getsource(config_schema)
    assert '"in_memory"' in src or "'in_memory'" in src


def test_provide_app_config_explicit_env_does_not_read_dotenv(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text("LOG_LEVEL=ERROR\n", encoding="utf-8")
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    cfg = provide_app_config(
        {
            "APP_PROFILE": "demo",
            "API_BASE_URL": "https://demo.example/api",
        }
    )
    assert cfg.log_level == "INFO"

