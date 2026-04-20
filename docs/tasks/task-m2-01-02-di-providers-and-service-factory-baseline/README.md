## Task: implement — DI providers and service factory baseline

### Связи
- Story: [`../epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-02-di-providers-and-service-factory-baseline.md`](../epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-02-di-providers-and-service-factory-baseline.md)
- Epic: [`../epics/EPIC-M2-01-core-foundation-and-governance.md`](../epics/EPIC-M2-01-core-foundation-and-governance.md)

### Цель
Собрать единый DI-контур и убрать ad-hoc инициализацию сервисов в API-слое.

### AC Snapshot
- [ ] Контракт service factory определен.
- [ ] Providers реализованы и подключены в DI-bridge.
- [ ] API handlers используют только DI.
- [ ] Тесты резолва зависимостей проходят.

### Артефакты выполнения
- Фазовый лог: [`./BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- Верификация AC: [`./acceptance-verification-STORY-M2-01-02.md`](./acceptance-verification-STORY-M2-01-02.md)
