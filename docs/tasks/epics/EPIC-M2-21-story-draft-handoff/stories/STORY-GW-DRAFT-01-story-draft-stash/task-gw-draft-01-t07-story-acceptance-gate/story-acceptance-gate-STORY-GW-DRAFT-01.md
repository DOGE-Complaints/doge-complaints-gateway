# Story acceptance gate — STORY-GW-DRAFT-01

- **Story:** Стеш черновика истории (create + fetch)
- **Package:** `pkg-000043-20260703-gw-draft-01-story-draft-stash.yaml`
- **Result:** PASS
- **Date:** 2026-07-03

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| POST + `{draft_id}`, no issue | PASS | T03, T05 — `test_post_story_drafts_returns_draft_id_without_creating_story` |
| 401 без сервисного токена | PASS | T03, T05 — `test_post_story_drafts_requires_service_token` |
| GET payload / 404 | PASS | T04, T05 — GET contract tests |
| 400 invalid contract | PASS | T03, T05 — `DOMAIN_ERROR` (same as `/intake/stories`) |
| TTL → 404 | PASS | T02, T05 — `test_get_story_drafts_expired_draft_returns_404` |
| Отдельный StoryDraftRepository | PASS | T01, T02 — port + 3 adapters |

## Commands (live verification)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```

**Live run:** verify ok 7 paths; draft contract pytest 7 passed; full unit 561 passed (2026-07-03)

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
