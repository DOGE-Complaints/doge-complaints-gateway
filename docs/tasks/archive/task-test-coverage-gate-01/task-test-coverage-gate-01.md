## Task: docs+qa — formal test coverage gates

### Цель
Ввести обязательный quality gate по test buckets и verification commands для всех batch волн supabase-native перехода.

### Почему это важно (риск)
Без формальных gate-ов сложные task waves закрываются неравномерно и теряют воспроизводимость приемки.

### Факты из кода (Code Facts / SSOT)
1. Есть test matrix документ уровня runtime.
2. Есть run reports registry в bullrun index.
3. Новая supabase-native wave добавляет отдельные unit/mock/live buckets.

### Gap / Проблема
Нет формализованного минимального набора test buckets для закрытия wave.

### AC/DoD
- [ ] (P0) Определены обязательные buckets: unit-api-app, unit-infra-config, unit-domain, integration-supabase-live.
- [ ] (P0) Для каждого batch указан verification command набор.
- [ ] (P1) Обновлены test matrix + bullrun index references.
- [ ] (P1) Проверка run-summary включена в gate.

### Где менять код
- `docs/runtime-docs/test-matrix-by-type-layer-mocks.md`
- `docs/tasks/bullrun-launch-index.md`
- `docs/tasks/run-reports/`

### План выполнения (Execution Plan)
1) Формализовать gates. 2) Синхронизировать docs. 3) Проверить воспроизводимость verification набора.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -q
```
