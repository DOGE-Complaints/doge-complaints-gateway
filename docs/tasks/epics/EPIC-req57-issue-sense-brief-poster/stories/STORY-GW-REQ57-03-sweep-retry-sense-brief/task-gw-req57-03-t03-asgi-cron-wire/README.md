# task-gw-req57-03-t03-asgi-cron-wire

## Task: implement — ASGI cron wire (T03)

## Meta
- **Story:** [STORY-GW-REQ57-03](../STORY-GW-REQ57-03-sweep-retry-sense-brief.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Done:** 2026-10-15T12:03:07Z
- **Package:** pkg-000115
- **Skill declared:** python-pro
- **Depends on:** T02
- **Scaffolded:** 2026-10-15T11:57:04Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req57-issue-sense-brief-poster/STORY-GW-REQ57-03-sweep-retry-sense-brief.md`
- **AC trace:** `asgi_app.py` ~229–265 · nudge-enabled gate (`AIBRIDGE_SENSE_BRIEF_NUDGE_ENABLED`)

## Purpose
Start/stop `SenseBriefSweepCronJob` in `asgi_app.py` lifespan (~229–265) alongside cluster cron (~194–228); gated by nudge enable

## Code Facts
### Live (post-P3 close) — 2026-10-15T12:03:07Z
1. Lifespan starts/stops `SenseBriefSweepCronJob` when `aibridge_sense_brief_nudge_enabled`.
2. Interval reuses `cluster_cron_interval_s` (no invent env).
3. Path: `src/core/api/asgi_app.py`.

## Gap
**Closed P3 2026-10-15T12:03:07Z.**

## Acceptance / DoD
- [x] Sense-brief sweep cron started/stopped with app lifespan alongside cluster cron
- [x] No invent second ASGI entry; reuse existing lifecycle pattern
- [x] BULLRUN phases complete when closed
- [x] `acceptance-verification-gw-req57-03-t03.md` signed (P3)

## Where to change
- `src/core/api/asgi_app.py`

## Out of scope
Eligible query (T01); job body (T02); ready guard (T04); tests (T05); gate (T06)

## Verification commands
```bash
rg -n "SenseBriefSweepCronJob|sense_brief_sweep" doge-complaints-gateway/src/core/api/asgi_app.py
```
