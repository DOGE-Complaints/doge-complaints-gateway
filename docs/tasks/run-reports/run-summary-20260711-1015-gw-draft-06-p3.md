---
generated_utc: 2026-07-11T10:15:42Z
builder_project: gateway
pkg: pkg-000050-20260711-gw-draft-06-remove-legacy-intake-stories-route
story: STORY-GW-DRAFT-06
phase: P3
artifact_kind: run_summary
---

# Run summary — GW-DRAFT-06 P3 execute (pkg-000050)

**Window:** flat T01→T06  
**Result:** PASS  
**Date:** 2026-07-11T10:15:42Z

## Delivered

- Removed public `POST /intake/stories` from `asgi_app.py` and `PUBLIC_ROUTES`
- Runtime OpenAPI + SSOT docs → story-drafts-only GPT write path
- `simulation_runner.py` → `POST /story-drafts` stash-only (201 + `draft_id`)
- Retired `test_http_intake_endpoint.py`; migrated ~25 test files via `story_draft_intake_helpers.py`
- Story gate signed; `--verify --check-dates` ok

## Verification

```
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates → ok
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration" → 565 passed, 12 skipped
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py → 16 passed
rg intake/stories src/ → 0
```

## Follow-up (out of scope)

- GW-SEED-01: runner submit/cluster + hosted demo seed
- Stale `/intake/stories` mentions in bootstrap/manuals docs (non-runtime-docs)
