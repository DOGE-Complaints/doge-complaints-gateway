# task-gw-thr-01-t01-shell-capability-contract

## Task: implement — Shell capability contract (T01)

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
Capability checklist for verification policy + shell knobs (validation type phone|eID, integration name, max depth, per-reaction enables, max_reactions_per_actor, Topic-guarded presentation defaults, media-type allowlist within parent §9 floors). Wire into pack load/config types without inventing REQ-forbidden JSON key strings until operator lock.

## Code Facts
1. Active pair = NODE_SCHEMA_* (SSR-16 / AppConfig).
2. **As-of-Done (P3):** [`shell_capabilities.py`](../../../../../../src/core/schema/shell_capabilities.py) sidecar contract; [`contracts.py`](../../../../../../src/core/schema/contracts.py) `ShellCapabilitiesBlock`; [`resolver.py`](../../../../../../src/core/schema/resolver.py) `load_pack` → `load_shell_capabilities` (fail-closed). Caps = REQ7 capability ids in sidecar — not pack.json product key table.
3. **As-of-Done:** warehouse `schema-packs/*/v*/shell_capabilities.json` (5/5); uus `phone`/`uus_phone_sms`. **Historical (pre-P3):** verification / threads shell blocks Not found (grep empty).

## Gap
**Closed (P3 2026-09-21T20:29:51Z):** implemented. **G1 SSOT As-of-Done (P6 2026-09-21T20:35:45Z).**

## Acceptance / DoD
- [x] Capability contract types/checklist present for verification + shell knobs
- [x] No invented concrete pack JSON key strings in DoD
- [x] Wire hooks identified for pack load/config
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/schema/ (contracts / resolver / load validation)`
- `activatable packs layout under schema-packs/ (structure only until key lock)`

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
rg -n 'NODE_SCHEMA|resolve_pack' doge-complaints-gateway/src/core/schema doge-complaints-gateway/src/core/config
```
