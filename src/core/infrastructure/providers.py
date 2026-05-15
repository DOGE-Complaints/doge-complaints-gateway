from __future__ import annotations
from os import environ
import logging
from typing import Mapping

from core.application import ServiceFactory
from core.config import AppConfig, load_config_from_env
from core.config.env_file import merge_dotenv_from_cwd
from core.domain import (
    HealthRepository,
    IdempotencyRepository,
    SignalProfileRepository,
    StoryRepository,
)
from core.domain import ClusterMembershipStore, StorySignalStore
from core.infrastructure.repositories import (
    InMemoryClusterMembershipStore,
    InMemoryHealthRepository,
    InMemoryIdempotencyRepository,
    InMemoryIssueProjectionEmbeddingStore,
    InMemoryIssueProjectionStore,
    InMemoryIssueStoryLinkStore,
    InMemorySignalProfileRepository,
    InMemoryStoryEmbeddingStore,
    InMemoryStoryRepository,
    InMemoryStorySignalStore,
)
from core.infrastructure.db_sqlite import (
    SqliteClusterMembershipStore,
    SqliteDatabase,
    SqliteIssueCandidateStore,
    SqliteIdempotencyRepository,
    SqliteIssueStoryLinkStore,
    SqliteIssueProjectionEmbeddingStore,
    SqliteIssueProjectionStore,
    SqliteReviewAuditLogRepository,
    SqliteStoryEmbeddingStore,
    SqliteStoryRepository,
    SqliteStorySignalStore,
)
from core.infrastructure.db_supabase import (
    SupabaseClusterMembershipStore,
    SupabaseDatabase,
    SupabaseIssueCandidateStore,
    SupabaseIdempotencyRepository,
    SupabaseIssueStoryLinkStore,
    SupabaseIssueProjectionEmbeddingStore,
    SupabaseIssueProjectionStore,
    SupabaseReviewAuditLogRepository,
    SupabaseStoryEmbeddingStore,
    SupabaseStoryRepository,
    SupabaseStorySignalStore,
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

logger = logging.getLogger(__name__)


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
    if env is None:
        priority = dict(environ)
        source = dict(priority)
        merge_dotenv_from_cwd(source, priority=priority)
    else:
        source = dict(env)
    source.setdefault("APP_PROFILE", "demo")
    source.setdefault("API_BASE_URL", "https://demo.local")
    source.setdefault("REQUEST_TIMEOUT_S", "15")
    return load_config_from_env(source)


def provide_service_factory(config: AppConfig | None = None) -> ServiceFactory:
    resolved_config = config or provide_app_config()
    logger.info(
        "factory.persistence_backend_selected backend=%s stage=%s",
        resolved_config.db_backend,
        "infrastructure.providers",
        extra={
            "backend": resolved_config.db_backend,
            "stage": "infrastructure.providers",
            "outcome": "selected",
        },
    )
    story_repository = provide_story_repository()
    idempotency_repository = provide_idempotency_repository()
    story_embedding_store = InMemoryStoryEmbeddingStore()
    issue_projection_store = InMemoryIssueProjectionStore()
    issue_projection_embedding_store = InMemoryIssueProjectionEmbeddingStore()
    issue_story_link_store = InMemoryIssueStoryLinkStore()
    issue_candidate_store = provide_issue_candidate_store()
    review_audit_log_repository = provide_review_audit_log_repository()
    story_signal_store: StorySignalStore = InMemoryStorySignalStore()
    cluster_membership_store: ClusterMembershipStore = InMemoryClusterMembershipStore()

    if resolved_config.db_backend == "sqlite" and resolved_config.database_url is not None:
        sqlite_db = SqliteDatabase.from_url(resolved_config.database_url)
        sqlite_db.ensure_schema()
        story_repository = SqliteStoryRepository(sqlite_db)
        idempotency_repository = SqliteIdempotencyRepository(sqlite_db)
        story_embedding_store = SqliteStoryEmbeddingStore(sqlite_db)
        issue_projection_store = SqliteIssueProjectionStore(sqlite_db)
        issue_projection_embedding_store = SqliteIssueProjectionEmbeddingStore(sqlite_db)
        issue_candidate_store = SqliteIssueCandidateStore(sqlite_db)
        review_audit_log_repository = SqliteReviewAuditLogRepository(sqlite_db)
        issue_story_link_store = SqliteIssueStoryLinkStore(sqlite_db)
        story_signal_store = SqliteStorySignalStore(sqlite_db)
        cluster_membership_store = SqliteClusterMembershipStore(sqlite_db)
        logger.info(
            "factory.persistence_backend_selected backend=%s stage=%s",
            "sqlite",
            "infrastructure.providers.sqlite",
            extra={
                "backend": "sqlite",
                "stage": "infrastructure.providers.sqlite",
                "outcome": "selected",
            },
        )
    elif (
        resolved_config.db_backend == "supabase"
        and resolved_config.supabase_url is not None
        and resolved_config.supabase_service_role is not None
    ):
        supabase_db = SupabaseDatabase.from_http(
            supabase_url=resolved_config.supabase_url,
            service_role_key=resolved_config.supabase_service_role,
            timeout_s=float(resolved_config.request_timeout_s),
        )
        story_repository = SupabaseStoryRepository(supabase_db)
        idempotency_repository = SupabaseIdempotencyRepository(supabase_db)
        story_embedding_store = SupabaseStoryEmbeddingStore(supabase_db)
        issue_projection_store = SupabaseIssueProjectionStore(supabase_db)
        issue_projection_embedding_store = SupabaseIssueProjectionEmbeddingStore(
            supabase_db
        )
        issue_candidate_store = SupabaseIssueCandidateStore(supabase_db)
        review_audit_log_repository = SupabaseReviewAuditLogRepository(supabase_db)
        issue_story_link_store = SupabaseIssueStoryLinkStore(supabase_db)
        story_signal_store = SupabaseStorySignalStore(supabase_db)
        cluster_membership_store = SupabaseClusterMembershipStore(supabase_db)
        logger.info(
            "factory.persistence_backend_selected backend=%s stage=%s",
            "supabase",
            "infrastructure.providers.supabase",
            extra={
                "backend": "supabase",
                "stage": "infrastructure.providers.supabase",
                "outcome": "selected",
            },
        )
    else:
        logger.info(
            "factory.persistence_backend_selected backend=%s stage=%s",
            "in_memory",
            "infrastructure.providers.in_memory",
            extra={
                "backend": "in_memory",
                "stage": "infrastructure.providers.in_memory",
                "outcome": "selected",
            },
        )

    logger.info(
        "factory.persistence_wiring backend=%s story_repository=%s idempotency_repository=%s story_embedding_store=%s",
        resolved_config.db_backend,
        story_repository.__class__.__name__,
        idempotency_repository.__class__.__name__,
        story_embedding_store.__class__.__name__,
        extra={
            "backend": resolved_config.db_backend,
            "story_repository": story_repository.__class__.__name__,
            "idempotency_repository": idempotency_repository.__class__.__name__,
            "story_embedding_store": story_embedding_store.__class__.__name__,
            "stage": "infrastructure.providers",
            "outcome": "success",
        },
    )

    return DefaultServiceFactory(
        health_repository=provide_health_repository(),
        story_repository=story_repository,
        idempotency_repository=idempotency_repository,
        signal_profile_repository=provide_signal_profile_repository(),
        issue_candidate_store=issue_candidate_store,
        review_audit_log_repository=review_audit_log_repository,
        evidence_pack_repository=provide_evidence_pack_repository(),
        geo_service=provide_geo_service(),
        config=resolved_config,
        story_embedding_store=story_embedding_store,
        issue_projection_store=issue_projection_store,
        issue_projection_embedding_store=issue_projection_embedding_store,
        issue_story_link_store=issue_story_link_store,
        story_signal_store=story_signal_store,
        cluster_membership_store=cluster_membership_store,
    )

