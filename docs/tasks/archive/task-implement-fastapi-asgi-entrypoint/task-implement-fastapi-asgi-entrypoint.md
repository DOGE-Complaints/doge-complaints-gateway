## Task: implement — FastAPI ASGI entrypoint for runtime API

### Цель
Добавить production-grade transport entrypoint на базе ASGI (`FastAPI` + `uvicorn`) для `doge-complaints-gateway`, чтобы запуск API происходил через типичный серверный стек Python, а не через ad-hoc `http.server`.

### Почему это важно (риск)
Ранее использовался ad-hoc HTTP transport без ASGI baseline; это не задаёт устойчивый production-like контур для middleware, observability, dependency injection и дальнейшего расширения API surface.

### Scope
Входит:
- создание `FastAPI` app entrypoint в `src/core/api`;
- запуск через `uvicorn` с host/port из env/config;
- перенос текущих handler операций в ASGI route layer без изменения бизнес-логики handler-ядра.

Не входит:
- полная миграция всех planned endpoints в HTTP transport;
- инфраструктурный деплой (docker/k8s/systemd).

### Факты из кода (Code Facts / SSOT)
1) `pyproject.toml`
- Runtime dependencies включают `fastapi` и `uvicorn`.
- Dev extras включают `pytest` и `httpx` (для transport smoke через `TestClient`).

2) `src/core/api/asgi_app.py`
- ASGI entrypoint: `FastAPI` app, route binding, env-driven `run_asgi_server`.

3) `src/core/api/handlers.py`
- Операции boundary представлены функциями:
  - `handle_health`
  - `handle_readiness`
  - `handle_protected_status`
  - `handle_metrics`

4) `docs/runtime-docs/server-env-quickstart.md`
- Локальный запуск сервера: `python3 -m core.api.asgi_app` или `uvicorn core.api.asgi_app:app`.

### Gap / Проблема
- Нет стандартизированного ASGI entrypoint.
- Нет framework-native route lifecycle/middleware model.
- Нет типичного `uvicorn`-запуска, который ожидают backend-разработчики и tooling.

### AC/DoD
- [x] (P0) В `src/core/api` добавлен `FastAPI` entrypoint (`app`).
- [x] (P0) Реализован запуск `uvicorn` через documented команду (`python -m ...` или `uvicorn module:app`).
- [x] (P0) Текущие runtime операции `/health`, `/ready`, `/protected/status`, `/metrics` доступны через ASGI routes.
- [x] (P0) Host/port задаются через env (включая `PORT`) и documented defaults.
- [x] (P1) `docs/runtime-docs/server-env-quickstart.md` обновлен под ASGI запуск.

### Где менять код
- `pyproject.toml` (добавить runtime dependency stack для ASGI).
- `src/core/api/`:
  - модуль ASGI app (`asgi_app.py`).
- `docs/runtime-docs/server-env-quickstart.md`

### План выполнения (Execution Plan)
1) Добавить зависимости `fastapi` и `uvicorn`.
2) Создать ASGI app и route binding к существующим handler-функциям.
3) Добавить env-driven host/port policy.
4) Прогнать smoke-запуск и базовые route checks.
5) Обновить quickstart документацию.

### Команды проверки (Verification Commands)
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pip install -e '.[dev]'
python3 -m pytest tests/test_bootstrap_smoke.py tests/test_api_security_and_ops.py -q
```
