# Тестовая матрица: типы, слои, scope, моки

## Контекст и управленческий вопрос

Ключевой вопрос для CTO-уровня:  
**какую степень уверенности дает текущий тестовый портфель по архитектурным слоям и критическим runtime сценариям, и где расположены зоны остаточного риска?**

## Current state (implemented now)

### 1) Профиль текущей стратегии тестирования

Текущий набор тестов строится вокруг трех целей:

1. Зафиксировать архитектурные инварианты (layer boundaries, DI wiring).
2. Подтвердить контрактность ключевых payload/error моделей.
3. Проверить in-process поведение сервисов на happy-path и важных негативных ветках.

Сильная сторона: хорошая дисциплина contract/unit/in-process integration в модульной архитектуре.  
Ограничение: отсутствует transport-level и external dependency integration слой.

### 2) Matrix by type and scope

| Test file | Type | Layer/scope | Confidence contribution |
|---|---|---|---|
| `tests/test_bootstrap_smoke.py` | smoke | bootstrap + API wiring | Базовый runtime поднимается |
| `tests/test_layer_guardrails.py` | unit/guardrail | architecture boundaries | Контроль дрейфа зависимостей |
| `tests/test_di_service_factory.py` | integration (in-process) | infrastructure -> application | Подтверждает service wiring |
| `tests/test_config_loading.py` | unit | config | Валидация env contract и defaults |
| `tests/test_api_security_and_ops.py` | integration (in-process) | API security + metrics | Подтверждает service auth и ops counters |
| `tests/test_http_transport_smoke.py` | integration (transport HTTP) | FastAPI route policy + envelope/status/content-type | Проверяет реальные HTTP 401/200 и контракты ответа |
| `tests/test_error_envelope_contract.py` | contract | API envelope taxonomy | Стабильность error envelope |
| `tests/test_trace_propagation.py` | integration | observability | Trace continuity в success/error path |
| `tests/test_intake_observability.py` | unit/integration | intake telemetry | Error classification + telemetry |
| `tests/test_story_intake_contract.py` | contract | intake schema | Валидность intake parser/response |
| `tests/test_story_intake_idempotency.py` | integration | application + repository | Идемпотентность intake |
| `tests/test_story_repository_lifecycle.py` | integration | lifecycle | Переходы story статусов |
| `tests/test_signal_profile_schema.py` | unit | profile schema | Signal dimension contract |
| `tests/test_signal_profile_quality_validation.py` | unit | profile quality | Validation rule correctness |
| `tests/test_signal_profile_enrichment_and_versioning.py` | integration | profile service | Versioning и enrichment |
| `tests/test_clustering_engine.py` | unit | cluster engine | Determinism и readiness logic |
| `tests/test_issue_promotion_service.py` | integration | promotion | Gate logic и state transitions |
| `tests/test_spa_projection.py` | contract + unit | projection | Governing enums + tx placeholder guard |
| `tests/test_evidence_pack.py` | integration + contract | evidence/lineage/privacy | Lineage integrity и redaction tiers |
| `tests/test_geo_intelligence.py` | integration | geo pipeline | Cache/fallback/retry behavior |
| `tests/test_adapters_demo_pilot.py` | integration | adapters/profile | Stub adapter determinism by profile |

### 3) Coverage by layer and business capability

- **Bootstrap/composition confidence**  
  `test_bootstrap_smoke.py`, `test_di_service_factory.py`
- **API boundary confidence**  
  `test_api_security_and_ops.py`, `test_error_envelope_contract.py`, `test_trace_propagation.py`
- **Core use-case confidence (application/domain)**  
  lifecycle/idempotency/profile/promotion/projection/evidence/geo test families
- **Config and operational baseline confidence**  
  `test_config_loading.py`, `test_api_security_and_ops.py`

### 4) Mocks / stubs / in-memory doubles (и зачем они нужны)

#### In-memory repositories

- `src/core/infrastructure/repositories.py`:
  - `InMemoryHealthRepository`
  - `InMemoryStoryRepository`
  - `InMemoryIdempotencyRepository`
  - `InMemorySignalProfileRepository`
- `src/core/evidence/repositories.py`:
  - `InMemoryEvidencePackRepository`
- `src/core/promotion/repositories.py`:
  - `InMemoryIssueCandidateStore`
  - `InMemoryReviewAuditLogRepository`
- `src/core/geo/repositories.py`:
  - `InMemoryGeoCacheRepository`

Роль: тестировать бизнес-логику и контракты без влияния I/O и без flaky внешних систем.

#### Provider/adapters stubs

- `src/core/geo/providers.py`:
  - `_TallinnOpenCageStub`, `_NarvaNominatimStub`
- `src/core/adapters/demo.py`:
  - `DemoWalletPushAdapter`, `DemoSignRequestAdapter`, `DemoTxBroadcastAdapter`

Роль: контролируемый deterministic baseline для geo/chain-подобных сценариев.

#### Test-local doubles

- `_OkService` в `tests/test_api_security_and_ops.py`
- `_FlakyProvider` в `tests/test_geo_intelligence.py`

Роль: целевая проверка отказоустойчивых веток (timeouts/retry/errors).

## Architectural consequences and risk zones

- Уверенность высокая на уровне чистой доменной логики и контрактов.
- Уверенность ограничена на уровне инфраструктурной интеграции и transport surface.
- Внедрение real DB/real chain потребует нового класса тестов, иначе возрастает deployment risk.

## Planned target

- Добавить test buckets:
  - `tests/integration_db/*`
  - `tests/integration_chain/*`
  - `tests/e2e/*`
- Ввести contract drift checks между OpenAPI и runtime handlers.
- Добавить failover сценарии для ops incident rehearsals.

## Gaps / risks

- Нет browser-level e2e тестов (пока покрыт только API transport smoke через `TestClient`).
- Нет integration тестов с реальной БД и миграциями.
- Нет integration тестов real on-chain broadcast/finality path.
- Нет chaos/failure-injection тестов для rollback runbook.

## Контрольные проверки

- Быстрый core regression набор:
  `python3 -m pytest tests/test_layer_guardrails.py tests/test_di_service_factory.py tests/test_api_security_and_ops.py tests/test_story_repository_lifecycle.py tests/test_spa_projection.py -q`
