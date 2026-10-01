# task-gw-req11-10-t05-ru-manual-replay-pack-wave

## Task: docs — RU manual pack-wave replay (T05)

## Meta
- **Story:** [STORY-GW-REQ11-10](../STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T11:35:43Z
- **Package:** pkg-000108
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Decision Ref:** backlog STORY-GW-REQ11-10

## Purpose
RU manual Present; load-manual § replay pack-wave primary. AC-05.

## Code Facts
**As-of-Done (P3 2026-10-01T11:35:43Z):**
1. `docs/runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md` Present.
2. Load manual §6.2 / inventory links pack-wave as primary; legacy simulate noted.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] RU manual Present (AC-05)
- [x] Load manual pack-wave primary
- [x] Order wipe→provision→replay→cluster→threads documented
- [x] BULLRUN phases complete when closed

## Where to change
- RU manual + load manual

## Out of scope
Product code reopen.

## Verification commands
```bash
test -f doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md
```
