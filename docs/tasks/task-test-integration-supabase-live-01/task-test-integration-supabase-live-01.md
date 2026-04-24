## Task: tests — live supabase integration pipeline

### Цель
Собрать отдельный integration bucket `tests/integration/supabase/` для end-to-end проверки live DB контура: migrations, repositories, RLS и API pipeline.

### Почему это важно (риск)
Без live integration слоя нельзя доказать рабочий Supabase-native runtime в условиях, близких к production.

### Факты из кода (Code Facts / SSOT)
1. Есть миграции supabase schema и RLS.
2. Текущий DB-backed e2e ориентирован на sqlite режим.
3. План целевого состояния требует live DB integration bucket.

### Gap / Проблема
Отсутствует интеграционный тестовый пакет на реальной Supabase базе.

### AC/DoD
- [ ] (P0) Создан bucket `tests/integration/supabase/`.
- [ ] (P0) Тесты проверяют `intake -> issues -> projection` на live DB.
- [ ] (P0) Тесты включают migration/schema readiness и RLS expectations.
- [ ] (P1) Добавлены команды запуска bucket в task docs/index.

### Где менять код
- `tests/integration/supabase/`
- `docs/tasks/`

### План выполнения (Execution Plan)
1) Подготовить fixtures live supabase. 2) Реализовать pipeline integration tests. 3) Добавить запуск в quality gates.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests/integration/supabase -q
```
