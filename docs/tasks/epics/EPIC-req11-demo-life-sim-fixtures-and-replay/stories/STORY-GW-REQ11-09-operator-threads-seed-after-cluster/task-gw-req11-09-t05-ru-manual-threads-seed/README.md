# task-gw-req11-09-t05-ru-manual-threads-seed

## Task: docs — RU manual threads seed (T05)

## Meta
- **Story:** [STORY-GW-REQ11-09](../STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-10-01T10:52:44Z
- **Package:** pkg-000107
- **Skill declared:** python-pro
- **Depends on:** T01–T03
- **Scaffolded:** 2026-10-01T10:45:33Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`

## Purpose
RU manual Present + load-manual § threads cross-link; close **B-THR-CLI**. Scope #1,#9 · AC-05.

## Code Facts
**As-of-Done (P3 2026-10-01T10:52:44Z):**
1. Present: `docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md`.
2. Load manual §6.2 / §7 / §8 updated — B-THR-CLI **Closed**; Make one-liner link.

### Historical (scaffold / pre-P3)
RU threads-seed manual Absent; B-THR-CLI open.

## Gap
**As-of-Done:** closed.

## Acceptance / DoD
- [x] RU manual Present (AC-05)
- [x] Operator can smoke/full from terminal without chat agent
- [x] Load manual links § threads; **B-THR-CLI** closed
- [x] Terms lock documented
- [x] BULLRUN phases complete when closed

## Where to change
- `docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md`
- `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md`

## Out of scope
SPA verify.

## Verification commands
```bash
ls doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md
rg -n 'B-THR-CLI|life-sim-seed-threads' doge-complaints-gateway/docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md
```
