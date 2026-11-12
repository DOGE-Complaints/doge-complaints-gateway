# task-gw-req59-01-t02-aibridge-client-contract-parity

## Task: verify — aibridge client contract parity (T02)

## Meta
- **Story:** [STORY-GW-REQ59-01](../STORY-GW-REQ59-01-aibridge-stash-parity-verify.md)
- **Type:** verify
- **Status:** 🔵 Done
- **Package:** pkg-000117
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-11-05T12:01:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md`
- **AC trace:** AC-GW-59-01 · peer arch `01-keep-pipe`

## Purpose
Parity vs aibridge: path `/story-drafts`, Bearer from config, success body `draft_id`+`trace_id`, outcome map

## Code Facts
### Live (As-of-Done P3 / P6 SSOT) — 2026-11-05T12:20:04Z
1. Peer `gateway.py` `STASH_PATH="/story-drafts"` · `execute_stash` · `parse_success_body` — Present (peer).
2. Gateway envelope success with `draft_id` + `trace_id` — Present (T01 / create envelope).
3. Parity cited in evidence note — Present (`docs/analysis/evidence-gw-req59-01-…`).

## Gap
**Closed P3** (parity cited) · P6 SSOT align G4.

## Acceptance / DoD
- [x] Parity cited: path, Bearer config, success body keys, outcome map
- [x] No invent AC; no aibridge code change this task
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req59-01-t02.md` signed (P3)

## Where to change
- Evidence only (task notes / analysis); peer `gateway.py` read-only

## Out of scope
Change aibridge; invent new stash fields; SPA continuation UX

## Verification commands
```bash
rg -n "STASH_PATH|execute_stash|draft_id|GATEWAY_SERVICE_API_TOKEN" doge-ai-bridge/src/aibridge/gateway.py | head -40
```
