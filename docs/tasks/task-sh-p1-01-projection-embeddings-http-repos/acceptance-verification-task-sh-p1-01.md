# Acceptance verification — TASK-SH-P1-01

## Checklist
- [ ] Все projection/embedding stores в supabase режиме работают через HTTP.
- [ ] Семантика source checksum и policy version сохранена.
- [ ] Regression тесты зелёные.

## Verification commands
- `python3 -m pytest tests -k "projection and embedding and supabase" -q`
