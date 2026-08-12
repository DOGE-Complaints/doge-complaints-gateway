## Task: tests — end-to-end contract checks from intake/create to SPA payload

### Цель
Добавить сквозные e2e/contract проверки полного API pipeline: входные payload -> domain pipeline -> SPA-compatible response shape.

### Почему это важно (риск)
Сейчас тесты intake и projection раздельные; без e2e доказательства есть риск несовместимости между этапами.

### Scope
Входит:
- e2e tests для полного happy-path;
- negative tests для contract violations;
- регресс-гейт на совместимость между стадиями.

Не входит:
- performance/load тесты;
- browser UI e2e.

### Факты из кода (Code Facts / SSOT)
1) `tests/test_http_transport_smoke.py`
- покрывает только ops endpoints.

2) `tests/test_story_intake_contract.py`
- покрывает parser/contract отдельно от HTTP pipeline.

3) `tests/test_spa_projection.py`
- покрывает projection отдельно от intake/create flow.

### Gap / Проблема
`GAP-IP-005`: отсутствует сквозная проверка совместимости pipeline до SPA model.

### Decision Points
- **PM decision:** определить минимальный e2e сценарий для demo acceptance.
- **CTO decision:** зафиксировать тесты как contract-gate перед переводом задач в done.
- **Options:**
  - A: только 1 happy-path e2e.
  - B: happy-path + негативные contract cases + regression matrix.
- **Recommendation:** вариант B (снижает риск интеграционных поломок и сохраняет фундамент).

### AC/DoD
- [ ] (P0) Добавлен e2e test: intake/create -> SPA response contract.
- [ ] (P0) Проверены обязательные SPA keys и envelope shape.
- [ ] (P1) Добавлены negative e2e cases для invalid payload/mapping.
- [ ] (P1) E2E suite включена в verification commands задач `TASK-INTAKE-HTTP-01..TASK-SPA-PROJECTION-DATA-01`.

### Где менять код
- `tests/` (новый e2e contract module)
- `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`
- `docs/tasks/` (acceptance criteria cross-links)

### План выполнения (Execution Plan)
1) Зафиксировать e2e contract сценарии.
2) Реализовать happy-path и negative cases.
3) Интегрировать в verification gates.
4) Обновить test matrix docs.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_http_transport_smoke.py tests/test_spa_projection.py -q
python3 -m pytest tests/test_e2e_intake_create_spa_contract.py -q
```
