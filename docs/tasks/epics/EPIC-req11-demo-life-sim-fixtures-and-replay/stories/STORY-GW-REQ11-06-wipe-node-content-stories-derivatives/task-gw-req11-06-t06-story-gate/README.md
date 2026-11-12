# task-gw-req11-06-t06-story-gate

## Task: gate — story acceptance gate (T06)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** gate
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** T01–T05 Done
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
Story acceptance gate for AC-GW-REQ1106-01…04. Template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`. No §Актуальная точка rewrite. No product wipe in APPLY.

## Code Facts
1. Gate artifacts Absent until P3.
2. `--verify` + `--check-dates` required before Done.

## Gap
**As-of-Done (P3):** closed.

Gate + acceptance-verification not written.

## Acceptance / DoD
- [x] story-acceptance-gate PASS/FAIL + evidence (P3)
- [x] acceptance-verification signed (Date post P3 live verify)
- [x] AC-GW-REQ1106-01…04 covered
- [x] Live `--project gateway --verify` recorded
- [x] Do not rewrite §Актуальная точка
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
Product implement beyond verify; invent wipe HTTP; Identity DELETE; rewrite §Актуальная точка.
- Overlay bans:
  - Stay `dev`.
  - Confirm: `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`.
  - Tables: `REQUIRED_READINESS_TABLES` + three threads only.
  - No Identity DELETE; no invent wipe HTTP.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify --check-dates
```
