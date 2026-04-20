from __future__ import annotations

from dataclasses import dataclass

from core.api import ApiDependencies, build_api_dependencies


@dataclass(frozen=True)
class AppBootstrap:
    api: ApiDependencies


def bootstrap_app() -> AppBootstrap:
    """Build minimal runtime skeleton across all layers."""
    return AppBootstrap(api=build_api_dependencies())

