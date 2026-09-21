# task-gw-thr-01-t05-story-gate

## Task: gate — Story acceptance gate (T05)

## Meta
- **Story:** [STORY-GW-THR-01](../STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md)
- **Type:** gate
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000093
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-09-21T20:17:40Z
- **Completed:** 2026-09-21T20:29:51Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md`

## Purpose
Story acceptance gate for AC-GW-THR01-01…05. PASS iff all AC. No invent key strings / ThreadContext route; no §Актуальная точка rewrite.

## Code Facts
1. Gate artifact scaffolded; Date after P3 live verify (scaffold uses APPLY utc for check-dates).
2. pkg-000093 immutable for P3.

## Gap
**Closed (P3 2026-09-21T20:29:51Z):** implemented.

## Acceptance / DoD
- [x] story-acceptance-gate PASS/FAIL + evidence (P3)
- [x] acceptance-verification signed (Date post P3 live verify)
- [x] AC-GW-THR01-01…05 covered
- [x] Live --project gateway --verify recorded
- [x] Do not rewrite §Актуальная точка
- [x] BULLRUN phases complete

## Where to change
- `This folder gate artifacts (P3)`

## Out of scope
THR-02/03; REQ8; invent ThreadContext route; invent pack JSON key strings; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** pack JSON key strings (Open until operator lock).
  - **Do not invent** public ThreadContext route.
  - Fail-closed only — no silent defaults inventing policy.
  - Mandatory migration — no backward-compat “old pack without knobs OK”.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000061…092; pointer is pkg-000093.

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
