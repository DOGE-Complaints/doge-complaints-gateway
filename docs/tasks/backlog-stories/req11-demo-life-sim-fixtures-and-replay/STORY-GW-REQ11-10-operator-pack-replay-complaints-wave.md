# STORY-GW-REQ11-10 — Operator pack-wave replay жалоб (CLI + wave-state + RU manual)

## Meta
- **Key:** `STORY-GW-REQ11-10-operator-pack-replay-complaints-wave`
- **Пакет:** [`req11-demo-life-sim-fixtures-and-replay/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) P3 2026-10-01T11:35:43Z · gate PASS · backlog kept
- **Pipeline:** [`../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/`](../../epics/EPIC-req11-demo-life-sim-fixtures-and-replay/stories/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md)
- **Тип:** tooling / operator CLI — submit pack **жалоб** (`stories.json`) в gateway; не Auth provision; не threads seed
- **Parent REQ:** [`55-req11-demo-life-sim-fixtures-and-replay.md`](../../../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) § profiled API replay; raises operator UX of REQ11-03 to pack-wave standard of 08/09
- **Parent product:** REQ11 §6.1 load pipeline (replay жалоб); §7.2 K1/K4
- **Justification:** operator 2026-10-01 audit — `make simulate-life-sim` Present, но **не** на стандарте 08/09: Make не fail-closed без `LIFE_SIM_PACK_DIR` (fallback на Absent flat `*_v0_1`); нет wave-state/resume по `fixture_story_id` (~1661 жалоб); нет dedicated RU manual. Нужен тот же класс CLI UX, что provision pack-wave
- **Siblings:** soft STORY-GW-REQ11-03 (Present replay — **reuse/refactor**); soft STORY-GW-REQ11-05 / **08** (secrets 1:1 `fixture_user_id`); soft STORY-GW-REQ11-04 (backdate path); soft STORY-GW-REQ11-06 / **09** (wipe / threads — **orthogonal**, после этого CLI)
- **Skill declared (future P3):** `python-pro`  
  Path: `.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`
- **Зависит от:** soft REQ11-03; soft 05/08 secrets; pack `stories.json` Present
- **Blocks:** operator self-serve full pack жалоб → cluster → threads (09)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)
- **Name ≠ create:** пути CLI / Make / wave JSON / RU manual ниже — **acceptance targets** до P3; эта постановка **не** materialize код/мануал
- **Note:** **STORY-GW-REQ11-07 removed** — номер **07 не переиспользовать**. Не путать: эта **backlog-story** ≠ fixture **жалобы** в `stories.json` ≠ Auth **жители** (08) ≠ **треды** (09)

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
5. **Операторский CLI** (target names — lock in P3): e.g. `tests/sandbox/life_sim_replay_pack_wave.py` + `make life-sim-replay-pack-wave`. **Reuse** [`life_sim_replay_lib.py`](../../../tests/sandbox/life_sim_replay_lib.py) + submit path из [`simulation_runner.py --life-sim`](../../../tests/simulation_runner.py) (stash service → submit user Bearer → optional backdate). Legacy `make simulate-life-sim` может остаться с deprecation note в manual (не удалять вслепую).
6. **Smoke:** `--limit N` / `SIMULATION_MAX_STORIES` + full pack; dry-run where feasible. Offline tests: fail-closed без pack; wave checkpoint/resume; missing creds gate.
7. **RU manual (target):** [`docs/runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md`](../../../runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md) — env, pack_id, resume, secrets, smoke. Cross-link из [`life-sim-demo-node-load-manual-ru.md`](../../../runtime-docs/manuals/life-sim-demo-node-load-manual-ru.md) § replay — убрать narrative «STOP only flat `*_v0_1`» как единственный путь; pack-wave = primary.
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

## Verified current state (As-of-Done 2026-10-01T11:41:52Z)

| Fact | Evidence |
|------|----------|
| Operator CLI + Make Present | `tests/sandbox/life_sim_replay_pack_wave.py` + `make life-sim-replay-pack-wave` |
| Fail-closed `LIFE_SIM_PACK_DIR` | Make exit 2 without pack; CLI `require_life_sim_pack_dir(require_stories=True)` → SystemExit 2 |
| Wave-state / resume | `life_sim_replay_wave_store.ReplayWaveStore` → `pack/waves/<wave_id>/replay_state.json` per `fixture_story_id` |
| RU manual + load primary | [`life-sim-replay-pack-wave-manual-ru.md`](../../../runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md); load-manual § replay pack-wave = primary |
| Offline tests | `tests/test_gw_req11_10_replay_pack_wave.py` 8 passed; gate PASS 2026-10-01T11:35:43Z |
| Reuse REQ11-03 path | `life_sim_replay_lib.py` + runner submit; Bearer by `fixture_user_id` |
| Legacy `simulate-life-sim` | Present (not fail-closed without pack; flat `*_v0_1` Absent) |
| REQ11-08 / 09 | Done pkg-000106 / pkg-000107 |
| Live leftover (G1 WAIVED) | LIMIT/full leftover Supabase Tunnel 403; dry-run LIMIT=2 ok |
| Pack example | `life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json` (~1661) |

## Verified current state (Historical — backlog scaffold 2026-10-01T11:24:48Z / pre-P3)

| Fact | Evidence |
|------|----------|
| REQ11-03 replay Present | `make simulate-life-sim` → `tests/simulation_runner.py --life-sim` + `life_sim_replay_lib.py` |
| Pack path in lib | `resolve_life_sim_pack_dir()` / `life_sim_stories_path()` — **optional**; без env → flat `dogestonia_life_sim_stories_v0_1.json` |
| Flat `*_v0_1` stories/users | **Absent** (cleaned 2026-09-30) |
| Make `simulate-life-sim` requires `LIFE_SIM_PACK_DIR` | **No** — unlike `life-sim-provision-pack-wave` |
| Wave-state / resume per `fixture_story_id` | **Absent** |
| Dedicated RU pack-wave replay manual | **Absent** (only load manual §6.2 + STOP note) |
| Join `fixture_user_id` → secrets Bearer | Present in runner (`creds_index.get(fixture_user_id)`) |
| REQ11-08 provision pack-wave | Done pkg-000106 — secrets + `LIFE_SIM_PACK_DIR` fail-closed standard |
| REQ11-09 threads seed | Done pkg-000107 — operator CLI standard; depends on жалобы + cluster first |
| Pack example | `life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction/stories.json` (~1661) |

---

## Target / AC

- [x] **AC-GW-REQ1110-01:** CLI/Make **fail-closed** без `LIFE_SIM_PACK_DIR`; читает pack `stories.json`; **никогда** не пишет туда статусы.
- [x] **AC-GW-REQ1110-02:** Wave-state JSON per wave отслеживает каждого `fixture_story_id`; checkpoint; resume skips `submitted`.
- [x] **AC-GW-REQ1110-03:** Bearer из life-sim secrets по `fixture_user_id`; fail-closed если creds отсутствуют для user жалобы.
- [x] **AC-GW-REQ1110-04:** Reuses REQ11-03 replay path (lib/runner); Make entry Present (`life-sim-replay-pack-wave` or locked name); smoke `--limit` / full.
- [x] **AC-GW-REQ1110-05:** RU manual Present; load manual § replay links pack-wave as primary; operator runs without chat agent.
- [x] **AC-GW-REQ1110-06:** K1 соблюдён; offline tests на pack gate / wave resume / missing creds где feasible; не invent intake APIs.

---

## Code touchpoints (As-of-Done)

- `tests/sandbox/life_sim_replay_pack_wave.py` + `life_sim_replay_wave_store.py` + `make life-sim-replay-pack-wave` (Present)
- `docs/runtime-docs/manuals/life-sim-replay-pack-wave-manual-ru.md` + load-manual pack-wave primary (Present)
- `tests/test_gw_req11_10_replay_pack_wave.py` (Present)
- Reuse: `life_sim_replay_lib.py`, `simulation_runner.py --life-sim`, legacy `make simulate-life-sim`
- Wave: `life_sim_packs/<pack_id>/waves/<wave_id>/replay_state.json`
- Secrets: `.secrets/life_sim_users_creds_*` (gitignored; same as 08)
- Downstream: cluster → `make life-sim-seed-threads` (09)

### Historical (scaffold «named only» / pre-P3)

- Pack-wave CLI / Make fail-closed / wave-state / dedicated RU manual (**Absent**)
- Only legacy `simulate-life-sim` + optional pack path in lib

---

## Dependencies

- Soft: STORY-GW-REQ11-03 Present (foundation to raise to pack-wave UX).
- Soft: STORY-GW-REQ11-05 / 08 Done — secrets covering pack users for жалобы.
- Pack with `stories.json` (+ scale meta) on disk.
- Operator: never commit secrets; wipe content = 06 if restarting; cluster/threads after Pass of this CLI.
