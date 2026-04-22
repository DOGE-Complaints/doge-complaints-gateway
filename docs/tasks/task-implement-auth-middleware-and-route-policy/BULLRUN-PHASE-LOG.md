# BULLRUN Phase Log — TASK-BP-API-02

## Phase 1 — Analysis
- Подтвержден риск ad-hoc auth в handlers без единой route policy.

## Phase 2 — Implementation
- В `src/core/api/asgi_app.py` добавлены декларативные карты:
  - `PUBLIC_ROUTES`
  - `PROTECTED_ROUTES`
- Для protected routes включен dependency guard `require_service_auth`.
- Unauthorized ответы унифицированы через envelope contract.

## Phase 3 — Verification
- Добавлены проверки policy enforcement в `tests/test_http_transport_smoke.py`.

## Phase 4 — Documentation
- Обновлены security/runtime/openapi документы под transport policy.
