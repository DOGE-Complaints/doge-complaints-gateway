# Story acceptance gate — STORY-GW-GAUTH-02

- **Story:** Introspection пользовательского токена у identity
- **Package:** `pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml`
- **Result:** PASS
- **Date:** 2026-06-25

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Для verify-гейтед действия gateway получает от identity свежий `{ active, sub, phone_verified }` по пользовательскому токену через `POST /oauth/introspect`. | PASS | T02 client + T03 `require_user_token`; T05 `test_active_verified_introspection_allows_intake` |
| Gateway предъявляет identity свой сервисный токен (иначе identity отвечает 401/403). | PASS | T01 env + T02 `Authorization: Bearer`; T05 `test_introspect_client_posts_form_with_service_bearer` |
| Статус не берётся из тела токена. | PASS | T02 `_parse_introspection_body`; T05 `test_phone_verified_comes_from_identity_not_payload_jwt` |
| Identity недоступен/ответ невалиден/`active=false` → **безопасный отказ** (fail-closed, D-GAUTH-4). | PASS | T04 policy; T05 inactive/down/not-configured tests |
| Контракт ответа соответствует построенному identity ([`introspection.py`](../../../../../../../../../doge-identity-service/src/core/oauth/introspection.py)). | PASS | T02 parse active/inactive; matches identity shape |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q -m 'not live_integration'
```

**Live run (2026-06-25):** gauth-02 contract 8 passed; unit suite 542 passed, 12 skipped.

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
