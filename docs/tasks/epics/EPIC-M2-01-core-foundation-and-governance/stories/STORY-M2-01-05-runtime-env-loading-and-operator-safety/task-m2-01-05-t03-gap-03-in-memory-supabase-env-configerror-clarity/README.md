## Task workspace — `task-m2-01-05-t03-gap-03-in-memory-supabase-env-configerror-clarity`

- Story: [`../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md`](../STORY-M2-01-05-runtime-env-loading-and-operator-safety.md)
- Decision Ref: [`../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md`](../../../../../../docs/analysis/gap-analysis-env-loading-target-state-2026-05-12.md) — **§5 GAP-03**, вариант **B** (информативное сообщение)

## Task: fix — ясный `ConfigError` при `in_memory` + Supabase env

### Цель
При `DB_BACKEND=in_memory` (дефолт) и одновременно заданных `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE` / `DATABASE_URL` сейчас fail-fast через `ConfigError` (H2). Улучшить текст ошибки (вариант B аудита), без ослабления политики «не смешивать in_memory с облачными кредами».

### Факты из кода
1. [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py) — проверка около сообщения `DB_BACKEND='in_memory' does not allow SUPABASE_URL/...` (см. grep по файлу).
2. [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py) — существующие негативные сценарии конфига.

### Gap / Проблема
GAP-03: сообщение не подсказывает исправление (`DB_BACKEND=supabase` или unset переменных).

### AC/DoD
- [ ] (P0) Новое/уточнённое сообщение `ConfigError` с явной подсказкой (как в §5 вариант B Decision Ref).
- [ ] (P1) Тест обновлён или добавлен: при триггере этой валидации текст содержит ключевые подсказки (или снимок сообщения зафиксирован в assert).
- [ ] (P2) Одна строка в `server-env-quickstart.md` или Decision Ref cross-link — по желанию.

### Где менять код
- [`src/core/config/schema.py`](../../../../../../src/core/config/schema.py)
- [`tests/test_config_loading.py`](../../../../../../tests/test_config_loading.py)

### Команды проверки
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_config_loading.py -q --tb=short
```
