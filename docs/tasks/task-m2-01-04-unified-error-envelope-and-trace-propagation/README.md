## Task: implement — unified error envelope and trace propagation

### Связи
- Story: [`../epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-04-unified-error-envelope-and-trace-propagation.md`](../epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-04-unified-error-envelope-and-trace-propagation.md)
- Epic: [`../epics/EPIC-M2-01-core-foundation-and-governance.md`](../epics/EPIC-M2-01-core-foundation-and-governance.md)

### Цель
Стабилизировать API-поведение: единый формат ошибок и обязательный `trace_id` в ответах и логах.

### AC Snapshot
- [ ] ErrorEnvelope унифицирован для всех ошибок.
- [ ] `trace_id` пробрасывается end-to-end.
- [ ] Contract tests покрывают error shape и trace propagation.
- [ ] Документация ответов API синхронизирована.

### Артефакты выполнения
- Фазовый лог: [`./BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- Верификация AC: [`./acceptance-verification-STORY-M2-01-04.md`](./acceptance-verification-STORY-M2-01-04.md)
