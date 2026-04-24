from __future__ import annotations
from os import environ
from typing import Mapping

from core.application import ServiceFactory
from core.config import AppConfig, load_config_from_env
from core.domain import (
    HealthRepository,
    IdempotencyRepository,
    SignalProfileRepository,
    StoryRepository,
)
from core.infrastructure.repositories import (
    InMemoryHealthRepository,
    InMemoryIdempotencyRepository,
    InMemoryIssueProjectionEmbeddingStore,
    InMemoryIssueProjectionStore,
    InMemorySignalProfileRepository,
    InMemoryStoryEmbeddingStore,
    InMemoryStoryRepository,
)
from core.infrastructure.db_sqlite import (
    SqliteDatabase,
    SqliteIdempotencyRepository,
    SqliteIssueProjectionEmbeddingStore,
    SqliteIssueProjectionStore,
    SqliteStoryEmbeddingStore,
    SqliteStoryRepository,
)
from core.infrastructure.db_supabase import (
    SupabaseDatabase,
    SupabaseIdempotencyRepository,
    SupabaseIssueProjectionEmbeddingStore,
    SupabaseIssueProjectionStore,
    SupabaseStoryEmbeddingStore,
    SupabaseStoryRepository,
)
from core.infrastructure.service_factory import DefaultServiceFactory
from core.evidence import EvidencePackRepository, InMemoryEvidencePackRepository
from core.geo import (
    GeoResolverChain,
    GeoResolverPolicy,
    GeoService,
    InMemoryGeoCacheRepository,
    InMemoryGeoMetrics,
    default_provider_chain,
)
from core.promotion.repositories import InMemoryIssueCandidateStore, InMemoryReviewAuditLogRepository


def provide_health_repository() -> HealthRepository:
    return InMemoryHealthRepository()


def provide_story_repository() -> StoryRepository:
    return InMemoryStoryRepository()


def provide_idempotency_repository() -> IdempotencyRepository:
    return InMemoryIdempotencyRepository()


def provide_signal_profile_repository() -> SignalProfileRepository:
    return InMemorySignalProfileRepository()


def provide_issue_candidate_store() -> InMemoryIssueCandidateStore:
    return InMemoryIssueCandidateStore()


def provide_review_audit_log_repository() -> InMemoryReviewAuditLogRepository:
    return InMemoryReviewAuditLogRepository()


def provide_evidence_pack_repository() -> EvidencePackRepository:
    return InMemoryEvidencePackRepository()


def provide_geo_service() -> GeoService:
    metrics = InMemoryGeoMetrics()
    cache = InMemoryGeoCacheRepository()
    chain = GeoResolverChain(
        providers=default_provider_chain(),
        policy=GeoResolverPolicy(max_attempts_per_provider=2),
        metrics=metrics,
    )
    return GeoService(cache=cache, resolver=chain, metrics=metrics)


def provide_app_config(env: Mapping[str, str] | None = None) -> AppConfig:
    source = dict(environ) if env is None else dict(env)
    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "https://demo.local")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    return load_config_from_env(source)


def provide_service_factory(config: AppConfig | None = None) -> ServiceFactory:
    resolved_config = config or provide_app_config()
    story_repository = provide_story_repository()
    idempotency_repository = provide_idempotency_repository()
    story_embedding_store = InMemoryStoryEmbeddingStore()
    issue_projection_store = InMemoryIssueProjectionStore()
    issue_projection_embedding_store = InMemoryIssueProjectionEmbeddingStore()

    if resolved_config.db_backend == "sqlite" and resolved_config.database_url is not None:
        sqlite_db = SqliteDatabase.from_url(resolved_config.database_url)
        sqlite_db.ensure_schema()
        story_repository = SqliteStoryRepository(sqlite_db)
        idempotency_repository = SqliteIdempotencyRepository(sqlite_db)
        story_embedding_store = SqliteStoryEmbeddingStore(sqlite_db)
        issue_projection_store = SqliteIssueProjectionStore(sqlite_db)
        issue_projection_embedding_store = SqliteIssueProjectionEmbeddingStore(sqlite_db)
    elif (
        resolved_config.db_backend == "supabase"
        and resolved_config.database_url is not None
    ):
        supabase_db = SupabaseDatabase.from_url(resolved_config.database_url)
        story_repository = SupabaseStoryRepository(supabase_db)
        idempotency_repository = SupabaseIdempotencyRepository(supabase_db)
        story_embedding_store = SupabaseStoryEmbeddingStore(supabase_db)
        issue_projection_store = SupabaseIssueProjectionStore(supabase_db)
        issue_projection_embedding_store = SupabaseIssueProjectionEmbeddingStore(
            supabase_db
        )

    return DefaultServiceFactory(
        health_repository=provide_health_repository(),
        story_repository=story_repository,
        idempotency_repository=idempotency_repository,
        signal_profile_repository=provide_signal_profile_repository(),
        issue_candidate_store=provide_issue_candidate_store(),
        review_audit_log_repository=provide_review_audit_log_repository(),
        evidence_pack_repository=provide_evidence_pack_repository(),
        geo_service=provide_geo_service(),
        config=resolved_config,
        story_embedding_store=story_embedding_store,
        issue_projection_store=issue_projection_store,
        issue_projection_embedding_store=issue_projection_embedding_store,
    )

