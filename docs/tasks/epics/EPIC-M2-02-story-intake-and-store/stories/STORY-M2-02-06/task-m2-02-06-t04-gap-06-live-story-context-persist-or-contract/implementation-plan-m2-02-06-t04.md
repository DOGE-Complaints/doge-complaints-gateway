# План реализации — TASK-M2-02-06-T04 (GAP-06)

1. Добавить `narrative_consistency_notes` в `StoryRecord`.
2. В `StoryIntakeService.create_story` читать `request.live_story_context` и маппить `consistency_notes`.
3. Расширить `save_story` / чтение строк в `db_supabase.py` и `db_sqlite.py`.
4. SQL: колонка в bootstrap и миграции.
5. Обновить тесты на round-trip.
