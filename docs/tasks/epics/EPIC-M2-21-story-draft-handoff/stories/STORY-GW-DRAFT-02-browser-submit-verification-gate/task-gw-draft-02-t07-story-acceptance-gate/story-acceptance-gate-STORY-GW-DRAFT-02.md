# Story acceptance gate — STORY-GW-DRAFT-02

- **Story:** Браузер-сабмит истории + гейт phone_verified
- **Package:** `pkg-000044-20260703-gw-draft-02-browser-submit-verification-gate.yaml`
- **Result:** PASS
- **Date:** 2026-07-03

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Браузер + `phone_verified=true` → 202, `submitter=sub` | PASS | T03, T05 — `test_verified_browser_submit_returns_202_and_authoritative_submitter` |
| `phone_verified=false` → 403 + `verify_url` | PASS | T03, T05 — `test_unverified_returns_403_verification_required` |
| Нет/битый токен → 401; identity down → 503 | PASS | T01, T03, T05 — `test_missing_bearer_*`, `test_inactive_*`, `test_identity_me_down_*` |
| Повторный submit `draft_id` идемпотентен | PASS | T04, T05 — `test_repeat_submit_is_idempotent` |
| `draft_id` unknown/expired → 404 | PASS | T02, T04, T05 — `test_unknown_draft_returns_404` |
| Проверка через identity `/me` (не local JWT) | PASS | T01, T05 — `IdentityMeClient` + contract tests (no Supabase JWT in gateway) |
| GET draft requires browser session (audit G1) | PASS | T08–T10 — `require_story_draft_read_user`; `test_gw_draft_02_get_auth_contract.py` |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_story_draft_submit_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_02_get_auth_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```

**Live run:** verify ok 7 paths; submit 7 passed; get-auth 6 passed; full unit 574 passed (2026-07-03)

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
