# Story acceptance gate — STORY-GW-DRAFT-06

- **Story:** Удаление legacy `POST /intake/stories`
- **Package:** `pkg-000050-20260711-gw-draft-06-remove-legacy-intake-stories-route.yaml`
- **Result:** PASS
- **Date:** 2026-07-11T10:15:42Z

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `rg 'POST /intake/stories\|"/intake/stories"' src/` → **0** matches (публичный route удалён) | PASS | T01; `asgi_app.py` route removed |
| `simulation_runner.py` использует `/story-drafts`, не `/intake/stories` | PASS | T03; stash-only 201 + `draft_id` |
| `handle_story_intake` вызывается только из submit/internal path (не из удалённого route) | PASS | T01; `handlers.py` submit-bridge |
| OpenAPI не описывает публичный `POST /intake/stories` | PASS | T02; `openapi.yaml` path removed |
| Контракт-тесты GW-DRAFT-01/02 + full pytest green | PASS | T04–T06; 565 offline + 16 contract |

## Commands (live verification 2026-07-11)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && rg 'POST /intake/stories|"/intake/stories"' src/ || test $? -eq 1
cd doge-complaints-gateway && rg '"/intake/stories"' tests/ || test $? -eq 1
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py
```

**Live run:** verify ok 6 paths; date-check ok; pytest **565 passed**, 12 skipped; GW-DRAFT-01/02 **16 passed**; src grep 0; tests grep 0 (1 negative assert in openapi compliance)

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
