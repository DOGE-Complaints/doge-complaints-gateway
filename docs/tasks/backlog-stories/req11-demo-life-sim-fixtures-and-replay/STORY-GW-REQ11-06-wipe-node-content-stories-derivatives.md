# STORY-GW-REQ11-06 — Wipe node content (stories + derivatives + threads)

## Meta
- **Key:** `STORY-GW-REQ11-06-wipe-node-content-stories-derivatives`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (P3 2026-09-30T07:56:35Z · gate PASS)
- **Operative package:** [`../../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml`](../../gateway-active-packages/pkg-000105-20260930-gw-req11-06-wipe-node-content-stories-derivatives.yaml)
- **Done at:** 2026-09-30T07:56:35Z
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Тип:** tooling / ops wipe for life-sim
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) (replay into zero/wiped env)
- **Parent product:** REQ11 §3.3 API replay / wiped env
- **Justification:** `--wipe-confirmed` у `simulation_runner --life-sim` — только флаг precondition; **wipe HTTP/скрипта на диске нет** (note-gw-req11-03)
- **Siblings:** soft REQ11-03/04 (replay after wipe); threads seed consumes empty threads DB
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** soft STORY-GW-REQ11-02 (profile / Supabase env)
- **Blocks:** honest life-sim runbook Pass (manual + `Life_sim_load.plan`)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** target paths ниже — **не** materialize в этой постановке; implement только через Gateway Builder P1–P8

---

## Goal

Дать оператору **явный** скрипт полной очистки **контента ноды** перед life-sim load: stories и все производные (labels, clusters/candidates, issues, drafts, embeddings, …) **и** threads (comments, reaction marks, thread rows), **без** удаления Identity / admin пользователей.

---

## Scope

1. **Target script:** `tests/sandbox/life_sim_wipe_node_content.py` + Make target e.g. `make life-sim-wipe-node-content` — materialize **only on P3**.
2. Gateway DB via existing Supabase service-role / profile env (`SUPABASE_URL` + `SUPABASE_SERVICE_ROLE`); FK-safe delete order from **verified** tables (`REQUIRED_READINESS_TABLES` / sqlite schema) — не invent table names.
3. Threads persistence tables verified in doge-threads mappers: `thread_reaction_marks`, `thread_comments`, `thread_threads` (optional `THREADS_SUPABASE_*` override if separate project).
4. Require explicit `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1` (зеркало semantics `--wipe-confirmed` у runner).
5. Operator docs: link from [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) after Present.

## Out of scope

- DELETE Identity `auth.users` / admin / secrets files.
- DROP schema / reverse migrations.
- Invent HTTP wipe API on gateway or threads.
- Implementing the script in the same turn as this backlog story (**name ≠ create**).
- Full live life-sim fill.

---

## Verified current state (As-of-Done 2026-09-30T07:56:35Z)

| Fact | Evidence |
|------|----------|
| Wipe script + Make | `tests/sandbox/life_sim_wipe_node_content.py`, `life_sim_wipe_lib.py`, `make life-sim-wipe-node-content` |
| Confirm gate | refuses without `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1` (exit 2) |
| Gateway + threads wipe | FK-safe `REQUIRED_READINESS_TABLES` + marks→comments→threads; live DELETE 204 |
| Runner flag | `simulation_runner.py` `--wipe-confirmed` — precondition only (no DELETE) |
| Manual §5 | [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) Present links + dry-run |
| Offline tests | `tests/test_gw_req11_06_wipe_node_content.py` 8 passed |
| Identity | not touched (no `auth.users` DELETE) |

## Verified current state (Historical — scaffold / pre-P3)

| Fact | Evidence |
|------|----------|
| No wipe script on disk | Absent `life_sim_wipe_node_content.py` (operator confirm 2026-09-30) |
| Runner only checks flag | `simulation_runner.py` `--wipe-confirmed` / `LIFE_SIM_WIPE_CONFIRMED` — precondition text, no DELETE |
| Gateway tables (readiness) | `db_supabase.py` `REQUIRED_READINESS_TABLES` (stories, doge_issues, story_drafts, …) |
| Threads table names | `supabase_discussion_mappers.py` `thread_threads` / `thread_comments`; marks `thread_reaction_marks` |
| Manual / plan name wipe path | manual + `Life_sim_load.plan.md` — **acceptance targets**, not Present |

---

## Target / AC

- [x] **AC-GW-REQ1106-01:** Script + Make present; refuses without confirm flag.
- [x] **AC-GW-REQ1106-02:** Wipes gateway story stack + threads tables per verified schema; does **not** touch Identity users.
- [x] **AC-GW-REQ1106-03:** Manual § wipe links to Present script; dry-run mode documented.
- [x] **AC-GW-REQ1106-04:** Offline/unit or smoke evidence for confirm-gate + ordered deletes (P3 lock).

---

## Code touchpoints (As-of-Done)

- `tests/sandbox/life_sim_wipe_node_content.py` + `life_sim_wipe_lib.py` (Present)
- `Makefile` `life-sim-wipe-node-content` (Present)
- Docs: `life-sim-demo-node-load-manual-ru.md` §5 Present

### Historical (scaffold «named only» / pre-P3)

- `tests/sandbox/life_sim_wipe_node_content.py` (Absent)
- `Makefile` target (Absent)
- Docs: life-sim manual wipe section (target only)

## Dependencies

- Soft: profile env from REQ11-02
- Soft: life-sim load plan / manual (docs already name this story)

## Related

- [`Life_sim_load.plan`](../../../../../.cursor/plans/Life_sim_load.plan.md) — wipe phase before provision/replay
- [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § wipe
- note-gw-req11-03 wipe precondition
