# task-gw-thr-01-t03-migrate-activatable-packs

## Task: implement — Migrate activatable packs (T03)

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
Migrate every pack that can be selected as active (local warehouse and Volume) to the new format. Uus Veerenni example: type=phone + named phone integration. No knobs-optional legacy mode on first launch.

## Code Facts
1. Warehouse / Volume ops — SSR-34 manuals; SCHEMA_PACKS_ROOT.
2. Tracked demo packs under schema-packs/; node packs may be Volume/local only.
3. Exact JSON key names Open — migrate capabilities once names locked.

## Gap
**Closed (P3 2026-09-21T20:29:51Z):** implemented.

## Acceptance / DoD
- [x] Activatable packs carry mandatory capabilities in new format
- [x] Uus Veerenni example: phone + named phone integration
- [x] No backward-compat 'old pack without knobs is OK'
- [x] BULLRUN phases complete when closed

## Where to change
- `schema-packs/<id>/<ver>/ (activatable trees)`
- `Volume/local packs under SCHEMA_PACKS_ROOT when present`

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
ls doge-complaints-gateway/schema-packs/
```
