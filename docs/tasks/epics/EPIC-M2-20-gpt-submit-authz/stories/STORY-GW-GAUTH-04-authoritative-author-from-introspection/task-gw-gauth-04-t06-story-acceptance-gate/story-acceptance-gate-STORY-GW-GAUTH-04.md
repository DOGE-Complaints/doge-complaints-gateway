# Story acceptance gate — STORY-GW-GAUTH-04

- **Story:** Авторитетный автор = `sub` из introspection (сверка с submitter/req-19)
- **Package:** `pkg-000042-20260625-gw-gauth-04-authoritative-author-introspection.yaml`
- **Result:** PASS
- **Date:** 2026-06-25

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Автор сохранённой истории соответствует `sub` из introspection. | PASS | T02/T05 — `test_verified_introspection_persists_sub_not_payload`; persisted `submitter_external_user_id` == introspected `sub` |
| При расхождении payload-submitter ↔ introspected `sub` — приоритет у `sub` (зафиксировано в контракте). | PASS | T03/T05 — `story_intake_submitter_mismatch` log + `test_mismatch_payload_submitter_sub_wins` |
| Формулировка авторства согласована с [`req-19 §5`](../../../../../../../requirements/19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md) (единый источник, без параллельной модели). | PASS | T04 — §5.3 GW-GAUTH-04 bullet |
| Кейс «нет introspection» не порождает историю с payload-автором (следствие fail-closed D-GAUTH-4). | PASS | T05 — 401 inactive / 403 unverified; story count unchanged |

## Commands (live verification 2026-06-25)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_04_authoritative_author_contract.py
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
