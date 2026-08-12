# Acceptance verification — task-m2-09-05-trace-observability-primary

## AC checklist
- [x] Story gate закрыт, все trace-gap задачи покрыты в task artifacts.

## Verification commands
```bash
cd doge-complaints-gateway && pytest -q tests/test_config_loading.py tests/test_api_security_and_ops.py tests/test_intake_observability.py
```

## Verification performed
- `src/core/logging_setup.py` добавлен с `configure_logging()`, context-filter и `StoryDebugFileHandler`.
- `src/core/api/asgi_app.py` применяет `LOG_LEVEL/LOG_FORMAT/LOG_DEBUG_DIR` и пишет `startup.config`.
- `src/core/api/handlers.py`, `src/core/application/services.py`, `src/core/infrastructure/db_supabase.py` покрыты intake/supabase DEBUG trace.
- `src/core/application/cluster_orchestrator.py`, `src/core/geo/service.py`, `src/core/application/issue_create.py` покрыты cluster/geo/issue trace.
- PII-safe логирование подтверждено: полный `narrative_original_text` не логируется, используется только preview/length.
- Тесты: `34 passed` (`pytest -q tests/test_config_loading.py tests/test_api_security_and_ops.py tests/test_intake_observability.py`).
