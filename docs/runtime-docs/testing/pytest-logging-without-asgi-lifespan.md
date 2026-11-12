# Логирование в pytest без ASGI lifespan

Факт из §5.4 отчёта `implementation-report-STORY-M2-02-05-bootstrap-parity-2026-05-10.md`: в типичной сессии **pytest** приложение FastAPI часто **не** проходит полный ASGI **lifespan**, поэтому `configure_logging()` из `src/core/api/asgi_app.py` (внутри `_lifespan`) **может не вызываться**. Корневой `logging` остаётся с уровнем по умолчанию (часто `WARNING`), и сообщения `DEBUG`/`INFO` из кода, завязанного на настроенный root, в выводе тестов **не видны** — это ожидаемо для unit/pytest и **не** ошибка runtime под uvicorn.

- Настройка уровня и хендлеров: `configure_logging` в `src/core/logging_setup.py`.
- Вызов из прод-пути: `lifespan=_lifespan` в `src/core/api/asgi_app.py`.

Для проверки логов в тестах используйте `caplog` / явный вызов `configure_logging` в фикстуре, либо интеграционный прогон через клиент с lifespan (см. документацию Starlette/FastAPI TestClient).
