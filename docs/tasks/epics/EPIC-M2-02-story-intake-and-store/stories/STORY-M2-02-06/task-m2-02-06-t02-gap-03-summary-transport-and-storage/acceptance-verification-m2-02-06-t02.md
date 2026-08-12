# Верификация приёмки — TASK-M2-02-06-T02

| AC | Уровень | Формулировка | Код / тесты | Статус |
|----|---------|--------------|-------------|--------|
| Хранение summary | P0 | JSON в БД | `narrative_summary_json`, migration | OK |
| Парсинг | P0 | Объект et/ru/en | `parse_story_intake_request` | OK |
| Тесты | P1 | Round-trip / bootstrap | `test_story_intake_live_context_not_on_record.py`, `test_supabase_bootstrap_schema.py` | OK |

`python3 -m pytest -q` — **239 passed, 10 skipped**.
