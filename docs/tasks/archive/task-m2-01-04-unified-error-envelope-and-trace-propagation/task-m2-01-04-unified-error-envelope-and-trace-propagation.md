## Task: implement — unified error envelope and trace propagation

### Source Story
- `docs/tasks/epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-04-unified-error-envelope-and-trace-propagation.md`

### Цель
Ввести единый контракт API-ошибок (`ErrorEnvelope`) и обязательный `trace_id` во всех ответах boundary-слоя.

### AC/DoD
- [ ] Все API-ошибки возвращаются в едином `ErrorEnvelope`.
- [ ] `trace_id` присутствует в каждом ответе и логах.
- [ ] Mapping ошибок предсказуемый.
- [ ] Добавлены contract tests.
- [ ] Документация API-ошибок обновлена.

### Артефакты
- Фазовый лог: `BULLRUN-PHASE-LOG.md`
- Верификация AC: `acceptance-verification-STORY-M2-01-04.md`
