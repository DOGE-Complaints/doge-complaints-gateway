# STORY-GW-THR-01 — Active pack: verification policy + shell knobs materialize

## Meta
- **Key:** `STORY-GW-THR-01-active-pack-verification-and-shell-knobs`
- **Пакет:** [`issue-thread-context-and-node-verification/`](./INDEX.md)
- **Status:** Done
- **Тип:** pack content / schema-pack load validation / fail-closed
- **Parent REQ:** [`52-issue-thread-context-and-node-verification.md`](../../../requirements/52-issue-thread-context-and-node-verification.md)
- **Parent product:** REQ7 · T-REQ7-04 / T-REQ7-08 · D4 · D28 · AC-REQ7-15
- **Architecture:** [`02-pack-verification-and-shell-knobs.md`](../../../architecture/threads-issue-context-and-pack/02-pack-verification-and-shell-knobs.md)
- **Skill declared (future P3):** `python-pro` · soft `code-documenter`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** loadable nested active pack for `NODE_SCHEMA_*` (ops / SSR-34 class precondition)
- **Blocks:** STORY-GW-THR-02
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)

---

## Scope

1. Materialize into the **active** pack the mandatory shell capabilities: validation type (`phone` \| `eID`) + integration name; max depth; per-reaction enables; `max_reactions_per_actor`; Topic-guarded presentation defaults; media-type allowlist within parent §9 floors.
2. Uus Veerenni target example: type = phone + named phone integration (REQ §2).
3. Fail-closed when the active pack omits mandatory shell capabilities — no silent product defaults that invent policy.
4. **Pack content migration** to the new format for every pack that can be selected as active (local warehouse and Volume) — **no** “knobs optional legacy” mode on first launch.
5. Exact JSON **key names remain Open** — do not invent key strings in DoD; capabilities must be present and validatable once names are locked in implement wave / operator decision.

## Out of scope

- Service-auth HTTP settings pull (→ STORY-GW-THR-02).
- Civic gate `phone_verified` → `identity_verified` (→ STORY-GW-THR-03).
- REQ8 sanction enforce / voice-source API.
- Pack Builder authoring UX; Landing as verification-policy home.
- Inventing a public ThreadContext route or concrete pack JSON key strings in the Draft sense (AC-GW-THR-01).

## Verified current state

| Fact | Evidence |
|------|----------|
| Active pair = env | `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` (SSR-16; `AppConfig`) — unchanged |
| Pack root | `SCHEMA_PACKS_ROOT` or in-tree `schema-packs/` — unchanged |
| Shell capabilities on activatable packs | **As-of-Done (P3):** sidecar `shell_capabilities.json` next to `pack.json` for tallinn/legal/mobility + uus v2/v3; fail-closed via [`shell_capabilities.py`](../../../src/core/schema/shell_capabilities.py) + [`resolver.py`](../../../src/core/schema/resolver.py) `load_shell_capabilities`. Uus: `phone` / `uus_phone_sms`. Caps live in sidecar — **not** invent pack.json key table (AC-04). **Historical (pre-P3 / arch):** verification / threads blocks **Not found** (grep empty under `schema-packs/`). |
| Warehouse / Volume ops | SSR-34 manuals; REQ52 §3 — unchanged |

## Target / AC

- [x] **AC-GW-THR01-01:** Active pack for `NODE_SCHEMA_*` carries verification policy capabilities (validation type + integration name) — parent AC-GW-THR-03.
- [x] **AC-GW-THR01-02:** Same pack carries shell knobs capabilities listed in parent AC-GW-THR-05.
- [x] **AC-GW-THR01-03:** Missing mandatory capabilities → fail-closed on resolve and/or settings path (arch `02`); no invented silent defaults.
- [x] **AC-GW-THR01-04:** Story/Draft does not mandate concrete pack JSON key strings (parent AC-GW-THR-01).
- [x] **AC-GW-THR01-05:** Activatable packs migrated to the new format; no backward-compat “old pack without knobs is OK”.

## Техническое решение (projected)

- **Approach:** extend active-pack resolve/load so mandatory shell **capabilities** (verification policy + knobs from REQ AC-GW-THR-05 / arch `02`) are present and validated; fail-closed if absent. Materialize/migrate activatable pack JSON on warehouse/Volume. Exact JSON key **strings** stay Open until implement-wave operator lock — do not invent in this story text.
- **Arch:** [`02-pack-verification-and-shell-knobs.md`](../../../architecture/threads-issue-context-and-pack/02-pack-verification-and-shell-knobs.md) · overview packaging/fail-closed
- **Skill:** `python-pro` · soft `code-documenter`

## Nested tasks (planned — folders at P1.3 only; name ≠ create)

> Pipeline folders `task-gw-thr-01-tNN-*` materialize only under P1.3 pkg — **do not** create them from this backlog edit.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-gw-thr-01-t01-shell-capability-contract` | Done | Capability checklist for verification policy + shell knobs (type, integration name, depth, reaction enables/max, Topic defaults, media allowlist); wire into pack load/config types **without** inventing REQ-forbidden key strings until operator lock |
| **T02** | `task-gw-thr-01-t02-fail-closed-active-pack` | Done | Active `NODE_SCHEMA_*` resolve: missing mandatory capabilities → ConfigError / fail-closed (no silent defaults) |
| **T03** | `task-gw-thr-01-t03-migrate-activatable-packs` | Done | Migrate activatable packs (incl. uus Veerenni phone + named integration example) to new format; no “knobs optional” legacy mode |
| **T04** | `task-gw-thr-01-t04-tests-pack-shell-required` | Done | Pytest: complete pack resolves; incomplete pack fails closed |
| **T05** | `task-gw-thr-01-t05-story-gate` | Done | Story AC-GW-THR01-01…05 gate |
| **T06** | `task-gw-thr-01-t06-audit-g1-as-of-done-ssot` | Done | Audit G1 As-of-Done SSOT (`run_mode=gw_thr_01_audit_followup`) |

## Code touchpoints (As-of-Done)

- **As-of-Done:** [`src/core/schema/shell_capabilities.py`](../../../src/core/schema/shell_capabilities.py) — sidecar contract + REQ capability ids; [`contracts.py`](../../../src/core/schema/contracts.py) `ShellCapabilitiesBlock` / `SchemaContext.shell_capabilities`; [`resolver.py`](../../../src/core/schema/resolver.py) `load_pack` → `load_shell_capabilities` (fail-closed). Warehouse: `schema-packs/<id>/<ver>/shell_capabilities.json`.
- Active pair boot / lifespan — SSR-16 patterns (asgi / config); missing caps → `UnsupportedVersionError` → `ConfigError` when soft-boot off.
- **Historical:** «exact validation hooks Unknown until implement-wave Read» — pre-P3 only.

## Dependencies

- Ops precondition: nested pack present for the active node.
- How pack validation type + integration name reach **identity** remains Open (not invented here).
- **Blocks:** STORY-GW-THR-02.
