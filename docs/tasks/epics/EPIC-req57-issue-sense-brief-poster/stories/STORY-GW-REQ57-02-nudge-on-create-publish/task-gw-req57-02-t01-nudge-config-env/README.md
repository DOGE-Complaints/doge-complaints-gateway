# task-gw-req57-02-t01-nudge-config-env

## Task: implement — nudge config env (T01)

## Meta
- **Story:** [STORY-GW-REQ57-02](../STORY-GW-REQ57-02-nudge-on-create-publish.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T11:41:13Z
- **Package:** pkg-000114
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-15T11:34:35Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-02-nudge-on-create-publish.md`
- **AC trace:** ENV-CHECKLIST; arch 00 §5

## Purpose
Config: AIBRIDGE_BASE_URL, AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN, AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED

## Code Facts
### Live (post-P3 close) — 2026-10-15T11:41:13Z
1. ENV_SCHEMA + AppConfig Present — `AIBRIDGE_BASE_URL`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`, `AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED`.
2. `example.env` documents locked names.
3. Paths: `src/core/config/schema.py`, `example.env`.

### Historical (scaffold / pre-P3) — 2026-10-15T11:34:35Z
1. Scaffold only.

## Gap
**Closed P3 2026-10-15T11:41:13Z.**

## Acceptance / DoD
- [x] Config schema / example.env expose locked nudge env names (no invent aliases)
- [x] Names match ENV-CHECKLIST exactly
- [x] No product nudge call yet (T02+)
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-02-t01.md` signed (P3)

## Where to change
- Config / schema / `example.env` (locked names only)
- [`ENV-CHECKLIST.md`](../../../../backlog-stories/req57-issue-sense-brief-poster/ENV-CHECKLIST.md)

## Out of scope
HTTP client (T02); hook (T04); tests (T06); bind/sweep/regenerate

## Verification commands
```bash
rg -n "AIBRIDGE_BASE_URL|AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN|AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED" doge-complaints-gateway/src doge-complaints-gateway/example.env | head -40
```
