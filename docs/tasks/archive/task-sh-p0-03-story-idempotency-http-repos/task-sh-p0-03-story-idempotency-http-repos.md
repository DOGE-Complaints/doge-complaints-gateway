## Task: implement — Stories and idempotency repositories via Supabase HTTP

Key: TASK-SH-P0-03  
Priority: P0  
Status: Todo  
Closes: SH-REPO-HTTP-01  
Supersedes: TASK-DB-SUPABASE-REPOS-02  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Мигрировать `stories` и `idempotency_keys` репозитории с DSN/SQL пути на HTTP client.

### Code facts
1. `SupabaseStoryRepository`/`SupabaseIdempotencyRepository` в `db_supabase.py` используют SQL запросы через курсор.
2. Ветка `DB_BACKEND='supabase'` в `providers.py` создает SQL-ориентированные репозитории.
3. Story intake и idempotency являются критическим входом для story-first pipeline.

### AC/DoD
- [ ] Stories repository работает через HTTP без `psycopg.connect`.
- [ ] Idempotency repository работает через HTTP и сохраняет контракт dedup.
- [ ] DI/providers используют HTTP реализации при supabase backend.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "story and idempotency and supabase" -q
rg -n "SupabaseStoryRepository|SupabaseIdempotencyRepository|psycopg.connect" src/core/infrastructure
```
