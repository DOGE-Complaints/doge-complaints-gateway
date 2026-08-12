# План реализации — TASK-M2-02-06-T02 (GAP-03)

1. `intake/contracts.py` — структура `narrative.summary.{et,ru,en}` → `summary_languages: tuple[tuple[str,str],...]`.
2. `domain/contracts.py` — `narrative_summary_json: str | None`.
3. `services.py` — `json.dumps` при наличии summary.
4. `db_supabase.py` / `db_sqlite.py` — поле в payload и чтение строки.
5. SQL: bootstrap `ALTER TABLE` + файл миграции `20260511_1200_*`.
6. Тесты: расширение `test_story_intake_live_context_not_on_record.py` и bootstrap asserts.

DoD: полный pytest зелёный.
