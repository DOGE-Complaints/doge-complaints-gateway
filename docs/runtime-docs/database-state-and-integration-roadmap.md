# База данных: текущее состояние и roadmap интеграции

## Контекст и управленческий вопрос

Ключевой вопрос:  
**какова фактическая зрелость persistence-контура сегодня, и что требуется для безопасного перехода от in-memory baseline к real DB без потери контрактной целостности?**

## Current state (implemented now)

### 1) Фактическая persistence модель runtime

В текущем `src/core` persistence целиком in-memory:

- `src/core/infrastructure/repositories.py`
- `src/core/evidence/repositories.py`
- `src/core/promotion/repositories.py`
- `src/core/geo/repositories.py`

`provide_service_factory()` в `src/core/infrastructure/providers.py` wiring-ит именно эти реализации.

### 2) Что это означает операционно

- Runtime удобен для deterministic тестов и демо-сценариев.
- Долговременное хранение состояния, recovery после рестарта и транзакционная согласованность отсутствуют.
- Текущая модель intentionally lightweight и не является production persistence profile.

### 3) DB connection status (строго по коду)

- В `src/core/config/schema.py` нет DB connection contract (`DATABASE_URL`, pool params).
- В `src/core` нет SQL/ORM клиентских модулей.
- `example.env` содержит `DATABASE_URL` и Supabase-related значения, но runtime ядро их напрямую не использует.

### 4) Доменные контракты как источник будущей схемы

Минимальный schema candidate формируется из фактических контрактов:

- `StoryRecord`, `IdempotencyRecord`, `SignalProfileRecord` (`src/core/domain/contracts.py`)
- `EvidencePackRecord` (`src/core/evidence/types.py`)
- promotion entities (`src/core/promotion/types.py`)
- geo cache contract (`src/core/geo/repositories.py`)

## Архитектурные последствия и ограничения

- Позитив: in-memory модель обеспечивает быстрый feedback cycle и низкую стоимость изменений в домене.
- Ограничение: нет durability и transactional semantics; это блокирует production deployment.
- Критичный момент перехода: сохранить idempotency и immutable audit behavior в SQL-представлении.

## Planned target (migration roadmap)

### 1) DDL/migrations package

Рекомендуемый минимальный набор таблиц:

- `stories`
- `idempotency_keys`
- `signal_profile_versions`
- `issue_candidates`
- `review_audit_log`
- `evidence_packs`
- `geo_cache`

### 2) SQL-backed repositories (contract compatibility first)

Новые реализации должны сохранить совместимость с текущими protocol/service контрактами:

- `StoryRepository`
- `IdempotencyRepository`
- `SignalProfileRepository`
- `EvidencePackRepository`
- `IssueCandidateStore` и `ReviewAuditLogRepository`

### 3) Config and health integration

- Расширить `AppConfig` (`src/core/config/schema.py`) DB полями.
- Ввести readiness/health проверки DB connectivity и migration version compatibility.

### 4) Integration test wave

- CRUD + transactional behavior для story/idempotency/profile/evidence/promotion.
- Race conditions для idempotency uniqueness.
- Migration up/down проверки на clean database.

## Gaps / risks

- В текущем runtime нет фактического скрипта создания таблиц; это roadmap deliverable.
- Без явной migration strategy есть риск расхождения между in-memory semantics и SQL persistence.
- Особо чувствительные зоны:
  - versioning `SignalProfileRecord`,
  - lineage snapshot semantics в evidence,
  - ordering/immutability review audit trail.

## Контрольные проверки

- Проверка текущего baseline persistence поведения:
  - `python3 -m pytest tests/test_story_repository_lifecycle.py tests/test_story_intake_idempotency.py tests/test_signal_profile_enrichment_and_versioning.py tests/test_evidence_pack.py tests/test_issue_promotion_service.py -q`
