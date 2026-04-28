# Acceptance verification — TASK-SH-P0-02

## Checklist
- [ ] `DB_BACKEND=supabase` не требует `DATABASE_URL`.
- [ ] Конфигурационные ошибки детерминированы и покрыты тестами.
- [ ] Переход не ломает `in_memory` и `sqlite` контракты.

## Verification commands
- `python3 -m pytest tests/test_config_loading.py tests/test_db_backend_switching.py -q`
- `rg -n "DB_BACKEND='supabase'|DATABASE_URL" "src/core/config/schema.py"`
