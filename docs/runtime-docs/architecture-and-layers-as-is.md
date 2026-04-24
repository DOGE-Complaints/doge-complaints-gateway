# Architecture & Layers (as-is)

## Контекст и управленческий вопрос

Текущий вопрос для архитектурного управления:  
**можно ли считать runtime-контур модульно устойчивым, с понятной ответственностью слоев и контролем дрейфа зависимостей?**

## Current state (implemented now)

### 1) Composition root и цепочка сборки

Фактическая сборка runtime выполняется в несколько этапов:

1. `bootstrap_app()` в `src/core/bootstrap.py` поднимает верхний runtime container.
2. `build_api_dependencies()` в `src/core/api/dependencies.py` собирает API boundary dependencies.
3. `provide_service_factory()` в `src/core/infrastructure/providers.py` формирует инфраструктурный wiring.
4. `DefaultServiceFactory` в `src/core/infrastructure/service_factory.py` отдает готовые application services.

```mermaid
flowchart TD
  bootstrapApp[bootstrap_app] --> apiDeps[build_api_dependencies]
  apiDeps --> providerLayer[provide_service_factory]
  providerLayer --> defaultFactory[DefaultServiceFactory]
  defaultFactory --> healthService[HealthService]
  defaultFactory --> intakeService[StoryIntakeService]
  defaultFactory --> signalProfileService[SignalProfileService]
  defaultFactory --> clusteringEngine[ClusteringEngine]
  defaultFactory --> promotionService[IssuePromotionService]
  defaultFactory --> projectionService[IssueProjectionService]
  defaultFactory --> evidenceService[EvidencePackService]
  defaultFactory --> geoService[GeoService]
```

### 2) Responsibility map по слоям

1. **Bootstrap / composition**
   - Функция: стартовая сборка runtime dependency graph.
   - Файлы: `src/core/bootstrap.py`.
2. **API boundary**
   - Функция: envelope, trace, security gate, ops-level handlers.
   - Файлы: `src/core/api/dependencies.py`, `src/core/api/handlers.py`, `src/core/api/envelope.py`, `src/core/api/security.py`, `src/core/api/metrics.py`, `src/core/api/logging.py`.
3. **Application**
   - Функция: orchestration бизнес-переходов и use-case поведения.
   - Файлы: `src/core/application/factory.py`, `src/core/application/services.py`.
4. **Domain**
   - Функция: неизменяемые контракты и статусы сущностей (`StoryRecord`, `SignalProfileRecord`, lifecycle enums).
   - Файлы: `src/core/domain/contracts.py`.
5. **Infrastructure**
   - Функция: concrete repositories/providers/service wiring для текущего runtime.
   - Файлы: `src/core/infrastructure/providers.py`, `src/core/infrastructure/service_factory.py`, `src/core/infrastructure/repositories.py`.

### 3) Feature-модули и их роль в цепочке данных

- `intake`: контракт входного payload и построение response envelope (`src/core/intake/contracts.py`).
- `profile`: нормализация/обогащение/валидация сигналов (`src/core/profile/*`).
- `cluster`: построение кластерных view и readiness score (`src/core/cluster/engine.py`).
- `promotion`: gate-based переходы кандидатов и audit trail (`src/core/promotion/*`).
- `projection`: governed mapping в SPA issue контракт (`src/core/projection/*`).
- `evidence`: lineage/evidence pack и tiered redaction (`src/core/evidence/*`).
- `geo`: cache-first гео-резолвинг с fallback/retry (`src/core/geo/*`).
- `adapters`: wallet/sign/broadcast protocol surfaces и demo/pilot stubs (`src/core/adapters/*`).
- `config`: профиль и feature-flag contract (`src/core/config/schema.py`).

### 4) Фактический data-flow контур (domain pipeline)

```mermaid
flowchart TD
  intakeContract[StoryIntakeRequest] --> intakeService[StoryIntakeService]
  intakeService --> storyRepo[StoryRepository]
  intakeService --> geoService[GeoService]
  storyRepo --> signalProfileService[SignalProfileService]
  signalProfileService --> clusteringEngine[ClusteringEngine]
  clusteringEngine --> promotionService[IssuePromotionService]
  promotionService --> projectionService[IssueProjectionService]
  promotionService --> evidenceService[EvidencePackService]
```

Примечание: этот pipeline отражает модульную совместимость и service surfaces.  
Полный orchestration сценарий как единый runtime workflow в коде сейчас не собран в один end-to-end orchestrator.

### 5) Как контролируется архитектурный дрейф

- `tests/test_layer_guardrails.py` фиксирует import-ограничения между слоями.
- `tests/test_bootstrap_smoke.py` подтверждает, что composition дает рабочий runtime.
- `tests/test_di_service_factory.py` подтверждает, что `DefaultServiceFactory` выдает ожидаемые services и конфиг.

### 6) HTTP Transport Layer (as-is, все активные маршруты)

Источник: `src/core/api/asgi_app.py` (строки 25–166). Все 8 маршрутов зарегистрированы и активны.

| Метод | Путь | Auth | Handler | Тест |
|-------|------|------|---------|------|
| GET | `/health` | public | `handle_health` | `test_http_transport_smoke.py` |
| GET | `/ready` | public | `handle_readiness` | `test_http_transport_smoke.py` |
| GET | `/protected/status` | Bearer / X-Service-Token | `handle_protected_status` | `test_http_transport_smoke.py` |
| GET | `/metrics` | Bearer / X-Service-Token | `handle_metrics` | `test_http_transport_smoke.py` |
| GET | `/demo/auth-page` | public | `FileResponse` (static) | — |
| GET | `/demo/auth-page/styles.css` | public | `FileResponse` (static) | — |
| POST | `/intake/stories` | public | `handle_story_intake` | `test_http_intake_endpoint.py` |
| POST | `/issues` | public | `handle_issue_create` | `test_http_issue_create_endpoint.py` |

`PUBLIC_ROUTES` tuple (`asgi_app.py:25-31`): `/health`, `/ready`, `/demo/auth-page`, `/intake/stories`, `/issues`.

### 7) End-to-End Domain Pipeline (as-is)

Сквозной поток данных через систему. Источники: `src/core/application/`, `src/core/promotion/`, `src/core/projection/`.

```
POST /intake/stories
  │
  ├─ parse_story_intake_request(payload)       [intake/contracts.py]
  └─ StoryIntakeService.create_story()         [application/services.py]
       ├─ IdempotencyRepository.get_by_key()   → early return если dup
       ├─ GeoService.resolve_for_story()       [geo/service.py] (если location_query)
       ├─ StoryRecord{lifecycle: ACCEPTED}  → StoryRepository.save()
       └─ advance_story_readiness()
            narrative complete  → READY_FOR_PROFILE
            narrative empty     → PARTIAL_READY
  → Response: {story_id, status, schema_version}

POST /issues
  │
  └─ IssueCreateService.create_issue(IssueCreateCommand)  [application/issue_create.py]
       │
       ├─ IssuePromotionService.create_candidate()    → IssueCandidateRecord{DRAFT}
       ├─ IssuePromotionService.submit_for_review()   → gate check → READY_FOR_REVIEW
       ├─ IssuePromotionService.start_review()        → IN_REVIEW
       ├─ IssuePromotionService.record_review(APPROVE) → PROMOTED
       │
       ├─ StoryPromotionProjectionBridge.build_projection_input()
       │    ├─ StoryRepository.get_story() × N   [по каждому story_id]
       │    ├─ _derive_issue_type(title, corpus)
       │    │    "broken/outage/hazard" → INCIDENT
       │    │    "request/need/please"  → SERVICE_REQUEST
       │    │    default               → IMPROVEMENT
       │    ├─ _derive_labels(title, corpus)
       │    │    waste/garbage → "waste"
       │    │    district/neighborhood → "district"
       │    │    road/street/bridge → "infrastructure"
       │    │    danger/unsafe → "safety"
       │    │    default → ["infrastructure"]
       │    └─ ProjectionInput{status: PUBLISHED, i18n: I18nText(et,ru,en)}
       │
       └─ IssueProjectionService.project(projection_input)
            ├─ validate_governed_enums()   [projection/validation.py]
            ├─ validate_optional_tx_fields()
            └─ SpaIssueProjection.to_public_dict()
                 → {id, status, type, labels, title, summary, description}
  → Response: {issue_id, status, projection, policy_version}
```

E2E тест (happy path + gate failure + validation error): `tests/test_e2e_intake_create_spa_contract.py`

## Architectural consequences and limitations

- Модель modular-by-contract уже есть, но delivery surface пока в форме handler functions, а не router/server entrypoint.
- Это снижает риск избыточной связанности на раннем этапе, но ограничивает прямую переносимость в production HTTP runtime без отдельного adapter слоя.
- DI дисциплина в коде подтверждается тестами, что хорошо для контролируемой эволюции.

## Planned target

- Расширить composition root под SQL-backed repositories и real chain adapters.
- Ввести единый end-to-end orchestration сервис для сценария intake→signal profile→cluster→promotion→projection→evidence (сейчас модули существуют независимо, единого оркестратора нет).

## Gaps / risks

- Нет единого orchestration сервиса, склеивающего все доменные модули в один синхронный pipeline.
- Риск смешения target-архитектуры из `docs/solution architecture` с текущим runtime-as-is, если не держать строгую границу источников.
- Нет SQL-backed persistence; in-memory блокирует production deployment.

## Контрольные проверки

- Проверка слоев и wiring:  
  `python3 -m pytest tests/test_layer_guardrails.py tests/test_bootstrap_smoke.py tests/test_di_service_factory.py -q`
