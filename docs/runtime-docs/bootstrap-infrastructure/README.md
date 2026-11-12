# Bootstrap Infrastructure — Техническая архитектура doge-complaints-gateway

Этот раздел документирует техническую инфраструктуру проекта послойно.
Каждый документ самодостаточен: содержит концепцию, реализацию с точными ссылками на код и пронумерованные шаги для репликации в новом проекте.

## Для кого

- **Разработчик на этом проекте**: быстрый навигатор по инфраструктурным слоям
- **Новый проект**: скопируй секцию "Шаги репликации" из каждого файла — и восстановишь ту же техническую инфраструктуру
- **Онбординг**: читай по порядку от 01 до 06

## Архитектурная схема слоёв

```
┌──────────────────────────────────────────────────────┐
│  HTTP Transport          asgi_app.py                 │  ← FastAPI, routes, middleware
│  (FastAPI + Uvicorn)     Makefile / railpack.json    │
├──────────────────────────────────────────────────────┤
│  DI Container            dependencies.py             │  ← ApiDependencies, lru_cache
│  (Manual Singleton)      build_api_dependencies()    │
├──────────────────────────────────────────────────────┤
│  Config                  config/schema.py            │  ← AppConfig, ENV_SCHEMA
│  (Pure Env Mapping)      config/env_file.py          │    load_config_from_env()
├──────────────────────────────────────────────────────┤
│  Service Factory         application/factory.py      │  ← ServiceFactory Protocol
│  (SOA + Provider)        infrastructure/providers.py │    DefaultServiceFactory
│                          infrastructure/service_factory.py │
├──────────────────────────────────────────────────────┤
│  Infrastructure          infrastructure/repositories.py   │  ← InMemory* impl
│  (3 backends)            infrastructure/db_supabase.py    │  ← Supabase* (httpx)
│                          infrastructure/db_sqlite.py      │  ← Sqlite* impl
├──────────────────────────────────────────────────────┤
│  Domain                  domain/contracts.py         │  ← Protocol interfaces
│  (Pure Python)           domain/narrative_i18n.py    │    StoryRecord, StoryRepository
└──────────────────────────────────────────────────────┘
```

## Таблица документов

| Файл | Слой | Главное для репликации |
|------|------|------------------------|
| [01-fastapi-transport.md](01-fastapi-transport.md) | HTTP Transport | FastAPI app, lifespan, CORS, middleware, routing |
| [02-dependency-injection.md](02-dependency-injection.md) | DI Container | ApiDependencies dataclass + lru_cache singleton |
| [03-soa-service-factory.md](03-soa-service-factory.md) | SOA | Protocol interfaces + DefaultServiceFactory |
| [04-supabase-persistence.md](04-supabase-persistence.md) | Infrastructure | SupabaseDatabase, bootstrap SQL, migrations |
| [05-env-config-and-launch.md](05-env-config-and-launch.md) | Config + Launch | AppConfig, Makefile, uvicorn, Railway |
| [06-testing-architecture.md](06-testing-architecture.md) | Testing | Pytest layers, conftest, CI, live integration |

## Порядок чтения для "clean project bootstrap"

Если ты восстанавливаешь инфраструктуру с нуля:

1. **[05](05-env-config-and-launch.md)** — сначала env и launch, чтобы понять как вообще стартует приложение
2. **[03](03-soa-service-factory.md)** — SOA: как написать Protocol и фабрику
3. **[04](04-supabase-persistence.md)** — Supabase: bootstrap SQL и реализация репозиториев
4. **[02](02-dependency-injection.md)** — как собрать всё в DI контейнер
5. **[01](01-fastapi-transport.md)** — как повесить DI на HTTP роуты
6. **[06](06-testing-architecture.md)** — как изолировать тесты от .env и Supabase

## Ключевые технологии

| Роль | Технология | Версия |
|------|-----------|--------|
| HTTP framework | FastAPI | ≥ 0.115.0 |
| ASGI server | Uvicorn | ≥ 0.30.0 |
| Persistence | Supabase (PostgREST REST API) | hosted |
| HTTP client | httpx | ≥ 0.27.0 |
| DB driver (fallback/test) | psycopg[binary] | ≥ 3.2.0 |
| Python | CPython | ≥ 3.11 |
| Tests | pytest + pytest-asyncio | ≥ 8.0 / ≥ 0.24 |
| Build | setuptools (pyproject.toml) | ≥ 68 |

**Нет:** SQLAlchemy, Alembic, python-dotenv, Pydantic (в infrastructure layer), Celery, Redis.
