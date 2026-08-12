# Верификация приёмки — TASK-M2-02-06-T01

| AC | Уровень | Формулировка | Код / тесты | Статус |
|----|---------|--------------|-------------|--------|
| P0 | P0 | Три опциональных языка title в intake и домене | `intake/contracts.py`, `domain/contracts.py`, `services.py` | OK |
| P0 | P0 | Персистенция в SQLite и Supabase | `db_sqlite.py`, `db_supabase.py`, SQL | OK |
| P1 | P1 | Регресс парсинга и round-trip narrative extensions | `test_story_intake_live_context_not_on_record.py`, bootstrap tests | OK |

Прогон: `python3 -m pytest -q` (2026-05-11) — **239 passed, 10 skipped**.
