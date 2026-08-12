# task-gw-draft-07-t06-story-acceptance-gate

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** tests / process
- **Status:** 🟢 Done
- **Package:** pkg-000056
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Story acceptance gate: sign all five parent AC (ready + submit 202 + retry + evidence + SPA-BUG-01 unblocked for regression) per [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md).

## Code Facts
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Parent AC — 5 bullets verbatim in pipeline story
- Intake / ready seams — [`handlers.py:159-182`](../../../../../../../../src/core/api/handlers.py), [`dependencies.py:75-83`](../../../../../../../../src/core/api/dependencies.py), [`asgi_app.py:228-238`](../../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- [x] All 5 parent AC signed in [`story-acceptance-gate-STORY-GW-DRAFT-07.md`](./story-acceptance-gate-STORY-GW-DRAFT-07.md)
- [x] Traces AC #5: FE-HANDOFF-03 / SPA-BUG-01 can close regression on a new draft after this Done
- [x] `--verify --check-dates` ok for pkg-000056
- [x] BULLRUN phases complete
- [x] Gate Date only after live verify in P3

## Where to change
- [`story-acceptance-gate-STORY-GW-DRAFT-07.md`](./story-acceptance-gate-STORY-GW-DRAFT-07.md)
- [`acceptance-verification-gw-draft-07-t06.md`](./acceptance-verification-gw-draft-07-t06.md)
- bullrun / backlog status sync after PASS

## Out of scope
- SPA UI hotfix; GPT OpenAPI; identity; rewriting UUID migrations; dropping `story_labels` from `REQUIRED_READINESS_TABLES`

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
curl -sS https://dogestonia-tallinn.up.railway.app/ready | python3 -m json.tool
# Plus T05 submit/retry evidence path
```
