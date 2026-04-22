# Acceptance Verification — TASK-BP-API-01

- [x] `FastAPI` app entrypoint добавлен (`src/core/api/asgi_app.py`).
- [x] Запуск через `python3 -m core.api.asgi_app` и `uvicorn core.api.asgi_app:app`.
- [x] Routes `/health`, `/ready`, `/protected/status`, `/metrics` доступны через ASGI.
- [x] Host/port управляются env (`HOST`, `PORT`, default `8000`).
- [x] Quickstart синхронизирован.
