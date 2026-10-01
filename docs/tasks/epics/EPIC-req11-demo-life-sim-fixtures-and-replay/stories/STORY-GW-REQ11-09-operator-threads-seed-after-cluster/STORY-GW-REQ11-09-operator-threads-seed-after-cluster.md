# STORY-GW-REQ11-09 — Operator threads seed after cluster (CLI + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-09-operator-threads-seed-after-cluster`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T10:52:44Z · gate PASS
- **Тип:** tooling / operator CLI — seed comments/reactions on **issues** (threads), not Auth provision, not fixture-story submit
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) § handoff / life-sim load; closes operator gap **B-THR-CLI** in load manual
- **Parent product:** REQ11 §6.1 load pipeline; §7.2 K1 (API Bearer actors OK)
- **decision_ref:** backlog REQ11-09 · REQ55 handoff / life-sim load · REQ11 §6.1/§7.2 K1 · operator 2026-10-01 threads seed after cluster · Meta sources
- **Justification:** operator 2026-10-01 — нужен **понятный терминальный** seed тредов **только после кластеризации** (non-empty issues); reuse Present Closed HTTP seed lib в `doge-threads`; без агентского чата на каждый прогон
- **Siblings:** soft STORY-GW-REQ11-03 (replay жалоб); soft STORY-GW-REQ11-04 (backdate + clustering handoff); soft STORY-GW-REQ11-05 / **08** (secrets / Bearer по `fixture_user_id`); soft STORY-GW-REQ11-06 (wipe — orthogonal); product seed lib Done в sibling `doge-threads` REQ11-01…04
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml`](../../../../gateway-active-packages/pkg-000107-20261001-gw-req11-09-operator-threads-seed-after-cluster.yaml)
- **Git:** `dev`
- **Operator locks:** fail-closed empty issues; reuse `closed_http_seed.seed_representative_issues`; actors Bearer by `fixture_user_id` (not `SERVICE_API_TOKEN`); never mutate pack JSON; no invent force-cluster / Closed APIs; **do not reuse** REQ11-07
- **Зависит от:** soft 03/04/05/08; pack replay + secrets Present; **hard** — non-empty `GET /node/issues` после cluster
- **Blocks:** operator self-serve threads seed → SPA verify
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** пути CLI / Make / RU manual ниже — **acceptance targets** до P3; этот scaffold **не** materialize код/мануал
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Не путать: эта **backlog-story** ≠ fixture **жалобы** (`stories.json`) ≠ Auth **жители** (08)
- **Scaffolded:** 2026-10-01T10:45:33Z

## Nested tasks (pkg-000107)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-09-t01-fail-closed-empty-issues-gate`](./task-gw-req11-09-t01-fail-closed-empty-issues-gate/README.md) | Done |
| T02 | [`task-gw-req11-09-t02-cli-make-thin-wrapper`](./task-gw-req11-09-t02-cli-make-thin-wrapper/README.md) | Done |
| T03 | [`task-gw-req11-09-t03-secrets-actors-handoff-seed`](./task-gw-req11-09-t03-secrets-actors-handoff-seed/README.md) | Done |
| T04 | [`task-gw-req11-09-t04-offline-unit-tests`](./task-gw-req11-09-t04-offline-unit-tests/README.md) | Done |
| T05 | [`task-gw-req11-09-t05-ru-manual-threads-seed`](./task-gw-req11-09-t05-ru-manual-threads-seed/README.md) | Done |
| T06 | [`task-gw-req11-09-t06-story-gate`](./task-gw-req11-09-t06-story-gate/README.md) | Done |
| T07 | [`task-gw-req11-09-t07-audit-g2-as-of-done-ssot`](./task-gw-req11-09-t07-audit-g2-as-of-done-ssot/README.md) | ⚪ Todo (audit wave `gw_req11_09_audit_followup`) |

## Goal

Дать оператору **один чистый вход** (CLI + Make/shell) для seed comments/reactions на **issues** после life-sim load: жёсткий **fail-closed gate «только после кластеризации»**, actors = Bearer из тех же `.secrets` что provision/replay (join `fixture_user_id`), thin wrapper над Present `seed_representative_issues`, и **мануал на русском** — чтобы прогон делался из терминала без агента.

## Scope

1. **Термины (lock):**
   - **Backlog-story** = эта постановка `STORY-GW-*`.
   - **Жалоба / fixture story** = строка pack `stories.json` → уже Present через `make simulate-life-sim` (не этот CLI).
   - **Треды** = comments/reactions на **issues** после clustering (этот CLI).
2. **Hard gate (fail-closed):** CLI **STOP**, если нет issues после clustering (`GET /node/issues` empty / нет handoff `issue_id`). Порядок load (документировать в manual): wipe (06) → provision жителей (05/08) → replay **жалоб** (`simulate-life-sim`) → **cluster** (`StoryClusterOrchestrator.process_all_pending()` / cron path) → **threads seed (этот CLI)** → SPA. Не invent HTTP force-cluster.
3. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_seed_threads.py` + `make life-sim-seed-threads`. Thin wrapper: poll/load issues → `GatewayIssueHandoff(issue_id, density)` → load actors from secrets → call Present lib.
4. **Reuse Present lib (не reinvent Closed APIs):** [`doge-threads/src/core/seed/closed_http_seed.py`](../../../../../../doge-threads/src/core/seed/closed_http_seed.py) — `seed_representative_issues(transport, issues, actors)`; density volume уже Done (sibling threads REQ11).
5. **Actors:** user Bearer из `.secrets/life_sim_users_creds_*` (или `LIFE_SIM_USERS_CREDS`); join key **`fixture_user_id`** — те же жители, что создаёт 05/08 и которыми submit’ит replay. **Запрет:** `SERVICE_API_TOKEN` как actor для comments/reactions seed.
6. **Handoff:** `issue_id` + `density` с node/issues после успешных жалоб + cluster (REQ11-04 handoff semantics).
7. **Connectivity note (verified, document in Verified):** provision secrets ↔ fixture `stories.json` ↔ replay join на `fixture_user_id`; threads seed потребляет **issues** + те же secrets как actors — не пишет в pack JSON.
8. **Smoke:** `--limit N` issues / dry-run where feasible; full after cluster non-empty.
9. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-threads-seed-manual-ru.md) — preconditions (cluster first), env (threads URL, secrets path), smoke, где смотреть handoff. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § threads; закрыть blocker **B-THR-CLI**.

## Out of scope

- Auth provision / pack-wave (STORY-GW-REQ11-05 / **08**).
- Submit fixture **жалоб** (`make simulate-life-sim` / REQ11-03) — уже Present; не дублировать в этом CLI.
- Content wipe (STORY-GW-REQ11-06).
- Inventing Closed HTTP comment/reaction APIs or density slope (Done in `doge-threads`).
- Invent HTTP force-cluster endpoint.
- SPA board/threads verify (sibling `20-…`).
- Mutating pack `users.json` / `stories.json`.
- Generating fixture story texts (pack-gen / removed 07).
- Implementing script/manual/code in the same turn as this backlog story (**name ≠ create**).

## Verified current state (As-of-Done P3 2026-10-01T10:52:44Z)

| Fact | Evidence |
|------|----------|
| Operator CLI / Make Present | `life_sim_seed_threads.py` + `make life-sim-seed-threads` |
| Fail-closed empty issues | exit 2 live local + offline unit |
| Reuse closed_http_seed | file-import `seed_representative_issues` |
| RU manual Present | `life-sim-threads-seed-manual-ru.md`; B-THR-CLI Closed |
| Offline tests | `test_gw_req11_09_seed_threads.py` 9 passed |
| Gate | [`story-acceptance-gate-STORY-GW-REQ11-09.md`](./task-gw-req11-09-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-09.md) PASS |
| Run summary | [`run-summary-20261001-1052-gw-req11-09-p3.md`](../../../../run-reports/run-summary-20261001-1052-gw-req11-09-p3.md) |
| Live full seed | **Leftover** — local `/node/issues` empty until operator cluster |

## Verified current state (Historical scaffold 2026-10-01T10:45:33Z)

| Fact | Evidence |
|------|----------|
| Closed HTTP seed lib Present | `doge-threads/src/core/seed/closed_http_seed.py` |
| Operator CLI / Make | **Absent** (pre-P3) |
| RU threads-seed manual | **Absent** (pre-P3) |
| B-THR-CLI | open (pre-P3) |

## Target / AC

- [x] **AC-GW-REQ1109-01:** CLI **fail-closed** без non-empty issues после clustering; documented order: … → cluster → threads seed.
- [x] **AC-GW-REQ1109-02:** Thin wrapper вызывает Present `seed_representative_issues` (не reinvent Closed APIs).
- [x] **AC-GW-REQ1109-03:** Actors = Bearer из life-sim secrets по тем же жителям (`fixture_user_id`); не service token.
- [x] **AC-GW-REQ1109-04:** Handoff `issue_id` + `density` с node/issues; Make/CLI entry Present (`life-sim-seed-threads` or locked name).
- [x] **AC-GW-REQ1109-05:** RU manual Present; operator can smoke/full from terminal without chat agent; load manual links § threads; B-THR-CLI closed.
- [x] **AC-GW-REQ1109-06:** Does not mutate pack JSON; K1 (no SPA resident login required for seed Pass); offline tests where feasible (gate empty-issues, handoff parse).

## Code touchpoints (named targets + Present reuse)

| Area | Path / note |
|------|-------------|
| **Reuse Present (threads)** | `doge-threads/src/core/seed/closed_http_seed.py` |
| **Target CLI** | `tests/sandbox/life_sim_seed_threads.py` (name lock P3) |
| **Target Make** | `make life-sim-seed-threads` (name lock P3) |
| **Secrets / actors** | `tests/sandbox/.secrets/life_sim_users_creds_*.json` — same as 05/08 + replay |
| **Upstream жалобы** | `make simulate-life-sim` + `LIFE_SIM_PACK_DIR` (not this story’s implement) |
| **Cluster** | `src/core/scheduler/cluster_cron.py` / `process_all_pending` |
| **RU manual** | `docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md` + link from life-sim load manual |
| **Orthogonal** | wipe 06; provision 05/08; SPA sibling `20-…` |

## Dependencies

- Soft: STORY-GW-REQ11-03, 04 Present; 05 Present; 08 soft (cleaner pack-wave secrets when Done).
- Hard: live node with **issues after clustering**; threads service up (profile `local` :8001); secrets covering actors.
- Operator: never seed before cluster; never commit secrets; wipe = 06 if restarting content.
