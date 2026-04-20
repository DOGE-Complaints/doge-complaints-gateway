# 14. ADR Log (Demo Architecture)

## ADR-M2-001: Story-first core model
- **Status:** Accepted
- **Decision:** Story хранится как первичный immutable объект.
- **Trade-off:** сложнее data model, но сохраняется доказательная база.

## ADR-M2-002: Dynamic cluster views
- **Status:** Accepted
- **Decision:** Кластеры как пересчитываемые представления с версионируемыми линзами.
- **Trade-off:** выше вычислительная сложность, но меньше semantic lock-in.

## ADR-M2-003: Projection isolation
- **Status:** Accepted
- **Decision:** SPA projection в отдельном модуле, не внутри cluster engine.
- **Trade-off:** +слой, но лучше контрактная стабильность.

## ADR-M2-004: Evidence as separate layer
- **Status:** Accepted
- **Decision:** Evidence pack отделён от публичной issue card.
- **Trade-off:** больше сущностей, но compliance/privacy и traceability выше.

## ADR-M2-005: Demo without blockchain runtime
- **Status:** Accepted
- **Decision:** В demo используем stubs/adapters, не real chain.
- **Trade-off:** меньше end-to-end realism, но быстрее и безопаснее запуск.

## ADR-M2-006: Reuse policy for legacy
- **Status:** Accepted
- **Decision:** Reuse только geo logic intent + часть доменной семантики; остальное greenfield.
- **Trade-off:** больше initial design work, но ниже техдолг.

## ADR-M2-007: Single entry for domain transitions (API and automation)
- **Status:** Proposed (для post-demo внедрения)
- **Decision:** HTTP API и scheduled/worker выполнения вызывают одни и те же application use-case через DI; инфраструктура cron/queue не содержит дублирующей доменной семантики.
- **Trade-off:** чуть больше дисциплины при написании фоновых задач; зато нет расхождения «ручной vs cron» путь.
- **См. также:** `16-automation-orchestration-and-scheduled-jobs.md`, `requirements/20-post-demo-orchestration-and-scheduled-jobs.md`.
