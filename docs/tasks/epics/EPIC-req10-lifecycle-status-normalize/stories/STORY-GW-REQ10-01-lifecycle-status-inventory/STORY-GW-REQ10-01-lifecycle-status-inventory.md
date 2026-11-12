# STORY-GW-REQ10-01 — Inventory distinct lifecycle_status values

## Meta
- **Key:** `STORY-GW-REQ10-01-lifecycle-status-inventory`
- **Parent Epic:** [`../../../EPIC-req10-lifecycle-status-normalize.md`](../../../EPIC-req10-lifecycle-status-normalize.md)
- **Пакет:** [`req10-lifecycle-status-normalize/`](../../../../backlog-stories/req10-lifecycle-status-normalize/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Тип:** data inventory / evidence for cleanup
- **source:** [`../../../../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md`](../../../../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md)
- **Parent REQ:** [`54-req10-lifecycle-status-normalize.md`](../../../../requirements/54-req10-lifecycle-status-normalize.md)
- **Parent product:** REQ10 §3.4, §6.3 **GW-10-01**, §7.1 H4 prep
- **Justification:** [`audit-threads-board-persist-clean-vs-hack-2026-09-27.md`](../../../../../../docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md) §3, §8
- **decision_ref:** backlog REQ10-01 · REQ54 · audit §3/§8 · REQ10 §3.4/§6.3 GW-10-01
- **Siblings:** threads `03-…` / spa `19-…` — no lifecycle contract
- **Skill declared:** python-pro · soft code-documenter
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml`](../../../../gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml)
- **Git:** `dev`
- **Operator lock:** inventory only — no production backfill here; data is test → cleanup target is canon enums
- **Зависит от:** —
- **Blocks:** STORY-GW-REQ10-02
- **Scaffolded:** 2026-09-28T17:11:07Z
- **P3 Done:** 2026-09-28T17:16:40Z · [`run-summary`](../../../../run-reports/run-summary-20260928-1716-gw-req10-01-p3.md) · [`gate`](./task-gw-req10-01-t04-story-gate/story-acceptance-gate-STORY-GW-REQ10-01.md) · [`inventory`](../../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md)

## Nested tasks (pkg-000098)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req10-01-t01-db-distinct-inventory`](./task-gw-req10-01-t01-db-distinct-inventory/README.md) | Done |
| T02 | [`task-gw-req10-01-t02-fixture-sqlite-scan`](./task-gw-req10-01-t02-fixture-sqlite-scan/README.md) | Done |
| T03 | [`task-gw-req10-01-t03-closed-list-normalize-note`](./task-gw-req10-01-t03-closed-list-normalize-note/README.md) | Done |
| T04 | [`task-gw-req10-01-t04-story-gate`](./task-gw-req10-01-t04-story-gate/README.md) | Done |

## Scope

1. Inventory distinct `lifecycle_status` values in hosted/test Supabase (operator-accessible project) — evidence note under gateway docs/analysis (path chosen at P3; do not invent schema).
2. Scan sqlite fixtures / seed SQL used by gateway tests for legacy `RECEIVED`/`received` (and any other non-enum strings).
3. Produce a closed list: enum-legal vs to-normalize-to-`accepted` vs unexpected (fail-closed candidates).
4. Do **not** run data cleanup / mapper slim in this story (→ REQ10-02).

## Out of scope

- Data cleanup / mapper slim / debug removal (→ REQ10-02).
- Threads/spa; new APIs; REQ8.
- H8 / `list_all` scale note.

## Verified current state

| Fact | Path |
|------|------|
| Enum values | `StoryLifecycleStatus` `src/core/domain/contracts.py:20-24` (`accepted`, `partial_ready`, `ready_for_profile`, `clustered`) |
| Supabase read maps `RECEIVED`/`received` → ACCEPTED | `src/core/infrastructure/db_supabase.py:179-224` `_parse_lifecycle_status` |
| Hydrate calls parser | `src/core/infrastructure/db_supabase.py:265` `_story_record_from_supabase_row` |
| sqlite hydrate uses `StoryLifecycleStatus(str(...))` only (no legacy map) | `src/core/infrastructure/db_sqlite.py:225` |
| Distinct live/test DB set | **Known** — inventory §T01: 162 rows; DISTINCT `clustered`/`ready_for_profile`/`RECEIVED`/`accepted` ([inventory](../../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md)) |

## Target / AC

- [x] **AC-GW-REQ1001-01:** Written inventory of distinct hosted/test `lifecycle_status` values (or documented operator blocker if DB unreachable).
- [x] **AC-GW-REQ1001-02:** Fixture/sqlite scan result: legacy `RECEIVED`/`received` present or absent.
- [x] **AC-GW-REQ1001-03:** Explicit list of values planned for normalize-to-`accepted` vs fail-closed unknowns (feeds REQ10-02 cleanup).

## Code touchpoints

- Read-only against DB/fixtures; no production mapper change in this story.
- Reference enum: `src/core/domain/contracts.py:20-24`

## Dependencies

- Ops access to test/hosted Supabase for DISTINCT query — **reachable** P3 2026-09-28T17:16:40Z (inventory §T01).
