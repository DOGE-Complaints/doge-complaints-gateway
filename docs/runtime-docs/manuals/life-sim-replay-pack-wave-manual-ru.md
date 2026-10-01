# Life-sim replay pack-wave — операторский мануал (RU)

**Story:** STORY-GW-REQ11-10 · **Package:** `pkg-000108`  
**CLI:** `tests/sandbox/life_sim_replay_pack_wave.py` · **Make:** `life-sim-replay-pack-wave`  
**Связанный load-мануал:** [`life-sim-demo-node-load-manual-ru.md`](./life-sim-demo-node-load-manual-ru.md) § replay.

---

## Цель

Один терминальный вход: submit life-sim **жалоб** из pack `stories.json` с жёстким **fail-closed** `LIFE_SIM_PACK_DIR`, отдельным **wave-state** по `fixture_story_id`, resume и Bearer из тех же secrets, что provision (08) — без агентского чата на каждый прогон.

Legacy `make simulate-life-sim` остаётся, но **pack-wave = primary**.

---

## Preconditions (fail-closed)

| Требование | Значение |
|------------|----------|
| Pack | `LIFE_SIM_PACK_DIR` (или `PACK_DIR`) → каталог с `stories.json` |
| Secrets | `.secrets/life_sim_users_creds_*` покрывают `fixture_user_id` жалоб (после 08) |
| Gateway | профиль `DEMO_LIFE_SIM_PROFILE` (например `local`) + service token для stash |
| Wipe | content wipe (06) **до** full replay (см. load-мануал) |
| Запрет | писать статусы в fixture `stories.json`; invent intake APIs; invent HTTP force-cluster |

Без `LIFE_SIM_PACK_DIR` Make/CLI **STOP** (exit 2). Без secrets для user жалобы — **STOP**.

---

## Команды

Из `doge-complaints-gateway/`:

```bash
# Smoke (2 жалобы)
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/ls-20260930T0938Z-veerenni-yard-construction \
  DEMO_LIFE_SIM_PROFILE=local \
  make life-sim-replay-pack-wave LIMIT=2

# Dry-run (без HTTP; wave не помечает submitted)
LIFE_SIM_PACK_DIR=… LIFE_SIM_REPLAY_PACK_WAVE_DRY_RUN=1 \
  make life-sim-replay-pack-wave LIMIT=5

# Full pack (~1661) + явный wave id
LIFE_SIM_PACK_DIR=… WAVE_ID=demo-replay-1 DEMO_LIFE_SIM_PROFILE=local \
  make life-sim-replay-pack-wave
```

Эквивалент без Make:

```bash
LIFE_SIM_PACK_DIR=tests/sandbox/life_sim_packs/<pack_id> \
  .venv/bin/python tests/sandbox/life_sim_replay_pack_wave.py --limit 2
```

Reuse: `life_sim_replay_lib` + `simulation_runner` stash→submit (+ optional backdate lock B).

---

## Wave-state / resume

| Артефакт | Путь |
|----------|------|
| Fixture (read-only для status) | `$LIFE_SIM_PACK_DIR/stories.json` |
| Wave-state | `$LIFE_SIM_PACK_DIR/waves/<wave_id>/replay_state.json` (gitignored under packs) |

Статусы: `pending` | `submitted` | `failed`. Checkpoint после каждой жалобы. Resume **пропускает** `submitted`.

---

## Порядок load

wipe (06) → provision pack-wave (08) → **replay pack-wave (этот CLI)** → cluster → threads (09) → SPA.

---

## Связанные stories

- REQ11-03 foundation: `make simulate-life-sim` (legacy)
- REQ11-08 secrets: `make life-sim-provision-pack-wave`
- REQ11-09 threads: `make life-sim-seed-threads` (после cluster)
- Backlog: `docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-10-operator-pack-replay-complaints-wave.md`
