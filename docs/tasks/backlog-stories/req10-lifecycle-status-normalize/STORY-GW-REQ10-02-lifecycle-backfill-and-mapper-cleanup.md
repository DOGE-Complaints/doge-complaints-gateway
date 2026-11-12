# STORY-GW-REQ10-02 — Cleanup lifecycle data + slim mapper + remove debug I/O

## Meta
- **Key:** `STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup`
- **Пакет:** [`req10-lifecycle-status-normalize/`](./INDEX.md)
- **Status:** Done · P3 2026-09-28T17:44:10Z · pkg-000099 T01–T06 · gate PASS
- **Тип:** data cleanup / adapter harden / debug removal
- **Parent REQ:** [`54-req10-lifecycle-status-normalize.md`](../../../requirements/54-req10-lifecycle-status-normalize.md) §2, §4, §5
- **Parent product:** REQ10 §6.3 **GW-10-02…04**; AC **H1** (gateway), **H4**
- **Justification:** [`audit-threads-board-persist-clean-vs-hack-2026-09-27.md`](../../../../../docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md) §3, §8
- **Skill declared:** `python-pro` · soft `sql-pro` (unused — no SQL migration)  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operator lock:** test data → **normalize/clean to canon immediately**; no permanent RECEIVED special-case; no dual-path complexity; H8 skipped this wave
- **Зависит от:** STORY-GW-REQ10-01 (Done)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Pipeline:** [`../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md)
- **Scaffolded:** 2026-09-28T17:27:26Z · pkg-000099
- **Verified:** 2026-09-28T17:44:10Z · [`run-summary`](../../run-reports/run-summary-20260928-1744-gw-req10-02-p3.md) · [`gate`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t06-story-gate/story-acceptance-gate-STORY-GW-REQ10-02.md) · [`evidence`](../../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md)

---

## Scope

1. Clean/normalize known legacy `RECEIVED`/`received` → `accepted` (`StoryLifecycleStatus.ACCEPTED.value`) in test/hosted Supabase; sqlite fixtures/demo DB **if** inventory found them (same canon — no separate long-lived path).
2. Slim `_parse_lifecycle_status`: remove permanent growing legacy dict; unknown values still raise / fail closed.
3. Remove absolute debug file I/O to `.cursor/debug-ba94c7.log` (and sibling `#region agent log` in that path) — H1 gateway.
4. Prefer simple cleanup over elaborate migration ceremony (operator: data is test).

## Out of scope

- Inventory (→ REQ10-01).
- Threads tree/reactions; spa; invent public APIs; REQ8.
- H8 / `list_all` scale note or SQL aggregate (skipped this wave).
- Expanding legacy map with new permanent synonyms.

## Verified current state (As-of-Done)

| Fact | Path |
|------|------|
| Slim `_parse_lifecycle_status` (no RECEIVED map; no debug I/O) | `src/core/infrastructure/db_supabase.py` |
| Enum ACCEPTED | `src/core/domain/contracts.py:21` |
| sqlite no legacy map on read | `src/core/infrastructure/db_sqlite.py:225` |
| Inventory feed (REQ10-01 Done) | [`inventory-gw-req10-01…`](../../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md) |
| P3 evidence | [`evidence-gw-req10-02…`](../../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) — fixtures N/A; hosted operator blocker |

## Target / AC

- [x] **AC-GW-REQ1002-01:** Known legacy RECEIVED cleaned to `accepted` in test/hosted data (and fixtures if inventory required) — H4 / GW-10-02. *(fixtures N/A; hosted operator blocker)*
- [x] **AC-GW-REQ1002-02:** Mapper no longer depends on permanent RECEIVED special-case (prefer remove) — H4 / GW-10-03.
- [x] **AC-GW-REQ1002-03:** Unknown lifecycle values still fail closed.
- [x] **AC-GW-REQ1002-04:** No `.cursor/debug-*.log` writes from production lifecycle path — H1 gateway / GW-10-04; `rg` clean under `doge-complaints-gateway/src`.

## Code touchpoints

- `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status`
- `tests/test_gw_req10_02_lifecycle_parse.py`
- Hosted cleanup blocked — see evidence note

## Dependencies

- **Requires Done:** STORY-GW-REQ10-01.
- Cross-cut X-10-02 (`rg` no debug paths) — gateway piece in this story.

## Nested tasks (pipeline pkg-000099 · Done P3 2026-09-28T17:44:10Z)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | [`task-gw-req10-02-t01-hosted-lifecycle-backfill`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t01-hosted-lifecycle-backfill/README.md) | Done | hosted blocker documented |
| **T02** | [`task-gw-req10-02-t02-fixture-cleanup-confirm`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t02-fixture-cleanup-confirm/README.md) | Done | fixtures N/A |
| **T03** | [`task-gw-req10-02-t03-slim-lifecycle-mapper`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t03-slim-lifecycle-mapper/README.md) | Done | slim mapper; fail-closed |
| **T04** | [`task-gw-req10-02-t04-remove-debug-io`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t04-remove-debug-io/README.md) | Done | remove debug I/O |
| **T05** | [`task-gw-req10-02-t05-lifecycle-parse-tests`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t05-lifecycle-parse-tests/README.md) | Done | AC-02…04 tests |
| **T06** | [`task-gw-req10-02-t06-story-gate`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t06-story-gate/README.md) | Done | AC-GW-REQ1002-01…04 gate PASS |
| **T07** | [`task-gw-req10-02-t07-audit-g3-as-of-done-ssot`](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t07-audit-g3-as-of-done-ssot/README.md) | Done | P6 G3 CLOSED · `gw_req10_02_audit_followup` |
