# Architecture: Multi-View Reference

Этот документ — навигационный хаб. Одна и та же система показана с 5 углов зрения.  
Каждый View — краткое резюме + ссылки на источник правды (код или профильный doc).

---

## View 1: HTTP Transport — что видно снаружи

**Источник:** `src/core/api/asgi_app.py` + `docs/runtime-docs/architecture-and-layers-as-is.md §6`

| Метод | Путь | Auth | Назначение |
|-------|------|------|------------|
| GET | `/health` | public | Liveness probe |
| GET | `/ready` | public | Readiness probe |
| GET | `/protected/status` | Bearer token | Service auth gate |
| GET | `/metrics` | Bearer token | In-process counters |
| GET | `/demo/auth-page` | public | Demo static page |
| POST | `/intake/stories` | public | Принять жалобу |
| POST | `/issues` | public | Создать Issue + SPA projection |

**Auth:** `Authorization: Bearer <token>` или `X-Service-Token: <token>`.  
При `APP_PROFILE=pilot` — `SERVICE_API_TOKEN` обязателен, иначе fail-fast startup.  
При `APP_PROFILE=demo` — auth disabled если `SERVICE_API_TOKEN` не задан.

**Конверт ответа:**
- Успех: `{ "data": {...}, "trace_id": "..." }`
- Ошибка: `{ "error": { "code", "type", "message", "details" }, "trace_id": "..." }`

---

## View 2: Domain Pipeline — что происходит внутри

**Источник:** `src/core/application/` + `docs/runtime-docs/architecture-and-layers-as-is.md §7`

### Intake flow (`POST /intake/stories`)

```
StoryIntakeRequest {schema_version, submitter, narrative, origin?, privacy?}
  → StoryIntakeService.create_story()
       ├─ Idempotency check (idempotency-key header)
       ├─ GeoService.resolve() → StoryGeoSnapshot (если есть location_query)
       └─ StoryRecord сохраняется
            lifecycle: ACCEPTED → READY_FOR_PROFILE (narrative complete)
                               → PARTIAL_READY (narrative пустой)
```

### Issue create flow (`POST /issues`)

```
IssueCreateCommand {cluster_id, story_ids, readiness_score, title}
  → IssuePromotionService (state machine):
       DRAFT → submit_for_review (gate check) → READY_FOR_REVIEW
       → start_review → IN_REVIEW
       → record_review(APPROVE) → PROMOTED

  → StoryPromotionProjectionBridge.build_projection_input()
       Читает N StoryRecord → агрегирует narratives → выводит:
         issue_type: INCIDENT | SERVICE_REQUEST | IMPROVEMENT
         labels: [infrastructure, safety, waste, district]
         i18n: I18nText{et, ru, en} (сейчас deterministic fallback)

  → IssueProjectionService.project() → SpaIssueProjection
       → to_public_dict() → {id, status, type, labels, title, summary, description}
```

**Story lifecycle statuses** (`StoryLifecycleStatus`):
- `accepted` → начальный статус после сохранения
- `partial_ready` → narrative пустой/неполный
- `ready_for_profile` → narrative корректный, готов к enrichment

**Issue candidate statuses** (`IssueCandidateStatus`):
- `draft` → только создан (мутации: merge, split, reframe)
- `ready_for_review` → прошёл promotion gates
- `in_review` → на ревью
- `promoted` / `rejected` → финальные статусы

---

## View 3: DI Composition — как собрано

**Источник:** `docs/runtime-docs/architecture-and-layers-as-is.md §1`

```
run_asgi_server()
  └─ FastAPI app (asgi_app.py)
       └─ get_api_dependencies() [lru_cache]
            └─ build_api_dependencies()
                 └─ provide_service_factory()         [infrastructure/providers.py]
                      └─ DefaultServiceFactory        [infrastructure/service_factory.py]
                           ├─ InMemoryStoryRepository
                           ├─ InMemoryIdempotencyRepository
                           ├─ InMemorySignalProfileRepository
                           ├─ InMemoryIssueCandidateStore
                           ├─ InMemoryReviewAuditLogRepository
                           ├─ InMemoryEvidencePackRepository
                           ├─ InMemoryGeoCacheRepository
                           └─ GeoService (с chain providers)
```

**Сервисы, доступные через `ApiDependencies`:**

| Поле | Сервис | Используется в |
|------|--------|---------------|
| `health_service` | `HealthService` | `handle_health` |
| `story_intake_service` | `StoryIntakeService` | `handle_story_intake` |
| `issue_create_service` | `IssueCreateService` | `handle_issue_create` |
| `service_auth` | `ServiceTokenAuth` | все protected routes |
| `metrics` | `ApiMetrics` | все handlers |

---

## View 4: Layer Boundaries — что может импортировать что

**Источник:** `tests/test_layer_guardrails.py`

```
api/          → может импортировать: application, domain, config
application/  → может импортировать: domain, config
domain/       → не импортирует ничего из других слоёв
infrastructure/ → может импортировать: domain, config, application (protocols)
```

**Запрещённые зависимости (зафиксированы в guardrail тестах):**
- `domain` НЕ импортирует `api`, `application`, `infrastructure`
- `application` НЕ импортирует `api`, `infrastructure`
- `infrastructure` НЕ импортирует `api`

**Feature-модули** (не слои, а бизнес-подсистемы):

| Модуль | Ответственность |
|--------|----------------|
| `intake/` | Парсинг и валидация входного payload |
| `profile/` | Нормализация / enrichment сигналов |
| `cluster/` | Кластеризация по 6 измерениям |
| `promotion/` | State machine кандидатов Issue |
| `projection/` | SPA-совместимый DTO |
| `evidence/` | Lineage, redaction, audit |
| `geo/` | Cache-first геокодинг с fallback |
| `adapters/` | Wallet/sign/broadcast протоколы (stubs) |

---

## View 5: Test Coverage Map — в чём уверены, в чём нет

**Источник:** `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`

| Уровень уверенности | Покрытые области |
|---------------------|-----------------|
| **HIGH** | Domain contracts (story lifecycle, idempotency, signal profiles), promotion state machine, projection enums + tx validation, evidence lineage, geo fallback/retry |
| **MEDIUM** | HTTP transport (intake, issue create, e2e pipeline), API security (auth on/off, token extraction), DI bootstrap, config validation |
| **LOW / ABSENT** | Real DB integration + migrations, real chain adapter (Arweave), chaos/failure-injection, browser-level UI |

**Ключевые тесты по архитектурным зонам:**

```
Bootstrap & DI:       test_bootstrap_smoke.py, test_di_service_factory.py
Layer guardrails:     test_layer_guardrails.py
API security:         test_api_security_and_ops.py, test_http_transport_smoke.py
HTTP transport:       test_http_intake_endpoint.py, test_http_issue_create_endpoint.py
E2E pipeline:         test_e2e_intake_create_spa_contract.py
Bridge & contracts:   test_story_promotion_projection_bridge.py
Domain lifecycle:     test_story_repository_lifecycle.py, test_story_intake_idempotency.py
Projection contract:  test_spa_projection.py
Evidence:             test_evidence_pack.py
Geo:                  test_geo_intelligence.py
```

---

## Навигация по профильным документам

| Вопрос | Документ |
|--------|----------|
| Как устроены слои? | `architecture-and-layers-as-is.md` |
| Какие API роуты и форматы? | `api-reference/API_REFERENCE.md`, `api-reference/openapi.yaml` |
| Как запустить локально? | `server-env-quickstart.md` |
| Какой статус DB / Arweave? | `database-state-and-integration-roadmap.md`, `arweave-status-and-runbook.md` |
| Как работает auth? | `security-env-api-access.md` |
| Что тестировано? | `test-matrix-by-type-layer-mocks.md` |
| Что делать при инциденте? | `operations-playbook.md` |
| Откуда взяты факты? | `appendix/evidence-trace-map-ru.md` |
