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
    log_debug_dir: str | None
    log_format: str
    db_backend: str
    db_enabled: bool
    database_url: str | None
    supabase_url: str | None
    supabase_service_role: str | None
    cluster_min_size: int
    cluster_min_size_by_lens: dict[str, int]
    cluster_readiness_threshold: int
    cluster_active_lenses: tuple[str, ...]
    cluster_primary_lens: str
    cluster_signal_source: str
    cluster_id_algorithm: str
    cluster_geo_filter: str
    cluster_geo_scope: tuple[str, str] | None
    cluster_tie_breaker: str
    cluster_type_resolution: str
    cluster_cron_interval_s: int
    cluster_cron_enabled: bool
    identity_base_url: str | None
    spa_verify_base_url: str | None
    story_draft_ttl_seconds: int
    node_schema_id: str
    node_schema_version: str


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
        name="LOG_DEBUG_DIR",
        required=False,
        default=None,
        description="Directory for per-story DEBUG log files.",
    ),
    EnvSpec(
        name="LOG_FORMAT",
        required=False,
        default="text",
        description="Stdout log format: text | json.",
    ),
    EnvSpec(
        name="SERVICE_API_TOKEN",
        required=False,
        default=None,
        description=(
            "Service-to-service API token for protected operations. "
            "Required for pilot profile strict auth mode. "
            "Public-content write routes (POST /story-drafts, POST /node/issues) "
            "reject with 401 when missing or invalid even if this env is unset (GW-GAUTH-01)."
        ),
    ),
    EnvSpec(
        name="IDENTITY_BASE_URL",
        required=False,
        default=None,
        description=(
            "Identity service base URL for browser /me forward (GET {base}/me, GW-DRAFT-02)."
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
        default="5",
        description="Minimum number of stories for cluster-level promotion eligibility (global fallback).",
    ),
    EnvSpec(
        name="CLUSTER_MIN_SIZE_BY_LENS",
        required=False,
        default=(
            "composite_primary_micro=8,service_object_micro=3,deep_need_local=3,"
            "ecosystem_signal_systemic=3"
        ),
        description=(
            "Per-lens min story counts for promotion (lens_id=count pairs, comma-separated)."
        ),
    ),
    EnvSpec(
        name="CLUSTER_READINESS_THRESHOLD",
        required=False,
        default="60",
        description="Readiness threshold used by promotion gates (aligned with L3 readiness formula for small clusters).",
    ),
    EnvSpec(
        name="CLUSTER_ACTIVE_LENSES",
        required=False,
        default=(
            "composite_primary_micro,civic_domain_micro,failure_pattern_micro,"
            "civic_weight_systemic,desired_outcome_local,affected_group_local,"
            "geographic_district_micro,service_object_micro,deep_need_local,"
            "ecosystem_signal_systemic"
        ),
        description="Comma-separated enabled cluster lenses.",
    ),
    EnvSpec(
        name="CLUSTER_PRIMARY_LENS",
        required=False,
        default="composite_primary_micro",
        description="Primary lens for orchestrator (must be one of CLUSTER_ACTIVE_LENSES).",
    ),
    EnvSpec(
        name="CLUSTER_SIGNAL_SOURCE",
        required=False,
        default="canonical",
        description="Signal extraction strategy (canonical only).",
    ),
    EnvSpec(
        name="CLUSTER_ID_ALGORITHM",
        required=False,
        default="sha256",
        description="Cluster id derivation: legacy_hash | sha256.",
    ),
    EnvSpec(
        name="CLUSTER_GEO_FILTER",
        required=False,
        default="country",
        description="Geo filtering granularity for clustering: district|settlement|region|country.",
    ),
    EnvSpec(
        name="CLUSTER_GEO_SCOPE",
        required=False,
        default=None,
        description="Optional node responsibility zone, format <level>:<value> (e.g. settlement:tallinn).",
    ),
    EnvSpec(
        name="CLUSTER_TIE_BREAKER",
        required=False,
        default="alpha",
        description="Tie-breaker strategy for equal-score candidates (alpha only until REQ-36).",
    ),
    EnvSpec(
        name="CLUSTER_TYPE_RESOLUTION",
        required=False,
        default="canonical_priority",
        description="Issue type resolution strategy for clustered stories.",
    ),
    EnvSpec(
        name="CLUSTER_CRON_INTERVAL_S",
        required=False,
        default="60",
        description="Cron interval in seconds for background cluster processing.",
    ),
    EnvSpec(
        name="CLUSTER_CRON_ENABLED",
        required=False,
        default="true",
        description="Enable/disable background cluster cron loop.",
    ),
    EnvSpec(
        name="STORY_DRAFT_TTL_SECONDS",
        required=False,
        default="86400",
        description=(
            "TTL for story draft stash entries in seconds (GW-DRAFT-01; recommended 3600–86400)."
        ),
    ),
    EnvSpec(
        name="NODE_SCHEMA_ID",
        required=True,
        default=None,
        description="Active node schema pack id (schema-packs/<id>/<version>/).",
    ),
    EnvSpec(
        name="NODE_SCHEMA_VERSION",
        required=True,
        default=None,
        description="Active node schema pack version (schema-packs/<id>/<version>/).",
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


def _parse_log_format(raw: str | None) -> str:
    if raw is None:
        return "text"
    normalized = raw.strip().lower()
    if normalized not in {"text", "json"}:
        raise ConfigError(
            f"Invalid LOG_FORMAT={raw!r}. Expected one of: ['json', 'text']."
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


def _all_cluster_lens_ids() -> frozenset[str]:
    return frozenset(
        {
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
        }
    )


def _parse_cluster_min_size_by_lens(
    raw: str,
    *,
    allowed_lenses: frozenset[str],
) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in raw.split(","):
        chunk = item.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ConfigError(
                f"Invalid CLUSTER_MIN_SIZE_BY_LENS entry {chunk!r}. Expected lens_id=count."
            )
        lens_id, count_raw = chunk.split("=", 1)
        lens_id = lens_id.strip().lower()
        if lens_id not in allowed_lenses:
            raise ConfigError(
                f"Invalid CLUSTER_MIN_SIZE_BY_LENS lens {lens_id!r}. "
                f"Allowed: {sorted(allowed_lenses)}."
            )
        count = _parse_positive_int(count_raw, env_name="CLUSTER_MIN_SIZE_BY_LENS")
        result[lens_id] = count
    return result


def _parse_cluster_lenses(raw: str) -> tuple[str, ...]:
    allowed = _all_cluster_lens_ids()
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


def _parse_cluster_signal_source(raw: str) -> str:
    normalized = raw.strip().lower()
    if normalized != "canonical":
        raise ConfigError(
            f"Invalid CLUSTER_SIGNAL_SOURCE={raw!r}. Expected: canonical."
        )
    return normalized


def _parse_cluster_tie_breaker(raw: str) -> str:
    normalized = raw.strip().lower()
    if normalized != "alpha":
        raise ConfigError(
            f"Invalid CLUSTER_TIE_BREAKER={raw!r}. Expected: alpha."
        )
    return normalized


def _parse_cluster_id_algorithm(raw: str) -> str:
    normalized = raw.strip().lower()
    allowed = {"legacy_hash", "sha256"}
    if normalized not in allowed:
        raise ConfigError(
            f"Invalid CLUSTER_ID_ALGORITHM={raw!r}. Expected one of: {sorted(allowed)}."
        )
    return normalized


def _parse_cluster_geo_filter(raw: str) -> str:
    from core.geo.scope import parse_cluster_geo_filter

    try:
        return parse_cluster_geo_filter(raw)
    except ValueError as exc:
        raise ConfigError(str(exc)) from exc


def _parse_cluster_geo_scope(raw: str | None) -> tuple[str, str] | None:
    from core.geo.scope import parse_cluster_geo_scope

    if raw is None or not str(raw).strip():
        return None
    try:
        return parse_cluster_geo_scope(raw)
    except ValueError as exc:
        raise ConfigError(str(exc)) from exc


def _parse_cluster_primary_lens(raw: str, active: tuple[str, ...]) -> str:
    normalized = raw.strip().lower()
    if normalized not in _all_cluster_lens_ids():
        raise ConfigError(
            f"Invalid CLUSTER_PRIMARY_LENS={raw!r}. Must be a known lens id."
        )
    if normalized not in active:
        raise ConfigError(
            f"CLUSTER_PRIMARY_LENS={raw!r} must appear in CLUSTER_ACTIVE_LENSES={list(active)}."
        )
    return normalized


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


def _resolve_node_schema_pack(*, schema_id: str, schema_version: str) -> None:
    """Fail-fast: active pair must resolve to an on-disk pack. No civic fallback."""
    from core.schema.contracts import SchemaRef
    from core.schema.errors import UnknownSchemaError, UnsupportedVersionError
    from core.schema.resolver import resolve_pack

    try:
        resolve_pack(SchemaRef(schema_id=schema_id, schema_version=schema_version))
    except (UnknownSchemaError, UnsupportedVersionError) as exc:
        raise ConfigError(
            f"NODE_SCHEMA_ID/NODE_SCHEMA_VERSION={schema_id!r}/{schema_version!r} "
            f"does not resolve to a pack catalog: {exc}"
        ) from exc


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
    log_debug_dir = _get_value(source, "LOG_DEBUG_DIR")
    log_format = _parse_log_format(_get_value(source, "LOG_FORMAT"))
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
                "DB_BACKEND is 'in_memory' but DATABASE_URL or Supabase variables "
                "(SUPABASE_URL / SUPABASE_SERVICE_ROLE) are set. That usually means a `.env` "
                "or shell exports target Supabase while the process still defaults to in_memory "
                "(for example `uvicorn` without loading `.env`). Fix: set DB_BACKEND=supabase "
                "and keep the Supabase vars, or remove DATABASE_URL / SUPABASE_* from the "
                "environment when you intend in_memory."
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
    cluster_min_size_by_lens = _parse_cluster_min_size_by_lens(
        _require_value(source, name="CLUSTER_MIN_SIZE_BY_LENS"),
        allowed_lenses=_all_cluster_lens_ids(),
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
    cluster_primary_lens = _parse_cluster_primary_lens(
        _require_value(source, name="CLUSTER_PRIMARY_LENS"),
        cluster_active_lenses,
    )
    cluster_signal_source = _parse_cluster_signal_source(
        _require_value(source, name="CLUSTER_SIGNAL_SOURCE")
    )
    cluster_id_algorithm = _parse_cluster_id_algorithm(
        _require_value(source, name="CLUSTER_ID_ALGORITHM")
    )
    cluster_geo_filter = _parse_cluster_geo_filter(
        _require_value(source, name="CLUSTER_GEO_FILTER")
    )
    cluster_geo_scope = _parse_cluster_geo_scope(
        _get_value(source, "CLUSTER_GEO_SCOPE")
    )
    cluster_tie_breaker = _parse_cluster_tie_breaker(
        _require_value(source, name="CLUSTER_TIE_BREAKER")
    )
    cluster_type_resolution = _require_value(
        source, name="CLUSTER_TYPE_RESOLUTION"
    ).strip().lower()
    cluster_cron_interval_s = _parse_positive_int(
        _require_value(source, name="CLUSTER_CRON_INTERVAL_S"),
        env_name="CLUSTER_CRON_INTERVAL_S",
    )
    cluster_cron_enabled = _parse_bool(
        _require_value(source, name="CLUSTER_CRON_ENABLED"),
        env_name="CLUSTER_CRON_ENABLED",
    )

    identity_base_url_raw = _get_value(source, "IDENTITY_BASE_URL")
    identity_base_url: str | None = None
    if identity_base_url_raw is not None:
        stripped_me_base = identity_base_url_raw.strip()
        if stripped_me_base:
            identity_base_url = _validate_http_url(
                stripped_me_base, env_name="IDENTITY_BASE_URL"
            ).rstrip("/")

    spa_verify_base_url_raw = _get_value(source, "SPA_VERIFY_BASE_URL")
    spa_verify_base_url: str | None = None
    if spa_verify_base_url_raw is not None:
        stripped_verify = spa_verify_base_url_raw.strip()
        if stripped_verify:
            spa_verify_base_url = _validate_http_url(
                stripped_verify, env_name="SPA_VERIFY_BASE_URL"
            ).rstrip("/")

    story_draft_ttl_raw = _require_value(source, name="STORY_DRAFT_TTL_SECONDS")
    try:
        story_draft_ttl_seconds = int(story_draft_ttl_raw)
    except ValueError as exc:
        raise ConfigError(
            f"Invalid STORY_DRAFT_TTL_SECONDS={story_draft_ttl_raw!r}. Expected integer."
        ) from exc
    if story_draft_ttl_seconds <= 0:
        raise ConfigError(
            f"Invalid STORY_DRAFT_TTL_SECONDS={story_draft_ttl_seconds}. Must be positive."
        )

    node_schema_id = _require_value(source, name="NODE_SCHEMA_ID")
    node_schema_version = _require_value(source, name="NODE_SCHEMA_VERSION")
    _resolve_node_schema_pack(
        schema_id=node_schema_id,
        schema_version=node_schema_version,
    )

    return AppConfig(
        profile=profile,
        api_base_url=api_base_url,
        request_timeout_s=request_timeout_s,
        flags=flags,
        log_level=log_level,
        log_debug_dir=log_debug_dir,
        log_format=log_format,
        db_backend=db_backend,
        db_enabled=db_enabled,
        database_url=database_url,
        supabase_url=supabase_url,
        supabase_service_role=supabase_service_role,
        cluster_min_size=cluster_min_size,
        cluster_min_size_by_lens=cluster_min_size_by_lens,
        cluster_readiness_threshold=cluster_readiness_threshold,
        cluster_active_lenses=cluster_active_lenses,
        cluster_primary_lens=cluster_primary_lens,
        cluster_signal_source=cluster_signal_source,
        cluster_id_algorithm=cluster_id_algorithm,
        cluster_geo_filter=cluster_geo_filter,
        cluster_geo_scope=cluster_geo_scope,
        cluster_tie_breaker=cluster_tie_breaker,
        cluster_type_resolution=cluster_type_resolution,
        cluster_cron_interval_s=cluster_cron_interval_s,
        cluster_cron_enabled=cluster_cron_enabled,
        identity_base_url=identity_base_url,
        spa_verify_base_url=spa_verify_base_url,
        story_draft_ttl_seconds=story_draft_ttl_seconds,
        node_schema_id=node_schema_id,
        node_schema_version=node_schema_version,
    )

