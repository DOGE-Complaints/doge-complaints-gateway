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

    return AppConfig(
        profile=profile,
        api_base_url=api_base_url,
        request_timeout_s=request_timeout_s,
        flags=flags,
        log_level=log_level,
    )

