# Story acceptance gate — STORY-GW-DRAFT-05

- **Story:** Dual intake contract (stash vs submit)
- **Package:** `pkg-000049-20260711-gw-draft-05-dual-intake-contract-stash-vs-submit.yaml`
- **Result:** PASS
- **Date:** 2026-07-11

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| `STASH_PENDING_EXTERNAL_USER_ID` и `require_submitter` **удалены**; legacy `__stash_pending_author__` только в tolerant-read (`_LEGACY_*` + `_normalize_stored_draft_payload`) | PASS | T01–T04, T09; `rg 'STASH_PENDING\|require_submitter\|\bstash_pending\b'` = 0; literal 1 hit in `contracts.py:18` |
| `parse_story_draft_stash_request` возвращает **`StoryDraftStashRequest`**, не `StoryIntakeRequest` | PASS | T01; `test_story_intake_contract.py` |
| `POST /story-drafts` принимает payload **без submitter**; stored JSON **не содержит** submitter/placeholder | PASS | T02, T04; `test_gw_draft_01_story_draft_stash_contract.py` |
| `POST /story-drafts/{id}/submit` собирает `StoryIntakeRequest` только на границе submit с authoritative submitter из `/me` | PASS | T02, T04; `test_gw_draft_02_story_draft_submit_contract.py` |
| Runtime OpenAPI и security SSOT описывают **два** request-контракта (stash vs intake bridge), lockstep с GPT OpenAPI v0.6.0 | PASS | T05, T06 |
| Контракт-тесты GW-DRAFT-01/02 + intake contract зелёные; нет assert на magic placeholder | PASS | T04, T09; 35 contract tests; legacy test uses imported constant |

## Commands (live verification 2026-07-11)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
cd doge-complaints-gateway && python3 -m pytest -q -m "not live_integration"
cd doge-complaints-gateway && rg 'STASH_PENDING|require_submitter|\bstash_pending\b' src/ tests/ || test $? -eq 1
cd doge-complaints-gateway && rg '__stash_pending_author__' src/core/intake/contracts.py
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_01_story_draft_stash_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py tests/test_story_intake_contract.py
```

**Live run:** verify ok 8 paths; date-check ok; pytest **570 passed**, 12 skipped; active-token grep = 0; legacy literal 1 hit; contract suite 35 passed

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
