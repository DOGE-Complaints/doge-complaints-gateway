# STORY-GW-REQ11-06 — Wipe node content (stories + derivatives + threads)

## Meta
- **Key:** `STORY-GW-REQ11-06-wipe-node-content-stories-derivatives`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Тип:** tooling / ops wipe for life-sim
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) (replay into zero/wiped env)
- **decision_ref:** backlog REQ11-06 · REQ55 wiped-env · Life_sim_load plan · note-gw-req11-03 wipe precondition
- **Skill declared:** python-pro
- **Operative package:** [`../../../../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml`](../../../../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml)
- **Git:** `dev`
- **Operator locks:** `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`; gateway tables = `REQUIRED_READINESS_TABLES` only; threads = `thread_reaction_marks` → `thread_comments` → `thread_threads`; **no** Identity `auth.users` DELETE; **no** invent wipe HTTP API
- **Зависит от:** soft STORY-GW-REQ11-02 (profile / Supabase env)
- **Scaffolded:** 2026-09-30T07:51:07Z

## Nested tasks (pkg-000105)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-06-t01-wipe-script-confirm-gate`](./task-gw-req11-06-t01-wipe-script-confirm-gate/README.md) | Done |
| T02 | [`task-gw-req11-06-t02-fk-safe-gateway-deletes`](./task-gw-req11-06-t02-fk-safe-gateway-deletes/README.md) | Done |
| T03 | [`task-gw-req11-06-t03-threads-tables-wipe`](./task-gw-req11-06-t03-threads-tables-wipe/README.md) | Done |
| T04 | [`task-gw-req11-06-t04-dry-run-operator-docs`](./task-gw-req11-06-t04-dry-run-operator-docs/README.md) | Done |
| T05 | [`task-gw-req11-06-t05-offline-unit-tests`](./task-gw-req11-06-t05-offline-unit-tests/README.md) | Done |
| T06 | [`task-gw-req11-06-t06-story-gate`](./task-gw-req11-06-t06-story-gate/README.md) | Done |
| T07 | [`task-gw-req11-06-t07-audit-g1-as-of-done-ssot`](./task-gw-req11-06-t07-audit-g1-as-of-done-ssot/README.md) | Done · G1 CLOSED P6 |
| T08 | [`task-gw-req11-06-t08-audit-g2-manual-s8-inventory`](./task-gw-req11-06-t08-audit-g2-manual-s8-inventory/README.md) | Done · G2 CLOSED P6 |

## Goal

Дать оператору **явный** скрипт полной очистки **контента ноды** перед life-sim load: stories и все производные **и** threads, **без** удаления Identity / admin пользователей.

## Scope / AC — As-of-Done

- [x] **AC-GW-REQ1106-01:** Script + Make present; refuses without confirm flag.
- [x] **AC-GW-REQ1106-02:** Wipes gateway story stack + threads tables per verified schema; does **not** touch Identity users.
- [x] **AC-GW-REQ1106-03:** Manual § wipe links to Present script; dry-run mode documented.
- [x] **AC-GW-REQ1106-04:** Offline/unit or smoke evidence for confirm-gate + ordered deletes.

## Verified current state (As-of-Done 2026-09-30T07:56:35Z)

| Fact | Evidence |
|------|----------|
| Wipe script + Make | `tests/sandbox/life_sim_wipe_node_content.py`, `make life-sim-wipe-node-content` |
| Confirm gate | refuse exit 2 without `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1` |
| Gateway tables | `REQUIRED_READINESS_TABLES` FK-safe order via PostgREST DELETE |
| Threads tables | marks → comments → threads; live 204 |
| Manual | `life-sim-demo-node-load-manual-ru.md` §5 Present |
| Offline tests | `tests/test_gw_req11_06_wipe_node_content.py` 8 passed |
| Identity | not touched |

## Code touchpoints (As-of-Done)

| Area | Path |
|------|------|
| Wipe script | `tests/sandbox/life_sim_wipe_node_content.py` + `life_sim_wipe_lib.py` |
| Makefile | `life-sim-wipe-node-content` |
| Docs | `docs/runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md` §5 |
| Tests | `tests/test_gw_req11_06_wipe_node_content.py` |
