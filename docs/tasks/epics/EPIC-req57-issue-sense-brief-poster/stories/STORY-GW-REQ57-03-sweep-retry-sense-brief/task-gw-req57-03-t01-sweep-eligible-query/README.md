# task-gw-req57-03-t01-sweep-eligible-query

## Task: implement — sweep eligible query (T01)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:03:07Z
- **Package:** pkg-000115
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-10-15T11:57:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md`
- **AC trace:** arch 02 §2.4

## Purpose
Select Issues `pending`/`failed` without successful brief apply

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:03:07Z
1. `is_sweep_eligible` / `list_sweep_eligible_issues` Present — pending|failed only; ready excluded.
2. Path: `src/core/application/sense_brief_sweep.py`.

## Gap
**Closed P3 2026-10-15T12:03:07Z.**

## Acceptance / DoD
- [x] Query/list Issues with `generation_status` in `pending`|`failed` lacking successful brief apply
- [x] No invent AC; no product beyond eligible selection
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-03-t01.md` signed (P3)

## Where to change
- `src/core/application/sense_brief_sweep.py`

## Out of scope
Cron job (T02); ASGI wire (T03); ready guard (T04); tests (T05); gate (T06); regenerate (04)

## Verification commands
```bash
rg -n "list_sweep_eligible|is_sweep_eligible" doge-complaints-gateway/src/core/application/sense_brief_sweep.py
```
