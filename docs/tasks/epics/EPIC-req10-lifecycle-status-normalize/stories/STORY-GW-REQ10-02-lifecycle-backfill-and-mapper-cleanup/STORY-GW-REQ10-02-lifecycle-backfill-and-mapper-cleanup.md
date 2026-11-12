# STORY-GW-REQ10-02 — Cleanup lifecycle data + slim mapper + remove debug I/O

## Meta
- **Key:** `STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup`
- **Parent Epic:** [`../../../EPIC-req10-lifecycle-status-normalize.md`](../../../EPIC-req10-lifecycle-status-normalize.md)
- **Пакет:** [`req10-lifecycle-status-normalize/`](../../../../backlog-stories/req10-lifecycle-status-normalize/INDEX.md)
- **Status:** ✅ Done
- **Тип:** data cleanup / adapter harden / debug removal
- **source:** [`../../../../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`](../../../../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Parent REQ:** [`54-req10-lifecycle-status-normalize.md`](../../../../requirements/54-req10-lifecycle-status-normalize.md) §2, §4, §5
- **Parent product:** REQ10 §6.3 **GW-10-02…04**; AC **H1** (gateway), **H4**
- **Justification:** [`audit-threads-board-persist-clean-vs-hack-2026-09-27.md`](../../../../../../docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md) §3, §8
- **decision_ref:** backlog REQ10-02 · REQ54 §2/§4/§5 · audit §3/§8 · REQ10 §6.3 GW-10-02…04 · inventory feed
- **Skill declared:** python-pro · soft sql-pro
- **Operative package:** [`../../../../gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml`](../../../../gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml)
- **Git:** `dev`
- **Operator lock:** test data → **normalize/clean to canon immediately**; no permanent RECEIVED special-case; no dual-path complexity; H8 skipped this wave
- **Зависит от:** STORY-GW-REQ10-01 (Done)
- **Scaffolded:** 2026-09-28T17:27:26Z

## Nested tasks (pkg-000099)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req10-02-t01-hosted-lifecycle-backfill`](./task-gw-req10-02-t01-hosted-lifecycle-backfill/README.md) | Done (hosted blocker) |
| T02 | [`task-gw-req10-02-t02-fixture-cleanup-confirm`](./task-gw-req10-02-t02-fixture-cleanup-confirm/README.md) | Done (N/A) |
| T03 | [`task-gw-req10-02-t03-slim-lifecycle-mapper`](./task-gw-req10-02-t03-slim-lifecycle-mapper/README.md) | Done |
| T04 | [`task-gw-req10-02-t04-remove-debug-io`](./task-gw-req10-02-t04-remove-debug-io/README.md) | Done |
| T05 | [`task-gw-req10-02-t05-lifecycle-parse-tests`](./task-gw-req10-02-t05-lifecycle-parse-tests/README.md) | Done |
| T06 | [`task-gw-req10-02-t06-story-gate`](./task-gw-req10-02-t06-story-gate/README.md) | Done |
| T07 | [`task-gw-req10-02-t07-audit-g3-as-of-done-ssot`](./task-gw-req10-02-t07-audit-g3-as-of-done-ssot/README.md) | Done (P6 G3 CLOSED · `gw_req10_02_audit_followup`) |

## Scope

1. Clean/normalize known legacy `RECEIVED`/`received` → `accepted` (`StoryLifecycleStatus.ACCEPTED.value`) in test/hosted Supabase; sqlite fixtures/demo DB **if** inventory found them (same canon — no separate long-lived path).
2. Slim `_parse_lifecycle_status`: remove permanent growing legacy dict; unknown values still raise / fail closed (`db_supabase.py:179–185` As-of-Done).
3. Remove absolute debug file I/O to `.cursor/debug-ba94c7.log` (and sibling `#region agent log` in that path) — H1 gateway. **As-of-Done:** removed.
4. Prefer simple cleanup over elaborate migration ceremony (operator: data is test).

## Out of scope

- Inventory (→ REQ10-01).
- Threads tree/reactions; spa; invent public APIs; REQ8.
- H8 / `list_all` scale note or SQL aggregate (skipped this wave).
- Expanding legacy map with new permanent synonyms.

## Verified current state

| Fact | Path |
|------|------|
| Slim `_parse_lifecycle_status` (no RECEIVED map; no debug I/O) | `src/core/infrastructure/db_supabase.py:179–185` (As-of-Done P3) |
| Hydrate call | `db_supabase.py:226` (As-of-Done; Historical was `:265`) |
| Enum ACCEPTED | `src/core/domain/contracts.py:21` |
| sqlite no legacy map on read | `src/core/infrastructure/db_sqlite.py:225` |
| Inventory feed (REQ10-01 Done) | [`inventory-gw-req10-01-lifecycle-status-2026-09-28.md`](../../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md) |
| P3 evidence | [`evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md`](../../../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) |
| Gate | [`task-gw-req10-02-t06-story-gate/story-acceptance-gate-STORY-GW-REQ10-02.md`](./task-gw-req10-02-t06-story-gate/story-acceptance-gate-STORY-GW-REQ10-02.md) PASS 2026-09-28T17:44:10Z |
| Tests | `tests/test_gw_req10_02_lifecycle_parse.py` |

## Target / AC

- [x] **AC-GW-REQ1002-01:** Known legacy RECEIVED cleaned to `accepted` in test/hosted data (and fixtures if inventory required) — H4 / GW-10-02. *(fixtures N/A; hosted operator blocker documented)*
- [x] **AC-GW-REQ1002-02:** Mapper no longer depends on permanent RECEIVED special-case (prefer remove) — H4 / GW-10-03.
- [x] **AC-GW-REQ1002-03:** Unknown lifecycle values still fail closed.
- [x] **AC-GW-REQ1002-04:** No `.cursor/debug-*.log` writes from production lifecycle path — H1 gateway / GW-10-04; `rg` clean under `doge-complaints-gateway/src`.

## Code touchpoints

- **As-of-Done:** `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status` `:179–185`; hydrate `:226`
- **Historical (pre-P3):** parser `:179–224` with legacy dict + debug I/O; hydrate `:265`
- Data cleanup against test/hosted Supabase (exact SQL/ops steps at P3 — do not invent new public APIs)
- sqlite fixtures only if inventory requires
- Tests: `tests/test_gw_req10_02_lifecycle_parse.py`

## Dependencies

- **Requires Done:** STORY-GW-REQ10-01.
- Cross-cut X-10-02 (`rg` no debug paths) — gateway piece in this story.
