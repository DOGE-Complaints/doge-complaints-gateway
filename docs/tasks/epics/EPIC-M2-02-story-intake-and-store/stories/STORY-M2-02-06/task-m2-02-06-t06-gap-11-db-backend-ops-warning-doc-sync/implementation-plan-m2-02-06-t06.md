# План реализации — TASK-M2-02-06-T06 (GAP-11)

1. Обновить строку GAP-11 в `docs/analysis/data-model-vs-bootstrap-000-full-init-2026-05-08.md` §16: факт дефолта `in_memory`, регресс-тест, WARNING `startup.db_backend_in_memory` в `asgi_app.py`.
2. Не дублировать полный Railway runbook (cross: M2-09-05 T02).
3. Прогнать `pytest tests/test_config_loading.py` (входит в полный suite).
