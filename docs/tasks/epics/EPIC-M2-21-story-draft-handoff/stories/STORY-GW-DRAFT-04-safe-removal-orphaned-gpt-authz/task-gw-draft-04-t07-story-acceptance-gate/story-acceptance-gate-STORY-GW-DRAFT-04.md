# Story acceptance gate — STORY-GW-DRAFT-04

- **Story:** Безопасное удаление осиротевшего кода gpt-submit-authz
- **Package:** `pkg-000046-20260703-gw-draft-04-safe-removal-orphaned-gpt-authz.yaml`
- **Result:** PASS
- **Date:** 2026-07-03

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Осиротевший код (OAuth-introspection-клиент, env `IDENTITY_INTROSPECT_URL/SERVICE_TOKEN`, GPT-`require_user_token`-путь) удалён; `grep` остаточных потребителей = 0 | PASS | T03–T04; `rg` orphans=0 in `src/` |
| Переиспользуемое (`verification_gate`, `verify_url`, `authoritative_submitter`, `IntrospectionResult`) работает; GW-DRAFT-02 зелёный | PASS | T02 `introspection_result.py`; draft_02 contract tests green |
| Тест-суит **зелёный после** удаления (не за счёт удаления живых тестов) | PASS | T05; **557 passed**, 21 skipped (1 live_integration fail-closed) |
| `/intake/stories` и `/tallinn/issues` — user-слой явно разрешён (переключён/снят) по T01, без «висящих» зависимостей | PASS | T01/T04 service-only deps |
| История не тронута: `docs/analysis/audit-gw-gauth-*`, `pkg-000039..042`, run-summary — на месте (D-DRAFT-6) | PASS | T07 `test -f` audits + pkg-000039/042 |
| `simulation_runner.py`/seed-доки согласованы с новой моделью | PASS | T06; no `GATEWAY_USER_TOKEN` in runner |

## Commands (live verification 2026-07-03)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && PYTHONPATH=src:. pytest -q
rg 'IdentityIntrospectionClient|require_user_token|IDENTITY_INTROSPECT_URL' src/ || test $? -eq 1
```

**Live run:** verify ok 7 paths; date-check ok; pytest 557 passed; grep orphans=0

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
