# Acceptance verification — TASK-SH-P0-01

## Checklist
- [ ] Supabase HTTP transport boundary добавлен и используется как единая точка доступа.
- [ ] Auth header (`service role`) и timeout/retry policy покрыты тестами.
- [ ] Нет прямой зависимости репозиториев на низкоуровневые HTTP детали.

## Verification commands
- `rg -n "class .*Supabase.*Http|PostgREST|Authorization" "src/core/infrastructure"`
- `python3 -m pytest tests -k "supabase and http and transport" -q`
