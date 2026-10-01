# STORY-GW-REQ11-10 — Operator pack-wave replay жалоб (CLI + wave-state + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-10-operator-pack-replay-complaints-wave`
- **Parent Epic:** [`../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md`](../../../EPIC-req11-demo-life-sim-fixtures-and-replay.md)
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T11:35:43Z · gate PASS · pkg-000108
- **Тип:** tooling / operator CLI — submit pack **жалоб** (`stories.json`) в gateway; не Auth provision; не threads seed
- **source:** [`../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md`](../../../../backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) § profiled API replay; raises operator UX of REQ11-03 to pack-wave standard of 08/09
- **Parent product:** REQ11 §6.1 load pipeline (replay жалоб); §7.2 K1/K4
- **decision_ref:** backlog REQ11-10 · REQ55 profiled API replay · REQ11 §6.1/§7.2 K1/K4 · operator 2026-10-01 pack-wave replay UX · Meta sources
- **Justification:** operator 2026-10-01 audit — `make simulate-life-sim` Present, но **не** на стандарте 08/09: Make не fail-closed без `LIFE_SIM_PACK_DIR` (fallback на Absent flat `*_v0_1`); нет wave-state/resume по `fixture_story_id` (~1661 жалоб); нет dedicated RU manual. Нужен тот же класс CLI UX, что provision pack-wave
- **Siblings:** soft STORY-GW-REQ11-03 (Present replay — **reuse/refactor**); soft STORY-GW-REQ11-05 / **08** (secrets 1:1 `fixture_user_id`); soft STORY-GW-REQ11-04 (backdate path); soft STORY-GW-REQ11-06 / **09** (wipe / threads — **orthogonal**, после этого CLI)
- **Skill declared:** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Operative package:** [`../../../../gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml`](../../../../gateway-active-packages/pkg-000108-20261001-gw-req11-10-operator-pack-replay-complaints-wave.yaml)
- **Git:** `dev`
- **Operator locks:** fail-closed `LIFE_SIM_PACK_DIR`; wave-state per `fixture_story_id`; reuse `life_sim_replay_lib` + runner; Bearer by `fixture_user_id`; never write statuses into pack `stories.json`; no invent intake/force-cluster; **do not reuse** REQ11-07
- **Зависит от:** soft REQ11-03; soft 05/08 secrets; pack `stories.json` Present
- **Blocks:** operator self-serve full pack жалоб → cluster → threads (09)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** пути CLI / Make / wave JSON / RU manual ниже — **acceptance targets** до P3; этот scaffold **не** materialize код/мануал
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Не путать: эта **backlog-story** ≠ fixture **жалобы** в `stories.json` ≠ Auth **жители** (08) ≠ **треды** (09)
- **Scaffolded:** 2026-10-01T11:30:34Z
- **Completed:** 2026-10-01T11:35:43Z

## Nested tasks (pkg-000108)

| ID | Folder | Status |
|----|--------|--------|
| T01 | [`task-gw-req11-10-t01-fail-closed-pack-dir-readonly-stories`](./task-gw-req11-10-t01-fail-closed-pack-dir-readonly-stories/README.md) | ✅ Done |
| T02 | [`task-gw-req11-10-t02-wave-state-checkpoint-resume`](./task-gw-req11-10-t02-wave-state-checkpoint-resume/README.md) | ✅ Done |
| T03 | [`task-gw-req11-10-t03-cli-make-reuse-replay-bearer`](./task-gw-req11-10-t03-cli-make-reuse-replay-bearer/README.md) | ✅ Done |
| T04 | [`task-gw-req11-10-t04-offline-unit-tests`](./task-gw-req11-10-t04-offline-unit-tests/README.md) | ✅ Done |
| T05 | [`task-gw-req11-10-t05-ru-manual-replay-pack-wave`](./task-gw-req11-10-t05-ru-manual-replay-pack-wave/README.md) | ✅ Done |
| T06 | [`task-gw-req11-10-t06-story-gate`](./task-gw-req11-10-t06-story-gate/README.md) | ✅ Done |
| T07 | [`task-gw-req11-10-t07-audit-g2-as-of-done-ssot`](./task-gw-req11-10-t07-audit-g2-as-of-done-ssot/README.md) | ✅ Done (audit G2) |

---

## Goal

Дать оператору **один чистый вход** (CLI + Make/shell) для submit life-sim **жалоб** из pack `stories.json`: жёсткий **fail-closed** `LIFE_SIM_PACK_DIR`, **отдельный wave-state** по каждому `fixture_story_id` (не внутри fixture JSON), **resume**, Bearer из тех же secrets что 08 (join `fixture_user_id`), и **мануал на русском** — чтобы прогон делался из терминала без агента на стандарте 08/09.

---

## Scope

1. **Термины (lock):**
   - **Backlog-story** = эта постановка `STORY-GW-*`.
   - **Жалоба / fixture story** = строка pack `stories.json` → API stash→submit (этот CLI).
   - **Жители** = Auth users (08); **треды** = comments/reactions на issues (09) — не этот CLI.
2. **Input (hard):** `LIFE_SIM_PACK_DIR` (или `PACK_DIR`) → immutable pack `stories.json` (+ `users.json`/`meta.json` для scale assert). Make/CLI **fail-closed** без pack (как `life-sim-provision-pack-wave`). **Запрет:** писать статусы replay в fixture `stories.json`.
3. **Wave-state JSON (отдельно от fixture):** per wave под pack, target e.g. `life_sim_packs/<pack_id>/waves/<wave_id>/replay_state.json` (точный path — P3). На каждого `fixture_story_id`: `pending` | `submitted` | `failed` (+ utc, error). **Checkpoint после каждой** жалобы. **Resume:** skip already `submitted`.
4. **Auth actors:** user Bearer из `.secrets/life_sim_users_creds_*` (или `LIFE_SIM_USERS_CREDS`); join **`fixture_user_id`** на строке жалобы — те же жители, что создаёт 08. **Fail-closed** если creds missing для user жалобы. Identity Supabase (как 08/replay).
5. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_replay_pack_wave.py` + `make life-sim-replay-pack-wave`. **Reuse** [`life_sim_replay_lib.py`](../../../../../tests/sandbox/life_sim_replay_lib.py) + submit path из [`simulation_runner.py --life-sim`](../../../../../tests/simulation_runner.py) (stash service → submit user Bearer → optional backdate). Legacy `make simulate-life-sim` может остаться с deprecation note в manual (не удалять вслепую).
6. **Smoke:** `--limit N` / `SIMULATION_MAX_STORIES` + full pack; dry-run where feasible. Offline tests: fail-closed без pack; wave checkpoint/resume; missing creds gate.
7. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md) — env, pack_id, resume, secrets, smoke. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § replay — убрать narrative «STOP only flat `*_v0_1`» как единственный путь; pack-wave = primary.
8. **Order in load:** wipe (06) → provision (08) → **replay жалоб (этот CLI)** → cluster → threads (09) → SPA.

## Out of scope

- Auth provision / pack-wave жителей (STORY-GW-REQ11-05 / **08**).
- Threads seed (STORY-GW-REQ11-09).
- Content wipe (STORY-GW-REQ11-06).
- Force cluster / invent HTTP force-cluster.
- Generating fixture story texts (pack-gen / removed 07).
- Mutating pack `users.json` / `stories.json` for status.
- Inventing intake/submit public APIs.
- SPA verify (sibling `20-…`).
- Implementing script/manual/code in the same turn as this backlog story (**name ≠ create**).

---

## Verified current state (As-of-Done P3 2026-10-01T11:35:43Z · P6 SSOT 2026-10-01T11:41:52Z)

| Fact | Evidence |
|------|----------|
| Operator CLI / Make Present | `life_sim_replay_pack_wave.py` + `make life-sim-replay-pack-wave` |
| Fail-closed pack dir | Make + `require_life_sim_pack_dir` → exit 2 |
| Wave-state Present | `ReplayWaveStore` → `pack/waves/<wave_id>/replay_state.json` |
| RU manual Present | `life-sim-replay-pack-wave-manual-ru.md`; load-manual pack-wave primary |
| Offline tests | `test_gw_req11_10_replay_pack_wave.py` 8 passed |
| Gate | [`story-acceptance-gate-STORY-GW-REQ11-10.md`](./task-gw-req11-10-t06-story-gate/story-acceptance-gate-STORY-GW-REQ11-10.md) PASS |
| Run summary | [`run-summary-20261001-1135-gw-req11-10-p3.md`](../../../../run-reports/run-summary-20261001-1135-gw-req11-10-p3.md) |
| Live LIMIT/full | **Leftover** — Supabase Tunnel 403 (G1 WAIVED) |

## Verified current state (Historical scaffold 2026-10-01T11:30:34Z / backlog 11:24:48Z)

| Fact | Evidence |
|------|----------|
| REQ11-03 replay Present | `make simulate-life-sim` + `life_sim_replay_lib.py` |
| Pack-wave CLI / Make fail-closed / wave-state / RU | **Absent** (pre-P3) |
| Make `simulate-life-sim` requires `LIFE_SIM_PACK_DIR` | **No** (pre-P3) |

## Target / AC

- [x] **AC-GW-REQ1110-01:** CLI/Make **fail-closed** без `LIFE_SIM_PACK_DIR`; читает pack `stories.json`; **никогда** не пишет туда статусы.
- [x] **AC-GW-REQ1110-02:** Wave-state JSON per wave отслеживает каждого `fixture_story_id`; checkpoint; resume skips `submitted`.
- [x] **AC-GW-REQ1110-03:** Bearer из life-sim secrets по `fixture_user_id`; fail-closed если creds отсутствуют для user жалобы.
- [x] **AC-GW-REQ1110-04:** Reuses REQ11-03 replay path (lib/runner); Make entry Present (`life-sim-replay-pack-wave` or locked name); smoke `--limit` / full.
- [x] **AC-GW-REQ1110-05:** RU manual Present; load manual § replay links pack-wave as primary; operator runs without chat agent.
- [x] **AC-GW-REQ1110-06:** K1 соблюдён; offline tests на pack gate / wave resume / missing creds где feasible; не invent intake APIs.

## Code touchpoints (As-of-Done)

| Area | Path / note |
|------|-------------|
| **CLI / Make** | `tests/sandbox/life_sim_replay_pack_wave.py` + `make life-sim-replay-pack-wave` (Present) |
| **Wave state** | `life_sim_replay_wave_store.py` → `pack/waves/<wave_id>/replay_state.json` |
| **Reuse** | `life_sim_replay_lib.py`, `simulation_runner.py --life-sim`, legacy `make simulate-life-sim` |
| **RU manual** | `life-sim-replay-pack-wave-manual-ru.md` + load-manual primary |
| **Tests** | `tests/test_gw_req11_10_replay_pack_wave.py` |
| **Secrets** | `.secrets/life_sim_users_creds_*` — same as 08 |
| **Downstream** | cluster → `make life-sim-seed-threads` (09) |

### Historical (scaffold «named only» / pre-P3)

- Pack-wave CLI / Make / wave-state / dedicated RU (**Absent**)

## Dependencies

- Soft: STORY-GW-REQ11-03 Present (foundation to raise to pack-wave UX).
- Soft: STORY-GW-REQ11-05 / 08 Done — secrets covering pack users for жалобы.
- Pack with `stories.json` (+ scale meta) on disk.
- Operator: never commit secrets; wipe content = 06 if restarting; cluster/threads after Pass of this CLI.
