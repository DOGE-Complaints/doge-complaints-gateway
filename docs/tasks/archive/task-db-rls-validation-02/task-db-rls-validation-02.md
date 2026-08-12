## Task: test — automated RLS validation for Supabase

### Цель
Построить автоматизированные integration проверки deny-by-default и allow для service role на ключевых таблицах DB-контура.

### Почему это важно (риск)
Без test-доказательств RLS policies могут быть формально добавлены, но не гарантировать реальную изоляцию доступа.

### Факты из кода (Code Facts / SSOT)
1. Миграция RLS baseline существует в `supabase/migrations`.
2. Отдельного набора `tests/integration/supabase` под policy scenarios нет.
3. Текущие e2e покрывают sqlite pipeline.

### Gap / Проблема
Отсутствует runtime-подтверждение корректности RLS/policy поведения.

### AC/DoD
- [ ] (P0) Добавлены integration tests на deny-by-default для anon/auth role.
- [ ] (P0) Добавлены integration tests на allow для service_role.
- [ ] (P1) Проверены сценарии для stories/projections/embeddings tables.
- [ ] (P1) Тесты запускаются отдельным supabase bucket.

### Где менять код
- `supabase/migrations/`
- `tests/integration/supabase/`

### План выполнения (Execution Plan)
1) Формализовать policy scenarios. 2) Добавить live policy tests. 3) Синхронизировать verification команды.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/integration/supabase -q
```
