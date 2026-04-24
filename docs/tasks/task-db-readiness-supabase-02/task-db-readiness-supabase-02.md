## Task: implement — supabase readiness preflight checks

### Цель
Добавить реальный readiness-проход для `DB_BACKEND=supabase`: connectivity, schema presence и минимальный policy probe.

### Почему это важно (риск)
False-positive readiness скрывает проблемы базы и приводит к ошибкам уже после старта runtime.

### Факты из кода (Code Facts / SSOT)
1. Текущий readiness-check покрывает sqlite путь.
2. `handle_readiness` публикует db статус из dependency слоя.
3. Для supabase нет полноценного preflight branch.

### Gap / Проблема
Readiness не подтверждает фактическую готовность Supabase.

### AC/DoD
- [ ] (P0) Добавлен supabase preflight (connectivity + key tables check).
- [ ] (P0) Добавлен минимальный policy probe/guardrail.
- [ ] (P1) Статус readiness детализирует причину `db.not_ready`.
- [ ] (P1) Добавлены unit/integration тесты readiness ветки.

### Где менять код
- `src/core/api/dependencies.py`
- `src/core/api/handlers.py`
- `tests/`

### План выполнения (Execution Plan)
1) Реализовать preflight API. 2) Интегрировать в dependency wiring. 3) Проверить контракт `/readiness`.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/test_http_readiness.py -q
```
