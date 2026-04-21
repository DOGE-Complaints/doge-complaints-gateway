# Testing Rationale (RU)

## 1. Стратегия тестов в текущем runtime

Текущий test portfolio оптимизирован под модульную архитектуру и быструю обратную связь:

- unit tests для чистых правил и схем;
- contract tests для payload/error стабильности;
- integration (in-process) tests для orchestration между сервисами и in-memory repositories;
- smoke tests для базовой сборки runtime.

Главная цель: обеспечить безопасную эволюцию доменных контрактов до внедрения тяжелой инфраструктуры.

## 2. Почему in-memory doubles доминируют

### Фактическая реализация

- Репозитории и stores в `src/core/infrastructure/repositories.py`, `src/core/evidence/repositories.py`, `src/core/promotion/repositories.py`, `src/core/geo/repositories.py`.
- Stub providers/adapters в `src/core/geo/providers.py`, `src/core/adapters/demo.py`.

### Практическая причина

- Исключение flaky внешних зависимостей.
- Полный контроль над сценариями ошибок/переходов.
- Детальная проверка бизнес-инвариантов без I/O шума.

## 3. Какие риски покрыты хорошо

- Layer drift (guardrails).
- Config contract errors.
- Envelope/error taxonomy.
- Story lifecycle и intake idempotency.
- Projection contract rules (governed enums, tx placeholders).
- Promotion state machine and gate logic.
- Evidence lineage and redaction tiers.
- Geo fallback/retry baseline.

Источники: `tests/*.py`, особенно

- `test_layer_guardrails.py`
- `test_config_loading.py`
- `test_error_envelope_contract.py`
- `test_story_repository_lifecycle.py`
- `test_spa_projection.py`
- `test_issue_promotion_service.py`
- `test_evidence_pack.py`
- `test_geo_intelligence.py`

## 4. Какие риски покрыты слабо (структурные пробелы)

1. Нет HTTP transport-level e2e.
2. Нет DB-backed integration/migration tests.
3. Нет real chain adapter integration tests.
4. Нет chaos/failure-injection rehearsal тестов для incident runbooks.

## 5. Что означает это для релизного решения

- Для demo/pilot-internal baseline текущий уровень достаточен по доменной корректности.
- Для production-grade выхода без нового test wave риск неприемлем:
  - инфраструктурные ошибки не будут заранее детектироваться в нужной полноте.

## 6. Recommended next test wave (planned)

### Wave A: Persistence

- `tests/integration_db/*`:
  - idempotency uniqueness,
  - transactional integrity,
  - migration compatibility.

### Wave B: Transport

- `tests/e2e/*`:
  - health/readiness/protected/metrics end-to-end over HTTP.

### Wave C: Chain

- `tests/integration_chain/*`:
  - signing/broadcast/finality scenarios,
  - retry/fallback behavior.
