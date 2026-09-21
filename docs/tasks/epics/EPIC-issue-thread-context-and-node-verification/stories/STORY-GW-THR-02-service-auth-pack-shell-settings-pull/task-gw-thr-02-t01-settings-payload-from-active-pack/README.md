# task-gw-thr-02-t01-settings-payload-from-active-pack

## Task: implement — Settings payload from active pack (T01)

## Meta
- **Story:** [STORY-GW-THR-02](../STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000094
- **Skill declared:** python-pro
- **Depends on:** STORY-GW-THR-01 Done (pkg-000093); prior T* in pkg order
- **Scaffolded:** 2026-09-21T20:43:05Z
- **Completed:** 2026-09-21T20:48:13Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-02-service-auth-pack-shell-settings-pull.md`

## Purpose
Map active-pack `shell_capabilities` → settings DTO (verification policy + shell knobs). Source = active `NODE_SCHEMA_*` pair only — no client-chosen pack id. Capability presence only; JSON field names remain Open (choose at P3, do not write into REQ).

## Code Facts
1. `SchemaContext.shell_capabilities: ShellCapabilitiesBlock` — `src/core/schema/contracts.py` (~158–181).
2. Loaded fail-closed via `load_shell_capabilities` — `src/core/schema/shell_capabilities.py` + `resolver.py`.
3. Active pair = `NODE_SCHEMA_*` (AppConfig / SSR class).
4. **As-of-Done (P3):** [`shell_settings.py`](../../../../../../src/core/schema/shell_settings.py) `build_active_pack_shell_settings` / `shell_capabilities_to_settings_dict` → `pack_shell_settings`; [`handlers.py`](../../../../../../src/core/api/handlers.py) `handle_pack_shell_settings`.
5. **Historical (pre-P3):** «No settings DTO / pull mapper found under `src/`» — gap closed at P3.

## Gap
**Closed (P3 2026-09-21T20:48:13Z):** `shell_settings.py` maps active-pack `ShellCapabilitiesBlock` → `pack_shell_settings` DTO; fail-closed via `resolve_pack`. **G1 SSOT As-of-Done (P6 2026-09-21T20:54:56Z).**


## Acceptance / DoD
- [x] Settings DTO maps verification policy + shell knobs from active-pack `shell_capabilities` (AC-GW-THR02-01)
- [x] No client-chosen pack id in request body / mapper inputs (Scope #2)
- [x] Incomplete caps remain fail-closed (no silent empty policy) (AC-GW-THR02-04)
- [x] No invented REQ-forbidden JSON key strings in DoD (Open)
- [x] BULLRUN phases complete when closed

## Where to change
- `src/core/` — settings DTO / mapper from `SchemaContext.shell_capabilities` (exact module chosen at P3)
- Do **not** change public Issue get projection in this task

## Out of scope
THR-03; REQ8; public ThreadContext route; invent path/JSON into REQ; Story bodies; §Актуальная точка rewrite.
- Overlay bans (every task):
  - **Do not invent** public ThreadContext route.
  - Path/JSON field names **Open** — choose at P3; do not write into REQ.
  - No Story narrative bodies in settings (D19).
  - Fail-closed — no silent empty policy.
  - Stay `semantic-schema-runtime`.
  - Do not mutate pkg-000093; pointer is pkg-000094.

## Verification commands
```bash
rg -n 'ShellCapabilitiesBlock|shell_capabilities' doge-complaints-gateway/src/core/schema
```
