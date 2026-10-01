# Life-sim threads seed after cluster — операторский мануал (RU)

**Story:** STORY-GW-REQ11-09 · **Package:** `pkg-000107`  
**CLI:** `tests/sandbox/life_sim_seed_threads.py` · **Make:** `life-sim-seed-threads`  
**Связанный load-мануал:** [`life-sim-demo-node-load-manual-ru.md`](./life-sim-demo-node-load-manual-ru.md) § threads.

---

## Цель

Один терминальный вход: seed **comments/reactions на issues** после life-sim load — **только после кластеризации** (non-empty `GET /node/issues`), actors = Bearer из тех же `.secrets`, что provision/replay (join `fixture_user_id`), thin wrapper над Present `seed_representative_issues` — без агентского чата.

---

## Термины (lock)

| Термин | Значение |
|--------|----------|
| Backlog-story | постановка `STORY-GW-*` |
| Жалоба / fixture story | строка pack `stories.json` → `make simulate-life-sim` (**не** этот CLI) |
| Треды | comments/reactions на **issues** после clustering (**этот** CLI) |

---

## Порядок load (fail-closed)

1. Wipe (REQ11-06) → 2. Provision жителей (05/08) → 3. Replay **жалоб** (`simulate-life-sim`) → 4. **Cluster** (`StoryClusterOrchestrator.process_all_pending()` / cron) → 5. **Threads seed (этот CLI)** → 6. SPA.

**STOP**, если `GET /node/issues` пуст / нет `issue_id` (exit 2).  
**Не** invent HTTP force-cluster — только cron / `process_all_pending`.

---

## Preconditions

| Требование | Значение |
|------------|----------|
| Issues | non-empty `GET $GATEWAY_URL/node/issues` после cluster |
| Threads | up (profile `local` → `http://127.0.0.1:8001`) |
| Secrets | `LIFE_SIM_USERS_CREDS` или `tests/sandbox/.secrets/life_sim_users_creds_*.json` |
| Actors | user Bearer по `fixture_user_id` — **запрет** `SERVICE_API_TOKEN` |
| Pack JSON | **никогда** не писать `users.json` / `stories.json` |
| Lib | reuse `doge-threads/.../closed_http_seed.seed_representative_issues` |

`density` = inbound story count, если поле Present (`density` / `story_count` / `len(story_ids)`); иначе `None` → volume FLOOR=1 в Present lib.

---

## Команды

Из `doge-complaints-gateway/`:

```bash
# Dry-run against local-five (override hosted GATEWAY_URL from .env)
GATEWAY_URL=http://127.0.0.1:8000 THREADS_URL=http://127.0.0.1:8001 \
  LIFE_SIM_SEED_THREADS_DRY_RUN=1 make life-sim-seed-threads

# Smoke (первые N issues) — только после non-empty cluster
GATEWAY_URL=http://127.0.0.1:8000 THREADS_URL=http://127.0.0.1:8001 \
  make life-sim-seed-threads LIMIT=2

# Full после non-empty cluster
GATEWAY_URL=http://127.0.0.1:8000 THREADS_URL=http://127.0.0.1:8001 \
  make life-sim-seed-threads
```

---

## Где смотреть handoff

| Артефакт | Path / факт |
|----------|-------------|
| Issues | `GET /node/issues` → `data.issues[].id` (+ density fields if Present) |
| Secrets actors | `.secrets/life_sim_users_creds_*` join `fixture_user_id` |
| Closed seed lib | `doge-threads/src/core/seed/closed_http_seed.py` |
| Clustering wait helper | `tests/sandbox/life_sim_wait_clustering.sh` (sleep; не seed CLI) |

---

## Pass / Fail

| Итог | Когда |
|------|--------|
| **Pass** | non-empty issues → actors from secrets → `seed_representative_issues` comments+reactions |
| **Fail-closed exit 2** | empty issues / no `issue_id` |
| **Leftover** | live full seed откладывается, если env issues empty — сначала cluster, не invent force-cluster |

---

## Related

| Doc | Role |
|-----|------|
| [life-sim-demo-node-load-manual-ru](./life-sim-demo-node-load-manual-ru.md) | полный load pipeline |
| [life-sim-provision-pack-wave-manual-ru](./life-sim-provision-pack-wave-manual-ru.md) | provision secrets |
| STORY-GW-REQ11-09 | backlog + pipeline AC |

---

*Live seed только при non-empty issues после cluster.*
