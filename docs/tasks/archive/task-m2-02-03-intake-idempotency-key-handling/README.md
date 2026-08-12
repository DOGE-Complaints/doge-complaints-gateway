## Task: implement — intake idempotency key handling

### Связи
- Story: [`../epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md`](../epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md)
- Epic: [`../epics/EPIC-M2-02-story-intake-and-store.md`](../epics/EPIC-M2-02-story-intake-and-store.md)

### Цель
Обеспечить idempotent intake flow: повторы с тем же ключом не создают дубликатов.

### AC Snapshot
- [ ] Idempotency-key обработка реализована.
- [ ] Повторный запрос возвращает детерминированный результат.
- [ ] Дубликаты story не создаются.
- [ ] Тесты идемпотентности проходят.

### Артефакты выполнения
- Фазовый лог: [`./BULLRUN-PHASE-LOG.md`](./BULLRUN-PHASE-LOG.md)
- Верификация AC: [`./acceptance-verification-STORY-M2-02-03.md`](./acceptance-verification-STORY-M2-02-03.md)
