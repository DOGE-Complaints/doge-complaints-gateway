## Task: implement — schema bootstrap и migration-baseline для Supabase

### Цель
Ввести воспроизводимый DB bootstrap через миграции для целевых таблиц stories/projections/embeddings и связей.

### Почему это важно (риск)
Без migration baseline сохраняется schema drift и невозможно стабильно разворачивать DB слой между окружениями.

### Scope
Входит: структура каталогов миграций, initial DDL, базовые расширения (`pgvector`), rollback-подход.
Не входит: SQL-backed runtime repositories.

### Факты из кода (Code Facts / SSOT)
1. В анализе зафиксировано отсутствие SQL/migrations/supabase config: `docs/analysis/supabase-db-layer-audit-and-target-state.md`.
2. В runtime сейчас только in-memory persistence: `src/core/infrastructure/providers.py`.
3. Целевые таблицы определены в анализе (stories, embeddings, projections): `docs/analysis/supabase-db-layer-audit-and-target-state.md`.

### Gap / Проблема
`GAP-DB-002`: нет DDL/migrations и schema bootstrap слоя.

### Decision Points
- **PM decision:** включить минимальный demo-ready набор таблиц в первую миграцию.
- **CTO decision:** migration-first, без «ручного SQL вне истории».
- **Options A/B:** одна большая миграция vs по-доменные миграции.
- **Recommendation:** по-доменные миграции с явными зависимостями.

### AC/DoD
- [ ] (P0) Создан migration baseline для таблиц и ключей целевого контура.
- [ ] (P0) Включены расширения для embeddings (pgvector).
- [ ] (P0) Зафиксированы up/down и порядок применения.
- [ ] (P1) Документирован минимальный bootstrap runbook.

### Где менять код
- `supabase/` (новая структура проекта/миграций)
- `docs/analysis/` (ссылки на migration baseline)
- `docs/tasks/` (phase/acceptance артефакты)

### План выполнения (Execution Plan)
1) Ввести структуру миграций. 2) Описать DDL по доменам. 3) Верифицировать порядок применения. 4) Зафиксировать runbook.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
# команды применения миграций/валидации будут добавлены в реализации task
```
