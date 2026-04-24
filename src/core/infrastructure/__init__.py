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
from core.infrastructure.providers import (
    provide_app_config,
    provide_geo_service,
    provide_health_repository,
    provide_idempotency_repository,
    provide_signal_profile_repository,
    provide_service_factory,
    provide_story_repository,
)
from core.infrastructure.service_factory import DefaultServiceFactory

__all__ = [
    "InMemoryHealthRepository",
    "InMemoryIdempotencyRepository",
    "InMemorySignalProfileRepository",
    "InMemoryStoryEmbeddingStore",
    "InMemoryIssueProjectionStore",
    "InMemoryIssueProjectionEmbeddingStore",
    "SqliteDatabase",
    "SqliteStoryRepository",
    "SqliteIdempotencyRepository",
    "SqliteStoryEmbeddingStore",
    "SqliteIssueProjectionStore",
    "SqliteIssueProjectionEmbeddingStore",
    "SupabaseDatabase",
    "SupabaseStoryRepository",
    "SupabaseIdempotencyRepository",
    "SupabaseStoryEmbeddingStore",
    "SupabaseIssueProjectionStore",
    "SupabaseIssueProjectionEmbeddingStore",
    "InMemoryStoryRepository",
    "DefaultServiceFactory",
    "provide_health_repository",
    "provide_idempotency_repository",
    "provide_signal_profile_repository",
    "provide_story_repository",
    "provide_geo_service",
    "provide_app_config",
    "provide_service_factory",
]

