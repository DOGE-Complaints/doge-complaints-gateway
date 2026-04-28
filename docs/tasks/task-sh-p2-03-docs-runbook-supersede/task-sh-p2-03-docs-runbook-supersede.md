## Task: docs — Runtime docs, runbook and DSN supersede map for Supabase HTTP

Key: TASK-SH-P2-03  
Priority: P2  
Status: Todo  
Closes: SH-DOCS-HTTP-01  
Supersedes: TASK-DB-CONFIG-SUPABASE-02, TASK-DB-SUPABASE-REPOS-02, TASK-DB-READINESS-SUPABASE-02  
Decision Ref: `docs/runtime-docs/server-env-quickstart.md`

### Goal
Синхронизировать документацию после HTTP-migration и формализовать supersede mapping DSN-wave -> HTTP-wave.

### AC/DoD
- [ ] Runtime docs и env runbook отражают HTTP-native supabase режим.
- [ ] В индекс/таски добавлен явный supersede map.
- [ ] Команды локального/railway запуска обновлены без DSN зависимости для supabase backend.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
rg -n "DATABASE_URL|SUPABASE_URL|SUPABASE_SERVICE_ROLE|HTTP" docs/runtime-docs docs/tasks
```
