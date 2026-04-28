## Task: implement — Supabase HTTP client bootstrap and transport abstraction

Key: TASK-SH-P0-01  
Priority: P0  
Status: In Progress  
Closes: SH-ARCH-HTTP-01  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Ввести единый HTTP-транспорт Supabase (PostgREST) и общий клиент для инфраструктурных репозиториев.

### Why it matters (risk)
Без общего транспорта миграция распадется на ad-hoc HTTP вызовы и создаст новый инфраструктурный дрейф.

### Code facts
1. `src/core/infrastructure/db_supabase.py` использует `psycopg.connect(...)` через DSN.
2. `src/core/infrastructure/providers.py` конструирует Supabase backend через `SupabaseDatabase.from_url(database_url)`.
3. `src/core/config/schema.py` уже содержит `SUPABASE_URL` и `SUPABASE_SERVICE_ROLE`, но runtime слой не использует их как основной канал.

### Gap
Отсутствует единый Supabase HTTP adapter boundary для безопасной замены DSN-репозиториев.

### Scope
- `src/core/infrastructure/` (новый HTTP transport/client модуль)
- `src/core/infrastructure/providers.py` (подготовка точки интеграции)
- базовые tests для transport уровня

### AC/DoD
- [ ] Добавлен общий Supabase HTTP client с auth headers и timeout.
- [ ] Добавлена транспортная абстракция без знания бизнес-репозиториев о деталях HTTP.
- [ ] Добавлены unit tests на success/error/timeout retry path.

### Execution plan
1. Ввести transport/client boundary и базовые DTO ответа/ошибки.
2. Реализовать конфигурирование через `SUPABASE_URL` и `SUPABASE_SERVICE_ROLE`.
3. Подготовить integration points для последующих TASK-SH-P0/P1.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
rg -n "SUPABASE_URL|SUPABASE_SERVICE_ROLE|http|postgrest" src/core/infrastructure
python3 -m pytest tests -k "supabase and http and transport" -q
```
