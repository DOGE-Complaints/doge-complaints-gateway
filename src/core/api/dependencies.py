from __future__ import annotations

from dataclasses import dataclass, field

from core.api.metrics import ApiMetrics
from core.api.security import ServiceTokenAuth, build_service_auth_from_env
from core.application import HealthService, IssueCreateService, StoryIntakeService
from core.config import AppConfig, load_config_from_env
from core.infrastructure import provide_service_factory


@dataclass(frozen=True)
class ApiDependencies:
    health_service: HealthService
    story_intake_service: StoryIntakeService
    issue_create_service: IssueCreateService
    config: AppConfig = field(
        default_factory=lambda: load_config_from_env(
            {
                "APP_PROFILE": "demo",
                "API_BASE_URL": "https://demo.local",
                "REQUEST_TIMEOUT_S": "15",
            }
        )
    )
    service_auth: ServiceTokenAuth = field(default_factory=ServiceTokenAuth.disabled)
    metrics: ApiMetrics = field(default_factory=ApiMetrics)


# Backward-compatible name used in tests and story docs
HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    service_factory = provide_service_factory()
    return ApiDependencies(
        health_service=service_factory.get_health_service(),
        story_intake_service=service_factory.get_story_intake_service(),
        issue_create_service=service_factory.get_issue_create_service(),
        config=service_factory.config,
        service_auth=build_service_auth_from_env(),
        metrics=ApiMetrics(),
    )
