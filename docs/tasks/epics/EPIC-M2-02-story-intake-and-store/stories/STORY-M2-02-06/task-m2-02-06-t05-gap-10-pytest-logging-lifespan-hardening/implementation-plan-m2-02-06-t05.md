# План реализации — TASK-M2-02-06-T05 (GAP-10)

1. Открыть `tests/conftest.py` (создать или расширить).
2. Добавить `@pytest.fixture(scope="session", autouse=True)` с вызовом `configure_logging` из `logging_setup`.
3. Убедиться, что prod `asgi_app` не меняется без необходимости.
4. Обновить §16.
