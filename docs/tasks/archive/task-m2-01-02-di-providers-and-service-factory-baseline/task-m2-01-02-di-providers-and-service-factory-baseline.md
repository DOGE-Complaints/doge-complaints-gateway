## Task: implement — DI providers and service factory baseline

### Source Story
- `docs/tasks/epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-02-di-providers-and-service-factory-baseline.md`

### Цель
Ввести единый DI-контур с контрактом `ServiceFactory`, чтобы API-слой получал зависимости только через DI bridge, без ad-hoc инициализации.

### AC/DoD
- [ ] Описан контракт `ServiceFactory`.
- [ ] Реализованы DI providers для базовых сервисов.
- [ ] API-слой получает зависимости через DI bridge.
- [ ] Добавлены unit/integration тесты DI graph.

### Артефакты
- Фазовый лог: `BULLRUN-PHASE-LOG.md`
- Верификация AC: `acceptance-verification-STORY-M2-01-02.md`
