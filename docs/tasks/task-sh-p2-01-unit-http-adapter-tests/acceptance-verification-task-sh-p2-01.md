# Acceptance verification — TASK-SH-P2-01

## Checklist
- [ ] Unit coverage закрывает ошибки HTTP транспорта.
- [ ] Unit coverage закрывает контракты всех Supabase HTTP repositories.
- [ ] CI unit bucket проходит стабильно.

## Verification commands
- `python3 -m pytest tests -k "supabase and http and unit" -q`
