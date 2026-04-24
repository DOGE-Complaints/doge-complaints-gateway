from __future__ import annotations

from core.infrastructure.providers import provide_service_factory


def test_sqlite_backend_uses_sqlite_repositories(monkeypatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("DB_BACKEND", "sqlite")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")

    factory = provide_service_factory()
    assert factory.story_repository.__class__.__name__.startswith("Sqlite")
    assert factory.idempotency_repository.__class__.__name__.startswith("Sqlite")


def test_supabase_backend_uses_supabase_repositories(monkeypatch) -> None:
    monkeypatch.setenv("APP_PROFILE", "demo")
    monkeypatch.setenv("API_BASE_URL", "https://demo.example/api")
    monkeypatch.setenv("DB_BACKEND", "supabase")
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
    monkeypatch.setenv("SUPABASE_URL", "https://demo.supabase.co")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE", "service-role-key")

    factory = provide_service_factory()
    assert factory.story_repository.__class__.__name__.startswith("Supabase")
    assert factory.idempotency_repository.__class__.__name__.startswith("Supabase")
