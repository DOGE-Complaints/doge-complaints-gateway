# План реализации — TASK-M2-02-06-T03 (GAP-04)

1. Убедиться, что gateway парсит `origin` (уже есть в `parse_story_intake_request`).
2. Обновить `GPT UI/instructions/api-orchestrator.md` §5.2.1: поле `origin` в минимальном примере и строки таблицы маппинга → колонки `public.stories`.
3. Подтвердить зелёный `pytest` для intake contract.

Gateway-код менять не требуется при совпадении имён полей с парсером.
