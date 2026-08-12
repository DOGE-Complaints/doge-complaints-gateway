# Story acceptance gate — STORY-GW-GAUTH-03

- **Story:** Гейт верификации + `verification_required` (403)
- **Package:** `pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml`
- **Result:** PASS
- **Date:** 2026-06-25

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `phone_verified == false` → **403 `verification_required`**, история не создаётся. | PASS | T04/T05 — `test_unverified_returns_403_verification_required_oauth04`, story count unchanged |
| Ответ содержит `verify_url` / контекст (куда вести пользователя), по канону OAUTH-04. | PASS | T01/T03/T05 — `error.details.verify_url` from `SPA_VERIFY_BASE_URL` |
| `active == true && phone_verified == true` → история создаётся (happy path). | PASS | T05 — `test_verified_introspection_allows_intake` → 202 |
| `active == false` (битый/просроченный токен) → **401** (отделён от verification_required). | PASS | T05 — `test_inactive_token_returns_401_not_verification_required` |
| Identity недоступен → отказ (fail-closed), не `verification_required`. | PASS | T05 — 503 on identity down / missing config |
| Формат `verification_required` совпадает с каноном identity (OAUTH-04). | PASS | T03/T05 — `details.error`, `reason`, `verify_url` |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_03_verification_gate_contract.py
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
