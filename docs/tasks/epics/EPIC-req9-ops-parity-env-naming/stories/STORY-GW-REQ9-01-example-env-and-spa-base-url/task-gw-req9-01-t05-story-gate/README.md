# task-gw-req9-01-t05-story-gate

## Task: gate — Story acceptance gate (T05)

## Meta
- **Story:** [STORY-GW-REQ9-01](../STORY-GW-REQ9-01-example-env-and-spa-base-url.md)
- **Type:** gate
- **Status:** 🔵 Done
- **Package:** pkg-000096
- **Skill declared:** python-pro
- **Depends on:** T01–T04 Done
- **Scaffolded:** 2026-09-26T12:02:43Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req9-ops-parity-env-naming/STORY-GW-REQ9-01-example-env-and-spa-base-url.md`

## Purpose
Story acceptance gate for AC-GW-REQ901-01…05. PASS iff all AC. Template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`. Hard cut only; no dual-read; no invent Railway service ids; no §Актуальная точка rewrite.

## Code Facts
1. Gate template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`.
2. Gate artifact Date only after P3 live pytest + `--verify` in that session.
3. pkg-000096 immutable for P3 product wave.

## Gap
Story gate artifact not yet produced (P3).

## Acceptance / DoD
- [x] story-acceptance-gate PASS/FAIL + evidence (P3)
- [x] acceptance-verification signed (Date post P3 live verify)
- [x] AC-GW-REQ901-01…05 covered
- [x] Live `--project gateway --verify` recorded
- [x] Do not rewrite §Актуальная точка
- [x] BULLRUN phases complete

## Where to change
- This folder gate artifacts (P3)

## Out of scope
REQ9-02; invent Railway ids; dual-read; §Актуальная точка rewrite.
- Overlay bans:
  - Hard cut only — **no** `SPA_VERIFY_*` dual-read.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000095; pointer is pkg-000096.

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
```
