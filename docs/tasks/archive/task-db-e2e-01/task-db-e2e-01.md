## Task: tests — e2e contracts for DB-backed intake/create/projection

### Цель
Добавить сквозные tests, подтверждающие совместимость pipeline `intake/create -> DB persistence -> SPA projection`.

### Почему это важно (риск)
Без e2e tests легко получить тихие разрывы между слоями и невалидные linkage-цепочки.

### Scope
Входит: happy-path + negative contract cases для DB-backed flow.
Не входит: нагрузочные/perf тесты.

### Факты из кода (Code Facts / SSOT)
1. Сейчас есть разрозненные tests intake/projection, но не DB-backed e2e.
2. Target DoD прямо требует e2e контрактных тестов.
3. План DB wave включает 4 раздельных data слоя и связи между ними.

### Gap / Проблема
Сквозной gap проверки совместимости стадий при переходе на DB слой.

### Decision Points
- **PM decision:** минимальный e2e сценарий для demo acceptance.
- **CTO decision:** e2e suite как обязательный gate перед `Done`.
- **Options A/B:** только happy-path vs happy-path + negative matrix.
- **Recommendation:** happy-path + negative matrix.

### AC/DoD
- [ ] (P0) Есть e2e тест полного DB-backed потока.
- [ ] (P0) Проверены связи `story -> issue -> projection -> evidence`.
- [ ] (P1) Есть negative tests на contract mismatch.
- [ ] (P1) E2E suite включена в verification gates DB задач.

### Где менять код
- `tests/` (новые e2e test modules)
- `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`
- task acceptance cross-links

### План выполнения (Execution Plan)
1) Зафиксировать e2e сценарии. 2) Реализовать тесты. 3) Интегрировать в CI/check gates. 4) Обновить docs.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
# e2e suite для DB-backed pipeline
```
