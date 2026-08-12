# Acceptance verification — TASK-SH-P2-03

## Checklist
- [ ] Runtime docs обновлены под Supabase HTTP client.
- [ ] DSN-wave -> HTTP-wave supersede map зафиксирован в task governance.
- [ ] Команды запуска/диагностики консистентны с новым режимом.

## Verification commands
- `rg -n "TASK-SH|Supersedes|DATABASE_URL|SUPABASE_URL|SUPABASE_SERVICE_ROLE" "docs/tasks" "docs/runtime-docs"`
