from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from os import environ
from typing import Mapping


class ConfigError(ValueError):
    """Raised when environment configuration is invalid."""


class DeploymentProfile(str, Enum):
    DEMO = "demo"
    PILOT = "pilot"


@dataclass(frozen=True)
class EnvSpec:
    name: str
    required: bool
    default: str | None
    description: str


@dataclass(frozen=True)
class FeatureFlags:
    wallet_adapter: bool
    blockchain_adapter: bool
    tokenization_pipeline: bool


@dataclass(frozen=True)
class AppConfig:
    profile: DeploymentProfile
    api_base_url: str
    request_timeout_s: int
    flags: FeatureFlags
    log_level: str
    db_backend: str
    db_enabled: bool
    database_url: str | None
    supabase_url: str | None
    supabase_service_role: str | None
    cluster_min_size: int
    cluster_readiness_threshold: int
    cluster_active_lenses: tuple[str, ...]
    cluster_geo_filter: str
    cluster_tie_breaker: str
    cluster_type_resolution: str


ENV_SCHEMA: tuple[EnvSpec, ...] = (
    EnvSpec(
        name="APP_PROFILE",
        required=False,
        default=DeploymentProfile.DEMO.value,
        description="Deployment profile: demo or pilot.",
    ),
    EnvSpec(
        name="API_BASE_URL",
        required=True,
        default=None,
        description="Base URL for API runtime.",
    ),
    EnvSpec(
        name="REQUEST_TIMEOUT_S",
        required=False,
        default="15",
        description="Default outbound request timeout in seconds.",
    ),
    EnvSpec(
        name="FF_WALLET_ADAPTER",
        required=False,
        default=None,
        description="Feature flag override for wallet adapter.",
    ),
    EnvSpec(
        name="FF_BLOCKCHAIN_ADAPTER",
        required=False,
        default=None,
        description="Feature flag override for blockchain adapter.",
    ),
    EnvSpec(
        name="FF_TOKENIZATION_PIPELINE",
        required=False,
        default=None,
        description="Feature flag override for tokenization pipeline.",
    ),
    EnvSpec(
        name="LOG_LEVEL",
        required=False,
        default="INFO",
        description="Application log level: DEBUG, INFO, WARNING, ERROR, CRITICAL.",
    ),
    EnvSpec(
        name="SERVICE_API_TOKEN",
        required=False,
        default=None,
        description=(
            "Service-to-service API token for protected operations. "
            "Required for pilot profile strict auth mode."
        ),
    ),
    EnvSpec(
        name="DB_BACKEND",
        required=False,
        default="in_memory",
        description="Database backend mode: in_memory, sqlite, supabase.",
    ),
    EnvSpec(
        name="DATABASE_URL",
        required=False,
        default=None,
        description="Database URL for sqlite/postgresql runtime persistence.",
    ),
    EnvSpec(
        name="SUPABASE_URL",
        required=False,
        default=None,
        description="Supabase project URL for runtime and readiness checks.",
    ),
    EnvSpec(
        name="SUPABASE_SERVICE_ROLE",
        required=False,
        default=None,
        description="Supabase service role key for server-side access.",
    ),
    EnvSpec(
        name="CLUSTER_MIN_SIZE",
        required=False,
        default="8",
        description="Minimum number of stories for cluster-level promotion eligibility.",
    ),
    EnvSpec(
        name="CLUSTER_READINESS_THRESHOLD",
        required=False,
        default="70",
        description="Readiness threshold used by promotion gates.",
    ),
    EnvSpec(
        name="CLUSTER_ACTIVE_LENSES",
        required=False,
        default="topic_micro,need_local,failure_systemic,failure_micro,repeatability_local,relevance_systemic",
        description="Comma-separated enabled cluster lenses.",
    ),
    EnvSpec(
        name="CLUSTER_GEO_FILTER",
        required=False,
        default="any",
        description="Geo filtering mode for clustering.",
    ),
    EnvSpec(
        name="CLUSTER_TIE_BREAKER",
        required=False,
        default="lexical",
        description="Tie-breaker strategy for equal-score candidates.",
    ),
    EnvSpec(
        name="CLUSTER_TYPE_RESOLUTION",
        required=False,
        default="canonical_priority",
        description="Issue type resolution strategy for clustered stories.",
    ),
)


def _get_value(env: Mapping[str, str], name: str) -> str | None:
    value = env.get(name)
    if value is None:
        return None
    trimmed = value.strip()
    return trimmed if trimmed else None


def _parse_profile(value: str | None) -> DeploymentProfile:
    raw_value = value or DeploymentProfile.DEMO.value
    normalized = raw_value.strip().lower()
    try:
        return DeploymentProfile(normalized)
    except ValueError as exc:
        raise ConfigError(
            f"Unsupported APP_PROFILE={raw_value!r}. Expected one of: demo, pilot."
        ) from exc


_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


def _validate_http_url(url: str, *, env_name: str) -> str:
    trimmed = url.strip()
    if not trimmed:
        raise ConfigError(f"{env_name} must be a non-empty URL.")
    lower = trimmed.lower()
    if not (lower.startswith("http://") or lower.startswith("https://")):
        raise ConfigError(
            f"{env_name} must start with http:// or https://, got {url!r}."
        )
    return trimmed


def _parse_log_level(raw: str | None) -> str:
    if raw is None:
        return "INFO"
    normalized = raw.strip().upper()
    if normalized not in _LOG_LEVELS:
        raise ConfigError(
            f"Invalid LOG_LEVEL={raw!r}. Expected one of: {sorted(_LOG_LEVELS)}."
        )
    return normalized


def _parse_bool(value: str, *, env_name: str) -> bool:
    normalized = value.strip().lower()
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    if normalized in truthy:
        return True
    if normalized in falsy:
        return False
    raise ConfigError(
        f"Invalid boolean for {env_name}={value!r}. Use one of: {sorted(truthy | falsy)}."
    )


def _parse_positive_int(value: str, *, env_name: str) -> int:
    try:
        parsed = int(value.strip())
    except ValueError as exc:
        raise ConfigError(f"Invalid {env_name}={value!r}. Expected integer.") from exc
    if parsed <= 0:
        raise ConfigError(f"Invalid {env_name}={parsed}. Must be positive.")
    return parsed


def _parse_cluster_lenses(raw: str) -> tuple[str, ...]:
    allowed = {
        "topic_micro",
        "need_local",
        "failure_systemic",
        "failure_micro",
        "repeatability_local",
        "relevance_systemic",
    }
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values:
        raise ConfigError("CLUSTER_ACTIVE_LENSES must contain at least one lens.")
    invalid = [item for item in values if item not in allowed]
    if invalid:
        raise ConfigError(
            "Invalid CLUSTER_ACTIVE_LENSES values: "
            f"{invalid}. Allowed: {sorted(allowed)}."
        )
    return tuple(dict.fromkeys(values))


def _required_spec(name: str) -> EnvSpec:
    for spec in ENV_SCHEMA:
        if spec.name == name:
            return spec
    raise RuntimeError(f"Env spec for {name} not found.")


def _require_value(env: Mapping[str, str], *, name: str) -> str:
    spec = _required_spec(name)
    value = _get_value(env, name)
    if value is None:
        if spec.required and spec.default is None:
            raise ConfigError(f"Missing required environment variable: {name}.")
        if spec.default is None:
            raise ConfigError(f"Missing environment variable with no default: {name}.")
        return spec.default
    return value


def _profile_defaults(profile: DeploymentProfile) -> FeatureFlags:
    if profile is DeploymentProfile.DEMO:
        return FeatureFlags(
            wallet_adapter=False,
            blockchain_adapter=False,
            tokenization_pipeline=False,
        )
    return FeatureFlags(
        wallet_adapter=True,
        blockchain_adapter=True,
        tokenization_pipeline=True,
    )


def load_config_from_env(env: Mapping[str, str] | None = None) -> AppConfig:
    source = env or environ
    profile = _parse_profile(_get_value(source, "APP_PROFILE"))
    api_base_url_raw = _require_value(source, name="API_BASE_URL")
    api_base_url = _validate_http_url(api_base_url_raw, env_name="API_BASE_URL")

    timeout_raw = _require_value(source, name="REQUEST_TIMEOUT_S")
    try:
        request_timeout_s = int(timeout_raw)
    except ValueError as exc:
        raise ConfigError(
            f"Invalid REQUEST_TIMEOUT_S={timeout_raw!r}. Expected integer."
        ) from exc
    if request_timeout_s <= 0:
        raise ConfigError(
            f"Invalid REQUEST_TIMEOUT_S={request_timeout_s}. Must be positive."
        )

    defaults = _profile_defaults(profile)

    wallet_raw = _get_value(source, "FF_WALLET_ADAPTER")
    blockchain_raw = _get_value(source, "FF_BLOCKCHAIN_ADAPTER")
    tokenization_raw = _get_value(source, "FF_TOKENIZATION_PIPELINE")

    flags = FeatureFlags(
        wallet_adapter=defaults.wallet_adapter
        if wallet_raw is None
        else _parse_bool(wallet_raw, env_name="FF_WALLET_ADAPTER"),
        blockchain_adapter=defaults.blockchain_adapter
        if blockchain_raw is None
        else _parse_bool(blockchain_raw, env_name="FF_BLOCKCHAIN_ADAPTER"),
        tokenization_pipeline=defaults.tokenization_pipeline
        if tokenization_raw is None
        else _parse_bool(tokenization_raw, env_name="FF_TOKENIZATION_PIPELINE"),
    )

    log_level = _parse_log_level(_get_value(source, "LOG_LEVEL"))
    service_api_token = _get_value(source, "SERVICE_API_TOKEN")
    if profile is DeploymentProfile.PILOT and service_api_token is None:
        raise ConfigError(
            "SERVICE_API_TOKEN is required for APP_PROFILE='pilot' strict auth mode."
        )

    db_backend_raw = _require_value(source, name="DB_BACKEND")
    db_backend = db_backend_raw.strip().lower()
    if db_backend not in {"in_memory", "sqlite", "supabase"}:
        raise ConfigError(
            f"Unsupported DB_BACKEND={db_backend_raw!r}. Expected in_memory/sqlite/supabase."
        )
    database_url = _get_value(source, "DATABASE_URL")
    supabase_url = _get_value(source, "SUPABASE_URL")
    supabase_service_role = _get_value(source, "SUPABASE_SERVICE_ROLE")
    if db_backend == "in_memory":
        if database_url is not None or supabase_url is not None or supabase_service_role is not None:
            raise ConfigError(
                "DB_BACKEND='in_memory' does not allow DATABASE_URL/SUPABASE_URL/SUPABASE_SERVICE_ROLE."
            )
    if db_backend == "sqlite":
        if database_url is None or not database_url.startswith("sqlite:///"):
            raise ConfigError(
                "DATABASE_URL is required for DB_BACKEND='sqlite' and must start with sqlite:///."
            )
        if supabase_url is not None or supabase_service_role is not None:
            raise ConfigError(
                "SUPABASE_URL/SUPABASE_SERVICE_ROLE are not allowed for DB_BACKEND='sqlite'."
            )
    if db_backend == "supabase":
        if database_url is None or not (
            database_url.startswith("postgresql://")
            or database_url.startswith("postgres://")
        ):
            raise ConfigError(
                "DATABASE_URL is required for DB_BACKEND='supabase' and must be postgresql://."
            )
        if supabase_url is None:
            raise ConfigError(
                "SUPABASE_URL is required for DB_BACKEND='supabase'."
            )
        if supabase_service_role is None:
            raise ConfigError(
                "SUPABASE_SERVICE_ROLE is required for DB_BACKEND='supabase'."
            )
    db_enabled = db_backend != "in_memory"
    cluster_min_size = _parse_positive_int(
        _require_value(source, name="CLUSTER_MIN_SIZE"),
        env_name="CLUSTER_MIN_SIZE",
    )
    cluster_readiness_threshold = _parse_positive_int(
        _require_value(source, name="CLUSTER_READINESS_THRESHOLD"),
        env_name="CLUSTER_READINESS_THRESHOLD",
    )
    if cluster_readiness_threshold > 100:
        raise ConfigError(
            "Invalid CLUSTER_READINESS_THRESHOLD. Expected value in range 1..100."
        )
    cluster_active_lenses = _parse_cluster_lenses(
        _require_value(source, name="CLUSTER_ACTIVE_LENSES")
    )
    cluster_geo_filter = _require_value(source, name="CLUSTER_GEO_FILTER").strip().lower()
    cluster_tie_breaker = _require_value(source, name="CLUSTER_TIE_BREAKER").strip().lower()
    cluster_type_resolution = _require_value(
        source, name="CLUSTER_TYPE_RESOLUTION"
    ).strip().lower()

    return AppConfig(
        profile=profile,
        api_base_url=api_base_url,
        request_timeout_s=request_timeout_s,
        flags=flags,
        log_level=log_level,
        db_backend=db_backend,
        db_enabled=db_enabled,
        database_url=database_url,
        supabase_url=supabase_url,
        supabase_service_role=supabase_service_role,
        cluster_min_size=cluster_min_size,
        cluster_readiness_threshold=cluster_readiness_threshold,
        cluster_active_lenses=cluster_active_lenses,
        cluster_geo_filter=cluster_geo_filter,
        cluster_tie_breaker=cluster_tie_breaker,
        cluster_type_resolution=cluster_type_resolution,
    )

