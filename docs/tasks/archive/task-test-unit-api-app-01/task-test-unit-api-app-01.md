## Task: tests — unit coverage for API and application orchestration

### Цель
Добрать unit/mock покрытие API handlers и application orchestration (intake/create/projection/readiness), включая error branches и contract invariants.

### Почему это важно (риск)
Без плотного unit слоя возможны регрессии в API контрактах и бизнес-оркестрации при изменении инфраструктурных адаптеров.

### Факты из кода (Code Facts / SSOT)
1. Есть базовые HTTP tests для intake/create endpoints.
2. `IssueCreateService` и `StoryIntakeService` содержат не все edge-case ветки под unit покрытием.
3. Readiness и DI orchestration имеют backend-specific ветвления.

### Gap / Проблема
Недостаточное покрытие mock-driven unit тестами API + application слоя.

### AC/DoD
- [ ] (P0) Покрыты happy/error ветки handlers для intake/issues/readiness.
- [ ] (P0) Покрыты orchestration ветви `StoryIntakeService` и `IssueCreateService`.
- [ ] (P1) Зафиксированы инварианты error envelope + trace propagation.
- [ ] (P1) Добавлена карта coverage по API/app bucket.

### Где менять код
- `tests/` (unit buckets)
- `src/core/api/`
- `src/core/application/`

### План выполнения (Execution Plan)
1) Составить список не покрытых веток. 2) Добавить mock-based unit tests. 3) Провести regression прогон.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "api or issue_create or intake" -q
```
