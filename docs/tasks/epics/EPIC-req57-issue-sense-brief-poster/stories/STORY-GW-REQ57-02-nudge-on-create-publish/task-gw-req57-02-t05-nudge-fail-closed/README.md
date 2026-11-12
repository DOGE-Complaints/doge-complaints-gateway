# task-gw-req57-02-t05-nudge-fail-closed

## Task: implement — nudge fail-closed (T05)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** T04
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** AC-5702-04

## Purpose
Disabled/missing env → no silent success; pending may remain

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. Fail-closed Present — disabled / missing_config / http_status / transport (no pretend ready).
2. Path: `sense_brief_nudge.py` `nudge()`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] Missing/disabled AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED → fail-closed (no pretend success)
- [x] Missing required URL/token when enabled → fail-closed
- [x] pending may remain observable
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t05.md` signed (P3)

## Where to change
- Nudge gate / client fail-closed branches
- Logging observability

## Out of scope
Happy-path enable (T04); invent AC

## Verification commands
```bash
rg -n "NUDGE_ENABLED|fail.closed|fail_closed" doge-complaints-gateway/src --glob '*.py' | head -40
```
