from __future__ import annotations

from dataclasses import dataclass, field

from core.api.metrics import ApiMetrics
from core.api.security import ServiceTokenAuth, build_service_auth_from_env
from core.application import (
    HealthService,
    IssueCreateService,
    StoryClusterOrchestrator,
    StoryIntakeService,
)
from core.application.issue_create import IssueProjectionReadStore
from core.config import AppConfig, load_config_from_env
from core.domain import LabelTranslationMissStore
from core.identity import IdentityIntrospectionClient, build_identity_introspection_from_config
from core.infrastructure import provide_service_factory


@dataclass(frozen=True)
class ApiDependencies:
    health_service: HealthService
    story_intake_service: StoryIntakeService
    story_cluster_orchestrator: StoryClusterOrchestrator
    issue_create_service: IssueCreateService
    issue_projection_read_store: IssueProjectionReadStore
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
    identity_introspection: IdentityIntrospectionClient | None = None
    metrics: ApiMetrics = field(default_factory=ApiMetrics)
    db_backend: str = "in_memory"
    db_ready: bool = True
    db_checks: dict[str, bool] = field(default_factory=dict)
    label_translation_miss_store: LabelTranslationMissStore | None = None


# Backward-compatible name used in tests and story docs
HandlerDependencies = ApiDependencies


def build_api_dependencies() -> ApiDependencies:
    service_factory = provide_service_factory()
    db_backend = service_factory.config.db_backend
    db_ready = True
    db_checks: dict[str, bool] = {}
    if db_backend == "sqlite" and service_factory.config.database_url is not None:
        from core.infrastructure.db_sqlite import SqliteDatabase

        health_db = SqliteDatabase.from_url(service_factory.config.database_url)
        db_checks = {"connectivity": health_db.healthcheck()}
        db_ready = db_checks["connectivity"]
        health_db.connection.close()
    elif (
        db_backend == "supabase"
        and service_factory.config.supabase_url is not None
        and service_factory.config.supabase_service_role is not None
    ):
        from core.infrastructure.db_supabase import SupabaseDatabase

        health_db = SupabaseDatabase.from_http(
            supabase_url=service_factory.config.supabase_url,
            service_role_key=service_factory.config.supabase_service_role,
            timeout_s=float(service_factory.config.request_timeout_s),
        )
        db_checks = {
            "connectivity": health_db.healthcheck(),
            "schema": health_db.required_tables_ready(),
            "columns": health_db.required_columns_ready(),
            "columns_geo_admin": health_db.required_stories_geo_admin_columns_ready(),
            "columns_v2": health_db.required_stories_intake_v2_columns_ready(),
            "policy_probe": health_db.service_role_policy_probe(),
        }
        db_ready = all(db_checks.values())
    return ApiDependencies(
        health_service=service_factory.get_health_service(),
        story_intake_service=service_factory.get_story_intake_service(),
        story_cluster_orchestrator=service_factory.get_story_cluster_orchestrator(),
        issue_create_service=service_factory.get_issue_create_service(),
        issue_projection_read_store=service_factory.get_issue_projection_read_store(),
        config=service_factory.config,
        service_auth=build_service_auth_from_env(),
        identity_introspection=build_identity_introspection_from_config(
            service_factory.config
        ),
        metrics=ApiMetrics(),
        db_backend=db_backend,
        db_ready=db_ready,
        db_checks=db_checks,
        label_translation_miss_store=service_factory.label_translation_miss_store,
    )
