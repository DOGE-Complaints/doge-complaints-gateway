## Task: tests — unit coverage for infrastructure and config switching

### Цель
Добавить unit/mock тесты для infrastructure adapters, service factory и backend-switching (in_memory/sqlite/supabase), включая config parsing edge-cases.

### Почему это важно (риск)
Ошибки в infra/config слое ломают runtime еще до бизнес-логики и создают трудноотлавливаемые дефекты.

### Факты из кода (Code Facts / SSOT)
1. Factory/providers управляют backend selection.
2. Есть sqlite adapters и in-memory adapters.
3. Supabase-native runtime требует строгого переключения и тестового подтверждения.

### Gap / Проблема
Недостаточно unit-покрытия для backend switch логики и инфраструктурных edge-cases.

### AC/DoD
- [ ] (P0) Покрыты unit тестами providers/factory branches для всех backend режимов.
- [ ] (P0) Покрыты config parsing негативные сценарии.
- [ ] (P1) Добавлены mocks/stubs для внешних DB клиентов.
- [ ] (P1) Поддерживается deterministic test execution.

### Где менять код
- `tests/`
- `src/core/infrastructure/`
- `src/core/config/`

### План выполнения (Execution Plan)
1) Матрица ветвлений providers/factory. 2) Тесты с mocks/stubs. 3) Stabilization и cleanup fixtures.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "config or provider or service_factory" -q
```
