# task-gw-req59-01-t04-stash-neq-story-assert

## Task: verify — stash ≠ published Story (T04)

## Meta
- **Story:** [STORY-GW-REQ59-01](../STORY-GW-REQ59-01-aibridge-stash-parity-verify.md)
- **Type:** verify
- **Status:** 🔵 Done
- **Package:** pkg-000117
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-11-05T12:01:41Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req59-req15-story-draft-stash-channel-parity-verify/STORY-GW-REQ59-01-aibridge-stash-parity-verify.md`
- **AC trace:** AC-GW-59-02

## Purpose
Evidence: after 201 stash, no Story/issue until submit; cite create vs `handle_story_draft_submit`

## Code Facts
### Live (As-of-Done P3 / P6 SSOT) — 2026-11-05T12:20:04Z
1. Create returns only `draft_id` — Present (`handle_story_draft_create`).
2. Story/issue via submit→intake (`handle_story_draft_submit`) — Present.
3. Assert Present — `test_post_story_drafts_returns_draft_id_without_creating_story` · evidence note AC-02.

## Gap
**Closed P3** (stash ≠ Story) · P6 SSOT align G4.

## Acceptance / DoD
- [x] Cited: after 201 stash, no Story/issue until submit
- [x] Cite create vs `handle_story_draft_submit` paths
- [x] No invent AC; no SPA UI
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req59-01-t04.md` signed (P3)

## Where to change
- Evidence notes; product only if hard break → T05

## Out of scope
SPA UI; invent Story publish on stash

## Verification commands
```bash
rg -n "handle_story_draft_create|handle_story_draft_submit|draft_id" doge-complaints-gateway/src/core/api/handlers.py | head -40
```
