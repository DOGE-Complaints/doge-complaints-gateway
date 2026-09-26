# STORY-GW-THR-01 — Active pack: verification policy + shell knobs materialize

## Meta
- **Key:** `STORY-GW-THR-01-active-pack-verification-and-shell-knobs`
- **Parent Epic:** [`../../../EPIC-issue-thread-context-and-node-verification.md`](../../../EPIC-issue-thread-context-and-node-verification.md)
- **Пакет:** [`issue-thread-context-and-node-verification/`](../../../../backlog-stories/issue-thread-context-and-node-verification/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** pack content / schema-pack load validation / fail-closed
- **source:** [`../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md`](../../../../backlog-stories/issue-thread-context-and-node-verification/STORY-GW-THR-01-active-pack-verification-and-shell-knobs.md)
- **Parent REQ:** 52 · REQ7 · T-REQ7-04 / T-REQ7-08 · D4 · D28 · AC-REQ7-15
- **Architecture:** [`../../../../architecture/threads-issue-context-and-pack/02-pack-verification-and-shell-knobs.md`](../../../../architecture/threads-issue-context-and-pack/02-pack-verification-and-shell-knobs.md)
- **decision_ref:** backlog THR-01
- **Skill declared:** python-pro · soft code-documenter
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000093-20260921-gw-thr-01-active-pack-verification-and-shell-knobs.yaml`](../../../../gateway-active-packages/pkg-000093-20260921-gw-thr-01-active-pack-verification-and-shell-knobs.yaml)
- **Git:** `semantic-schema-runtime`
- **Зависит от:** loadable nested active pack for `NODE_SCHEMA_*` (ops / SSR-34 class)
- **Blocks:** STORY-GW-THR-02
- **Scaffolded:** 2026-09-21T20:17:40Z
- **Completed:** 2026-09-21T20:29:51Z

## Nested tasks (pkg-000093)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-thr-01-t01-shell-capability-contract`](./task-gw-thr-01-t01-shell-capability-contract/README.md) | Done |
| T02 | [`task-gw-thr-01-t02-fail-closed-active-pack`](./task-gw-thr-01-t02-fail-closed-active-pack/README.md) | Done |
| T03 | [`task-gw-thr-01-t03-migrate-activatable-packs`](./task-gw-thr-01-t03-migrate-activatable-packs/README.md) | Done |
| T04 | [`task-gw-thr-01-t04-tests-pack-shell-required`](./task-gw-thr-01-t04-tests-pack-shell-required/README.md) | Done |
| T05 | [`task-gw-thr-01-t05-story-gate`](./task-gw-thr-01-t05-story-gate/README.md) | Done |
| T06 | [`task-gw-thr-01-t06-audit-g1-as-of-done-ssot`](./task-gw-thr-01-t06-audit-g1-as-of-done-ssot/README.md) | Done (G1 CLOSED P6 2026-09-21T20:35:45Z) |

## Scope / Out of scope

**In (verbatim backlog Scope):**
1. Materialize into the **active** pack the mandatory shell capabilities: validation type (`phone` \| `eID`) + integration name; max depth; per-reaction enables; `max_reactions_per_actor`; Topic-guarded presentation defaults; media-type allowlist within parent §9 floors.
2. Uus Veerenni target example: type = phone + named phone integration (REQ §2).
3. Fail-closed when the active pack omits mandatory shell capabilities — no silent product defaults that invent policy.
4. **Pack content migration** to the new format for every pack that can be selected as active (local warehouse and Volume) — **no** “knobs optional legacy” mode on first launch.
5. Exact JSON **key names remain Open** — do not invent key strings in DoD; capabilities must be present and validatable once names are locked in implement wave / operator decision.

**Out:** Service-auth HTTP settings pull (THR-02); civic gate `identity_verified` (THR-03); REQ8; Pack Builder UX; invent public ThreadContext route or concrete pack JSON key strings; rewrite §«Актуальная точка» / MVP dashboard.

## Target / AC

- [x] **AC-GW-THR01-01:** Active pack for `NODE_SCHEMA_*` carries verification policy capabilities (validation type + integration name) — parent AC-GW-THR-03.
- [x] **AC-GW-THR01-02:** Same pack carries shell knobs capabilities listed in parent AC-GW-THR-05.
- [x] **AC-GW-THR01-03:** Missing mandatory capabilities → fail-closed on resolve and/or settings path (arch `02`); no invented silent defaults.
- [x] **AC-GW-THR01-04:** Story/Draft does not mandate concrete pack JSON key strings (parent AC-GW-THR-01).
- [x] **AC-GW-THR01-05:** Activatable packs migrated to the new format; no backward-compat “old pack without knobs is OK”.
