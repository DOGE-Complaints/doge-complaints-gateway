# Acceptance verification — TASK-SH-P0-03

## Checklist
- [ ] Stories CRUD/upsert контракты сохранены на HTTP path.
- [ ] Idempotency dedup контракты сохранены на HTTP path.
- [ ] DI wiring для supabase backend переключен на HTTP implementations.

## Verification commands
- `python3 -m pytest tests -k "story and idempotency and supabase" -q`
- `rg -n "psycopg.connect" "src/core/infrastructure"`
