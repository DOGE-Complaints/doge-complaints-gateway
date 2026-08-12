# task-gw-draft-07-t05-browser-submit-smoke-and-evidence

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** verify
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Backlog T05 (smoke + evidence): verified browser `POST /story-drafts/{id}/submit` on filled draft → **202** + `story_id`; retry consumed draft → 404/expired; write sanitized evidence under `doge-complaints-gateway/docs/analysis/`.

## Code Facts
- Submit → intake — [`handlers.py`](../../../../../../../../src/core/api/handlers.py) `handle_story_draft_submit` → `handle_story_intake`
- db_ready gate — [`handlers.py:159-182`](../../../../../../../../src/core/api/handlers.py) `story_intake_rejected_db_not_ready` → 503 when not ready
- Idempotency replay — [`handlers.py:656-688`](../../../../../../../../src/core/api/handlers.py) `_story_intake_replay_from_idempotency` → **202** same story (GW-DRAFT-02 T04)
- Prior fail evidence — [`evidence-STORY-SPA-BUG-01-submit-http-2026-08-06T201810Z.md`](../../../../../../../../spa-app/docs/analysis/evidence-STORY-SPA-BUG-01-submit-http-2026-08-06T201810Z.md)

## Acceptance / DoD
- [x] Traces parent AC #2: Submit → **202** (not 503 `service_down` on happy path)
- [x] Traces parent AC #3: no false second publish (as-built: retry **202** + same `story_id` via idempotency; GET draft → **404**)
- [x] Traces parent AC #4: evidence artifact in `doge-complaints-gateway/docs/analysis/` (sanitized ready JSON + submit 202 `trace_id`)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t05.md`](./acceptance-verification-gw-draft-07-t05.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/analysis/evidence-STORY-GW-DRAFT-07-*.md` (new evidence file)
- Live hosted gateway + verified SPA session — no FE hotfix

## Out of scope
- Story acceptance gate signing (T06); SPA UI mapping fixes; GPT OpenAPI; identity

## Verification commands
```bash
# Verified user + filled draft (browser or curl with user bearer):
# POST https://dogestonia-tallinn.up.railway.app/story-drafts/{id}/submit → 202 + story_id
# POST same draft again → 404/expired
# Write sanitized evidence under doge-complaints-gateway/docs/analysis/
```
