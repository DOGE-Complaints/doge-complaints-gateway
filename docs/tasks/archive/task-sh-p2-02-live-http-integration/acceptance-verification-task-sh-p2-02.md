# Acceptance verification — TASK-SH-P2-02

## Checklist
- [ ] Live HTTP integration bucket реализован.
- [ ] Story-first roundtrip проверяется на реальной базе.
- [ ] Сценарии корректно skip-safe без live env.

## Verification commands
- `python3 -m pytest tests/integration/supabase -q`
- `python3 -m pytest tests -k "supabase and live and http" -q`
