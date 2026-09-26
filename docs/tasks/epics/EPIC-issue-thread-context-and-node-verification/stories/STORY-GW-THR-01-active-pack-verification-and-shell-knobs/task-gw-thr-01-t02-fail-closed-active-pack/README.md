# task-gw-thr-01-t02-fail-closed-active-pack

## Task: implement — Fail-closed active pack (T02)

## Meta
- **Story:** [STORY-GW-THR-01](../STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000093
- **Skill declared:** python-pro
- **Depends on:** prior T* in pkg order; loadable NODE_SCHEMA_* pack
- **Scaffolded:** 2026-09-21T20:17:40Z
- **Completed:** 2026-09-21T20:29:51Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md`

## Purpose
Active NODE_SCHEMA_* resolve: missing mandatory shell capabilities → ConfigError / fail-closed. No silent product defaults that invent policy.

## Code Facts
1. Boot/resolve fail-fast patterns exist for NODE_SCHEMA pack (SSR-16).
2. Arch 02: fail-closed packaging.
3. No foreign default / tallinn invent for missing knobs.

## Gap
**Closed (P3 2026-09-21T20:29:51Z):** implemented.

## Acceptance / DoD
- [x] Missing mandatory capabilities → ConfigError-class fail-closed
- [x] No silent defaults inventing verification/shell policy
- [x] URL-unset / SSR-34 warehouse path remains valid when caps present
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/schema/resolver.py and/or load validation`
- `src/core/config/schema.py boot resolve path if applicable`

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
rg -n 'ConfigError|resolve_pack' doge-complaints-gateway/src/core/schema doge-complaints-gateway/src/core/config
```
