# task-gw-public-01-t03

## Meta
- **Story:** [STORY-GW-PUBLIC-01](../STORY-GW-PUBLIC-01-public-issues-regression.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000048
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Contrast test: `POST /story-drafts` без `SERVICE_API_TOKEN` → 401. Закрывает backlog T03 и AC «T03–T04: write routes закрыты без service auth». Uses **story-drafts**, not legacy `/intake/stories`.

## Code Facts
- Write deps — [`asgi_app.py:521`](../../../../../../../../src/core/api/asgi_app.py) `POST /story-drafts` with `_STORY_DRAFT_WRITE_DEPS`
- Partial overlap: [`test_gw_draft_01_story_draft_stash_contract.py`](../../../../../../../../tests/test_gw_draft_01_story_draft_stash_contract.py) — not in dedicated M-5 module
- Legacy intake excluded per backlog — [GW-DRAFT-06](../../../../../../backlog-stories/story-draft-handoff/STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- Target module — [`tests/test_gw_public_01_public_issues_regression.py`](../../../../../../../../tests/test_gw_public_01_public_issues_regression.py)

## Acceptance / DoD
- [ ] Traces parent AC: T03–T04 write routes закрыты (T03 slice)
- [ ] Test: `POST /story-drafts` without Authorization → 401
- [ ] Test uses story-drafts path (not `/intake/stories`)
- [ ] Offline TestClient only
- [ ] [`acceptance-verification-gw-public-01-t03.md`](./acceptance-verification-gw-public-01-t03.md) signed after pytest PASS

## Where to change
- `doge-complaints-gateway/tests/test_gw_public_01_public_issues_regression.py` (add T03 contrast test)

## Out of scope
- `POST /tallinn/issues` (T04)
- `POST /story-drafts/{id}/submit` (browser auth — different layer)
- `src/core/` changes

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_public_01_public_issues_regression.py -k t03
```
