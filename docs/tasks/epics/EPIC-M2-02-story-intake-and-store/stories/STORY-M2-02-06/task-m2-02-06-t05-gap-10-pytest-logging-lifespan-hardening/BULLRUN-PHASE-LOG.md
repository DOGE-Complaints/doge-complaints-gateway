# BULLRUN Phase Log — TASK-M2-02-06-T05 (GAP-10)

## Phase 1 — Analysis
- [x] Prod: логирование через lifespan; pytest — без lifespan.

## Phase 2 — Decision
- [x] Session autouse в `tests/conftest.py` вызывает `configure_logging`.

## Phase 3 — Implementation
- [x] Fixture в `conftest.py`.

## Phase 4 — Verification
- [x] Регрессия intake/observability при полном pytest.

## Phase 5 — Documentation
- [x] §16 GAP-10; ссылка на `docs/runtime-docs/testing/pytest-logging-without-asgi-lifespan.md`.
