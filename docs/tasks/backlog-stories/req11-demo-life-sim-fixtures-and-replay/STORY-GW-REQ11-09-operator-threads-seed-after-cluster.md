# STORY-GW-REQ11-09 — Operator threads seed after cluster (CLI + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-09-operator-threads-seed-after-cluster`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T10:52:44Z · P6 G2 CLOSED 2026-10-01T11:00:11Z · gate PASS · backlog kept
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-09-operator-threads-seed-after-cluster/STORY-GW-REQ11-09-operator-threads-seed-after-cluster.md)
- **Тип:** tooling / operator CLI — seed comments/reactions on **issues** (threads), not Auth provision, not fixture-story submit
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) § handoff / life-sim load; closes operator gap **B-THR-CLI** in load manual
- **Parent product:** REQ11 §6.1 load pipeline; §7.2 K1 (API Bearer actors OK)
- **Justification:** operator 2026-10-01 — нужен **понятный терминальный** seed тредов **только после кластеризации** (non-empty issues); reuse Present Closed HTTP seed lib в `doge-threads`; без агентского чата на каждый прогон
- **Siblings:** soft STORY-GW-REQ11-03 (replay жалоб); soft STORY-GW-REQ11-04 (backdate + clustering handoff); soft STORY-GW-REQ11-05 / **08** (secrets / Bearer по `fixture_user_id`); soft STORY-GW-REQ11-06 (wipe — orthogonal); product seed lib Done в sibling `doge-threads` REQ11-01…04
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** soft 03/04/05/08; pack replay + secrets Present; **hard** — non-empty `GET /node/issues` после cluster
- **Blocks:** operator self-serve threads seed → SPA verify
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** пути CLI / Make / RU manual ниже — **acceptance targets** до P3; эта постановка **не** materialize код/мануал
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Не путать: эта **backlog-story** ≠ fixture **жалобы** (`stories.json`) ≠ Auth **жители** (08)

---

## Goal

Дать оператору **один чистый вход** (CLI + Make/shell) для seed comments/reactions на **issues** после life-sim load: жёсткий **fail-closed gate «только после кластеризации»**, actors = Bearer из тех же `.secrets` что provision/replay (join `fixture_user_id`), thin wrapper над Present `seed_representative_issues`, и **мануал на русском** — чтобы прогон делался из терминала без агента.

---

## Scope

1. **Термины (lock):**
   - **Backlog-story** = эта постановка `STORY-GW-*`.
   - **Жалоба / fixture story** = строка pack `stories.json` → уже Present через `make simulate-life-sim` (не этот CLI).
   - **Треды** = comments/reactions на **issues** после clustering (этот CLI).
2. **Hard gate (fail-closed):** CLI **STOP**, если нет issues после clustering (`GET /node/issues` empty / нет handoff `issue_id`). Порядок load (документировать в manual): wipe (06) → provision жителей (05/08) → replay **жалоб** (`simulate-life-sim`) → **cluster** (`StoryClusterOrchestrator.process_all_pending()` / cron path) → **threads seed (этот CLI)** → SPA. Не invent HTTP force-cluster.
3. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_seed_threads.py` + `make life-sim-seed-threads`. Thin wrapper: poll/load issues → `GatewayIssueHandoff(issue_id, density)` → load actors from secrets → call Present lib.
4. **Reuse Present lib (не reinvent Closed APIs):** [`doge-threads/src/core/seed/closed_http_seed.py`](../../../../doge-threads/src/core/seed/closed_http_seed.py) — `seed_representative_issues(transport, issues, actors)`; density volume уже Done (sibling threads REQ11).
5. **Actors:** user Bearer из `.secrets/life_sim_users_creds_*` (или `LIFE_SIM_USERS_CREDS`); join key **`fixture_user_id`** — те же жители, что создаёт 05/08 и которыми submit’ит replay. **Запрет:** `SERVICE_API_TOKEN` как actor для comments/reactions seed.
6. **Handoff:** `issue_id` + `density` с node/issues после успешных жалоб + cluster (REQ11-04 handoff semantics).
7. **Connectivity note (verified, document in Verified):** provision secrets ↔ fixture `stories.json` ↔ replay join на `fixture_user_id`; threads seed потребляет **issues** + те же secrets как actors — не пишет в pack JSON.
8. **Smoke:** `--limit N` issues / dry-run where feasible; full after cluster non-empty.
9. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md`](../../../runtime-docs/manuals/life-sim-threads-seed-manual-ru.md) — preconditions (cluster first), env (threads URL, secrets path), smoke, где смотреть handoff. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § threads; закрыть blocker **B-THR-CLI**.

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

---

## Verified current state (As-of-Done 2026-10-01T11:00:11Z)

| Fact | Evidence |
|------|----------|
| Operator CLI + Make Present | `tests/sandbox/life_sim_seed_threads.py`, `life_sim_seed_threads_lib.py`, `make life-sim-seed-threads` |
| RU manual + B-THR-CLI | [`life-sim-threads-seed-manual-ru.md`](../../../runtime-docs/manuals/life-sim-threads-seed-manual-ru.md); load-manual **B-THR-CLI Closed** |
| Closed HTTP seed lib Present | `doge-threads/src/core/seed/closed_http_seed.py` — `seed_representative_issues`, `GatewayIssueHandoff`, `FixtureActor` |
| Offline tests | `tests/test_gw_req11_09_seed_threads.py` 9 passed; gate PASS 2026-10-01T10:52:44Z |
| Fail-closed empty issues | exit 2 when `GET /node/issues` empty; no invent force-cluster |
| Actors | Bearer from `.secrets/life_sim_users_creds_*` by `fixture_user_id`; not `SERVICE_API_TOKEN` |
| Cluster path | cron / `StoryClusterOrchestrator.process_all_pending()`; no HTTP force-cluster |
| Clustering wait helper | `life_sim_wait_clustering.sh` (sleep + handoff echo) — orthogonal to seed CLI |
| Replay жалоб Present | `make simulate-life-sim` → `tests/simulation_runner.py --life-sim` + `life_sim_replay_lib.py` |
| Pack path for replay | `LIFE_SIM_PACK_DIR` → pack `users.json`/`stories.json`; Make **не** экспортирует env |
| Join key residents ↔ жалобы | `fixture_user_id` in pack users, pack stories, secrets |
| Provision / secrets | REQ11-05 Present; REQ11-08 Done (pack-wave); secrets gitignored |
| Load manual order | wipe → provision → replay → cluster → **threads seed CLI** → SPA |
| Live leftover (G1 WAIVED) | full seed after cluster **not** run in P3 when issues empty (fail-closed OK) |
| Threads product stories | sibling `doge-threads` REQ11-01…04 **Done** (lib reused by CLI) |

## Verified current state (Historical — backlog scaffold 2026-10-01T10:18:01Z / pre-P3)

| Fact | Evidence |
|------|----------|
| Operator CLI / Make for threads seed | **Absent** (load manual blocker **B-THR-CLI**) |
| RU threads-seed manual | **Absent** |
| Closed HTTP seed lib / pytest harness | Present (threads sibling; unchanged) |
| Cluster path / wait helper / replay / pack join | Present foundation (unchanged) |
| Provision / secrets | REQ11-05 Present; REQ11-08 Todo at scaffold time |
| Gateway req11 INDEX | 01–06 Done; 08 Todo; **09 Absent** until this story |

---

## Target / AC

- [x] **AC-GW-REQ1109-01:** CLI **fail-closed** без non-empty issues после clustering; documented order: … → cluster → threads seed.
- [x] **AC-GW-REQ1109-02:** Thin wrapper вызывает Present `seed_representative_issues` (не reinvent Closed APIs).
- [x] **AC-GW-REQ1109-03:** Actors = Bearer из life-sim secrets по тем же жителям (`fixture_user_id`); не service token.
- [x] **AC-GW-REQ1109-04:** Handoff `issue_id` + `density` с node/issues; Make/CLI entry Present (`life-sim-seed-threads` or locked name).
- [x] **AC-GW-REQ1109-05:** RU manual Present; operator can smoke/full from terminal without chat agent; load manual links § threads; B-THR-CLI closed.
- [x] **AC-GW-REQ1109-06:** Does not mutate pack JSON; K1 (no SPA resident login required for seed Pass); offline tests where feasible (gate empty-issues, handoff parse).

---

## Code touchpoints (As-of-Done)

- `tests/sandbox/life_sim_seed_threads.py` + `life_sim_seed_threads_lib.py` + `make life-sim-seed-threads` (Present)
- `docs/runtime-docs/manuals/life-sim-threads-seed-manual-ru.md` + load-manual B-THR-CLI Closed (Present)
- `tests/test_gw_req11_09_seed_threads.py` (Present)
- Reuse: `doge-threads/src/core/seed/closed_http_seed.py` (Present)
- Secrets: `tests/sandbox/.secrets/life_sim_users_creds_*.json` (gitignored)
- Orthogonal: wipe 06; provision 05/08; cluster cron; SPA sibling `20-…`

### Historical (scaffold «named only» / pre-P3)

- Operator CLI / Make / RU threads-seed manual (Absent)
- B-THR-CLI open

---

## Dependencies

- Soft: STORY-GW-REQ11-03, 04 Present; 05 Present; 08 soft (cleaner pack-wave secrets when Done).
- Hard: live node with **issues after clustering**; threads service up (profile `local` :8001); secrets covering actors.
- Operator: never seed before cluster; never commit secrets; wipe = 06 if restarting content.
