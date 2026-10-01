# Life-sim: наполнить демо-ноду «обжитыми» данными

| Field | Value |
|-------|--------|
| **utc** | `2026-09-30` |
| **SSOT** | Этот файл — детали настройки и runbook. Оркестрация: [`.cursor/plans/Life_sim_load.plan.md`](../../../../.cursor/plans/Life_sim_load.plan.md) |
| **Старт диалога** | [`cross-project-system-orientation.md`](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/cross-project-system-orientation.md) — ссылка из этого мануала |
| **Интервью params** | [`life-sim-node-load-run.md`](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/life-sim-node-load-run.md) (**не** opener диалога) |
| **Execute** | [`Life_sim_load.plan.md`](../../../../.cursor/plans/Life_sim_load.plan.md) |
| **Метод** | [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) |
| **Профиль по умолчанию** | `local` |
| **Parent** | [`REQ11`](../../../../docs/requirements%20backlog/REQ11-DOGEstonia-Uus-Veerenni-Demo-Life-Simulation.md) |

Малый canvas-seed (десятки историй) → [`seed-demo-data-runbook-ru.md`](./seed-demo-data-runbook-ru.md). Этот мануал — **REQ11 life-sim**: orientation → глубокое интервью params → wipe → ~200 жителей → истории → карточки → треды → SPA.

**Не копируй этот мануал в промпт** — передавай `@` на файл.

---

## 1. Зачем и кому

Сделать демо-ноду похожей на живой двор.

Цепочка ролей (жёстко):

1. **Orientation** — открывает кросс-проектный диалог.
2. **Промпт2** (`life-sim-node-load-run`) — проводит **интервью** по всем входящим переменным §4 (проработка, не форма) и **ждёт** «execute».
3. **`Life_sim_load.plan`** — полный прогон ноды Present-скриптами после execute.

Исходная точка: в Identity уже есть **первый админ** и service tokens в `.env`. Контент (stories / issues / threads) пустой или будет вытерт скриптом wipe (REQ11-06).

---

## 2. Картина простыми словами

```
Админ уже есть
  → orientation: карта системы
  → интервью: о чём нода / кто живёт / о чём жалуются (проработка params)
  → зафиксировать согласованные params (ops history прогона)
  → wipe stories и всего производного (включая треды) — REQ11-06
  → поднимаем пять сервисов
  → заселяем жителей (реальные аккаунты, не логин в SPA)
  → подаём истории → кластеризация → карточки
  → треды оживают → SPA без логина
```

| Слово | Смысл |
|-------|--------|
| **История params** | Согласованные в интервью переменные + utc + intent; ops convention пути — §4.5 (не отдельная STORY). |
| **История (story)** | Сырое обращение. На доске само не висит. |
| **Issue** | Карточка на доске после кластеризации. |
| **Wipe** | Удаление контента ноды скриптом REQ11-06 — **не** удаление людей в Identity. |
| **Force cluster** | Тот же вызов, что cron: `process_all_pending()`. |

---

## 3. Как стартовать

1. **Старт диалога:** [`cross-project-system-orientation.md`](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/cross-project-system-orientation.md) — `@` этот файл первым.
2. **Интервью:** в том же или следующем ходе `@` [`life-sim-node-load-run.md`](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/life-sim-node-load-run.md) + этот мануал + `Life_sim_load.plan` (без product REQ — замысел и locks уже здесь в §4). Промпт2 **не** «открывает диалог» — он **интервьюирует** по §4.
3. После закрытия interview агент фиксирует params (§4.5) и **ждёт** явного «execute» / «загружай».
4. На execute — только фазы [`Life_sim_load.plan.md`](../../../../.cursor/plans/Life_sim_load.plan.md).

---

## 4. Входные параметры (материал для интервью)

Параметры — замысел ноды **до** wipe/load. Два слоя. Промпт2 **прорабатывает** каждый блок (уточнения, примеры, trade-offs, осознанные defaults) — не чеклист «введи YAML».

### 4.1 Замки масштаба (обычно не трогать)

| Параметр | Социально | Технически |
|----------|-----------|------------|
| `profile_id` | Какую ноду наполняем (ноутбук vs hosted Уус-Веэрэнни) | `profiles/local.json` / `uus-veerenni.json` |
| `n_users` ≈ 200 | Сколько соседей «живут» в демо | Число аккаунтов provision |
| `stories_per_user` 8.5±2 clamp 1…20 | Кто-то пишет мало, кто-то много | Gauss |
| `lang_mix` 60/30/10 | Язык улицы: et / ru / en | Доли текстов |
| `calendar` 2026 + breakpoint 30.09 + 25/75 | Год демо; осенью «волна» | Даты + backdate |
| `seed` | Воспроизводимость «погоды» текстов | RNG seed |

### 4.2 Социальное направление (сюда смысл)

| Параметр | Социально | Как использовать |
|----------|-----------|------------------|
| `node_social_direction` | 1–3 предложения: *о чём эта нода* (двор, мусор, свет, стройка — не лозунги) | Обязательный компас в истории params |
| `user_context.personas` | Роли соседей | Пусто = нейтральные Resident N; иначе имя/язык из persona |
| `user_context.neighbourhood_tags` / `notes` | Микрогеография и быт | В историю запроса |
| `story_foci.themes` | О чём жалуются + `weight` + `blurbs` et/ru/en | Пусто = дефолтные civic blurbs; иначе тексты из тем |
| `cluster_force` / `threads_seed` / `spa_verify` | Собрать доску / оживить треды / проверить глазами | Pipeline knobs |

### 4.3 YAML-каркас (итог интервью — в чат или файл истории)

```yaml
profile_id: local
n_users: 200
stories_per_user: { mean: 8.5, sigma: 2.0, clamp: [1, 20] }
lang_mix: { et: 0.60, ru: 0.30, en: 0.10 }
calendar:
  year: 2026
  breakpoint: "2026-09-30T00:00:00Z"
  mass_pre: 0.25
  mass_post: 0.75
seed: 20260929
node_social_direction: |
  …
user_context:
  personas: []
  neighbourhood_tags: []
  notes: ""
story_foci:
  themes: []
```

### 4.4 Примеры направлений

**Двор Уус-Веэрэнни (defaults):** заполнить только `node_social_direction`, списки пустые → дефолтные blurbs / 200 / 8.5.

**Конфликт со стройкой:** `story_foci.themes` с весами на шум/пыль + personas у крана и у школы → другие тексты при load (направляющие интервью; Present fixtures = sample / generator REQ11-01).

### 4.5 Pack на диске (каждый прогон — отдельная подпапка)

**Root:** `tests/sandbox/life_sim_packs/<pack_id>/`

**`pack_id`:** `ls-<YYYYMMDD>T<HHMM>Z-<sense-slug>` — UTC snapshot + синтетика из `node_social_direction` (латиница/дефис, 2–5 слов).  
Примеры: `ls-20260930T1122Z-veerenni-yard-defaults`, `ls-20260930T1530Z-construction-noise-school`.

```
request.md      # utc + intent + согласованные params
params.json     # снимок §4.3
users.json
stories.json
meta.json
```

- Новый прогон → новый `pack_id`; **не** писать life-sim JSON в корень `tests/sandbox/`.
- Плоские `dogestonia_life_sim_*_v0_1.json` **сняты** (2026-09-30); не восстанавливать как SSOT.
- Secrets: `tests/sandbox/.secrets/life_sim_users_creds_<generation_id>.json` (вне pack).
- Canvas JSON — другой продукт; не смешивать.

**Load:** replay читает JSON **из pack**. As-of: `life_sim_replay_lib.py` ещё хардкодит Absent flat `*_v0_1` → до pack-path wiring execute = **STOP** или явная подстановка path (см. `Life_sim_load.plan`). Interview params — направляющие; mismatch foci→тексты = Partial.

---

## 5. Wipe: почистить базу от stories и производных — STORY-GW-REQ11-06

**Present (REQ11-06):** `tests/sandbox/life_sim_wipe_node_content.py` + `make life-sim-wipe-node-content`.

| Mode | Command |
|------|---------|
| Dry-run (no DELETE) | `LIFE_SIM_WIPE_DRY_RUN=1 make life-sim-wipe-node-content` или `…/life_sim_wipe_node_content.py --dry-run` |
| Live wipe | `LIFE_SIM_WIPE_CONFIRMED=1 make life-sim-wipe-node-content` или `--confirm-wipe` |

Confirm: **`--confirm-wipe`** или **`LIFE_SIM_WIPE_CONFIRMED=1`** (Make также принимает `CONFIRM_WIPE=1` → export). Без confirm скрипт **отказывается** (exit 2).

**Объём:** gateway `REQUIRED_READINESS_TABLES` (FK-safe order) + threads `thread_reaction_marks` → `thread_comments` → `thread_threads`. **Не** Identity/`auth.users`. **Не** invent wipe HTTP. **Не** DROP schema.

Env: `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE`. Optional separate threads DB: `THREADS_SUPABASE_URL` + `THREADS_SUPABASE_SERVICE_ROLE`.

`--wipe-confirmed` у `make simulate-life-sim` — только флаг precondition для replay, **не** DELETE (wipe делайте этим скриптом).

Story: [`STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`](../../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)

---

## 6. Runbook zero → Pass (после interview; на «execute»)

Зеркалит фазы [`Life_sim_load.plan.md`](../../../../.cursor/plans/Life_sim_load.plan.md). Детали STOP — там.

### 6.1 Предусловия

- Админ + `GATEWAY_API_TOKEN` / Supabase env на месте.
- Identity: `SMS_PROVIDER=file`.
- Gateway: cron не skipped (`CLUSTER_CRON_ENABLED=true`).
- Params согласованы в интервью (§4); история прогона зафиксирована или явно «defaults в чате».
- Wipe: Present REQ11-06 **или** операторский wipe + понимание `--wipe-confirmed`.

### 6.2 Шаги

1. **Wipe** — §5 после Present REQ11-06 (`make life-sim-wipe-node-content` + confirm); иначе STOP / operator wipe.
2. **Стек:** `./scripts/shell/local-five-serve-and-health.sh` — все ready.
3. **Provision:** предпочитайте pack-wave CLI — см. [`life-sim-provision-pack-wave-manual-ru.md`](./life-sim-provision-pack-wave-manual-ru.md) (`make life-sim-provision-pack-wave`, `LIFE_SIM_PACK_DIR`, wave-state, `skip`|`wipe-fixture-users`). Legacy entry: `make life-sim-provision-users`. Smoke `LIMIT=2` сначала. Gate: verified + gitignored `.secrets/`. Identity `SMS_PROVIDER=file` + `@dogestonia.me`.
4. **Replay:** из `life_sim_packs/<pack_id>/` + `DEMO_LIFE_SIM_PROFILE=local make simulate-life-sim` (STOP если runner path ещё на Absent flat `*_v0_1`).
5. **Force cluster** = тот же путь, что cron: `StoryClusterOrchestrator.process_all_pending()` ([`cluster_cron.py`](../../../src/core/scheduler/cluster_cron.py)); **poll** `GET /node/issues` до non-empty (не только sleep-helper).
6. **Threads:** [`life-sim-threads-seed-manual-ru.md`](./life-sim-threads-seed-manual-ru.md) — `make life-sim-seed-threads` (thin wrapper → `seed_representative_issues` + Bearer из secrets; handoff issue_id + density). **Fail-closed**, если issues empty.
7. **SPA:** anonymous `#/board`, `#/issue/:id`.

---

## 7. Pass / Fail / блокеры

| Итог | Когда |
|------|--------|
| **Pass** | wipe + provision + stories + issues + threads + SPA (+ params history) |
| **Partial** | LIMIT / MAX_STORIES / sample fixtures при несовпадении foci |
| **STOP** | Нет confirm wipe; wipe script Absent без operator wipe; cron skipped; 0 issues; 429 без плана |

| ID | Блокер |
|----|--------|
| B-WIPE | STORY-GW-REQ11-06 Done · wipe Present |
| B-FORCE | Нет HTTP force-cluster — использовать cron path `process_all_pending` |
| B-429 | Signup rate limit (provision) |
| B-THR-CLI | **Closed** — `make life-sim-seed-threads` Present ([threads-seed RU](./life-sim-threads-seed-manual-ru.md)) |

---

## 8. Инвентарь

| Слой | Path / факт |
|------|-------------|
| Orientation (старт диалога) | `docs/methodology/…/cross-project-system-orientation.md` |
| Промпт2 (интервью) | `docs/methodology/…/life-sim-node-load-run.md` |
| Reusable plan (execute) | `.cursor/plans/Life_sim_load.plan.md` |
| Wipe | STORY-GW-REQ11-06 · Present `life_sim_wipe_node_content.py` + `make life-sim-wipe-node-content` (Done) |
| Packs | `tests/sandbox/life_sim_packs/<pack_id>/` (UTC+sense; create on execute) |
| Flat life-sim `*_v0_1` | **Absent** (cleaned 2026-09-30) |
| Provision | `make life-sim-provision-pack-wave` (**Present** REQ11-08) · legacy `make life-sim-provision-users` (REQ11-05) · [pack-wave RU](./life-sim-provision-pack-wave-manual-ru.md) |
| Replay | `make simulate-life-sim` (**Present**) |
| Cluster | `process_all_pending` via cron (**Present**) |
| Threads seed | `make life-sim-seed-threads` (**Present** REQ11-09) · [RU](./life-sim-threads-seed-manual-ru.md) · lib `seed_representative_issues` |
| Stack | `scripts/shell/local-five-serve-and-health.sh` (**Present**) |
| Stories backlog | STORY-GW-REQ11-01…06,08,09 (07 **removed**) |

---

## 9. Related

| Doc | Role |
|-----|------|
| [orientation](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/cross-project-system-orientation.md) | **Старт диалога** |
| [life-sim-node-load-run](../../../../docs/methodology/Zeya888-builder-queue/prompts/architect/life-sim-node-load-run.md) | **Интервью** → STOP → execute |
| [Life_sim_load.plan](../../../../.cursor/plans/Life_sim_load.plan.md) | Полный e2e оркестратор |
| [REQ11](../../../../docs/requirements%20backlog/REQ11-DOGEstonia-Uus-Veerenni-Demo-Life-Simulation.md) | Product target |
| [INDEX REQ11 gateway](../../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md) | Stories 01–06 |
| [STORY-GW-REQ11-06](../../tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md) | Wipe tooling |
| [simulation-runner-manual](../testing/simulation-runner-manual.md) | Canvas `make simulate` |
| [clustering-story-to-issue](../clustering-story-to-issue.md) | Cron = `process_all_pending` |

---

*Live wipe/fill только по явной команде оператора.*
