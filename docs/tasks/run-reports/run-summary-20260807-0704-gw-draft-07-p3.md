# Run summary — GW-DRAFT-07 P3 Execute

- **Date:** 2026-08-07T07:04:17Z
- **builder_project:** gateway
- **gateway_input_package:** `pkg-000056-20260806-gw-draft-07-hosted-schema-blocks-browser-submit.yaml`
- **epic_key:** EPIC-M2-21
- **story_key:** STORY-GW-DRAFT-07
- **Result:** PASS (story gate)

## Tasks

| Task | Result |
|------|--------|
| T01 inventory | PASS — only `story_labels` missing on Public Node |
| T02 DDL | PASS — `draft_07_story_labels_text_fk` (text FK) |
| T03 redeploy | PASS — Railway `66629cac-0d9f-4516-9b10-057cf61b8eed` SUCCESS |
| T04 /ready | PASS — `db.ready=true`, `checks.schema=true` |
| T05 smoke+evidence | PASS — submit 202; idempotent retry same story_id; GET draft 404 |
| T06 gate | PASS — 2026-08-07T07:04:17Z |

## Evidence
- [`evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md`](../../analysis/evidence-STORY-GW-DRAFT-07-hosted-submit-2026-08-07T070417Z.md)
- Gate: `task-gw-draft-07-t06-story-acceptance-gate/story-acceptance-gate-STORY-GW-DRAFT-07.md`

## Notes
- No `src/` code changes (ops/verify story).
- AC3 as-built: retry submit returns **202** via `_story_intake_replay_from_idempotency` (same `story_id`); draft GET → 404.
- SPA-BUG-01 / FE-HANDOFF-03 unblocked for SPA retest.
- Offline pytest (`-m "not live_integration"`): **608 passed**, 4 failed (smoke header / pirita smoke / identity-config env) — pre-existing / env, not DRAFT-07 src.
