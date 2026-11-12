# Orchestrator runbook — Semantic Schema Runtime node-schema (SSR-16…18)

**Для кого:** агент-оркестратор (роль OP). Не пишет product-код. Не invent AC.  
**Пакет:** [`INDEX.md`](./INDEX.md)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Универсальный overnight:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**Этот файл — overlay очереди и continue-gate волны «одна активная схема ноды».** Где конфликт: **побеждает этот файл** (не пропускать следующую стори при FAIL gate; не включать SSR-06/07/12).  
**T-wave:** [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) — **исторический** (01–05 Done). Не стартовать 01–05 заново. **Не** переписывать G3 «`GET /tallinn/issues` stays». Не очередь этой волны.  
**Post-T-wave:** [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — **исторический** (08–15 Done). Не стартовать 08–15 заново. Не очередь этой волны.  
**Журнал волны (запуск OP):** [`wave-20260830-ssr-node-schema.md`](../../run-reports/operator-waves/wave-20260830-ssr-node-schema.md)  
**Process:** [`OP-gateway.process.md`](../../run-reports/operator-sessions/OP-gateway.process.md)  
**Fences P1–P8:** дословно из [`workflow.md`](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) / workflow-console — не перефразировать. Этот runbook не заменяет fence.

> **Updated:** 2026-08-30T14:09:10Z (`--print-utc-now`)

**Имя ветки = имя пакета:** `semantic-schema-runtime`  
(папка [`backlog-stories/semantic-schema-runtime/`](./INDEX.md); не `feat/gw-…`, не MVP-ветка).

---

## Шаг 0 — ветка пакета (до всего)

Это **первый** шаг OP. До него: не P1.3, не P2, не spawn BLD, не менять `gateway-active-package.current.yaml`. Оператору не писать, если команды ниже прошли.

Ветка **уже существует** после T-wave и post-T-wave. Цель шага: **switch** на канон, не плодить вторую ветку.

**Product git (факт диска, wave G0 2026-08-30T14:01:49Z):** workspace `DOGEstonia` **может не быть** git-корнем. Канон ветки SSR — nested [`doge-complaints-gateway/`](../../../../). Не `git switch` внутри nested `spa-app/` (там свой `.git`). T-wave/post-T-wave формулировку «корень = монорепо DOGEstonia» **не** копировать вслепую.

### 0.1 Корень и toplevel

Практический канон (факт: workspace без рабочего `.git`; product git = nested gateway):

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test -f docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
git rev-parse --abbrev-ref HEAD
```

| Факт | Действие |
|------|----------|
| cwd оканчивается на `/spa-app` | HALT. Выйти, повторить из gateway. |
| Нет `docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` | HALT. Не тот clone. |
| Уже на `semantic-schema-runtime` | Шаг 0.4 (status) → **G0 PASS**, дальше §1. |

### 0.2 Грязное дерево

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
git status --porcelain
```

Не `stash`, не `reset --hard`. Pre-existing dirty **не** на `dev` — тот же адаптер, что post-T-wave / wave G0: isolation = ветка `semantic-schema-runtime`; MVP dirt **не** коммитить в SSR P8. HALT только если dirty **и** HEAD не канон, или OP собирается смешать ES-04 product-fix с этой волной без команды.

### 0.3 Создать или перейти

Имя **ровно:** `semantic-schema-runtime`. Блоки ниже — **сверху вниз**; после первого успеха сразу **0.4**.

```bash
# Уже есть канон (ожидаемо после T-wave / post-T-wave)
git show-ref --verify --quiet refs/heads/semantic-schema-runtime && \
  git switch semantic-schema-runtime

# Наследие D-SSR-2 (старое имя) — переименовать, не плодить вторую ветку
git show-ref --verify --quiet refs/heads/feat/gw-semantic-schema-runtime && \
  git switch feat/gw-semantic-schema-runtime && \
  git branch -m semantic-schema-runtime

# Нет ни той ни другой — создать от текущего tip
git show-ref --verify --quiet refs/heads/semantic-schema-runtime || \
  git switch -c semantic-schema-runtime
```

Если ветка есть только на `origin`:

```bash
git fetch origin semantic-schema-runtime
git switch semantic-schema-runtime
```

Не делать: `push`, `push -u`, `--force`, `checkout -B` на MVP, создавать ветку из `spa-app`.

### 0.4 Подтверждение (это и есть G0)

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
git status -sb
```

В wave MD: `GATE: G0 branch=semantic-schema-runtime created_or_switched=yes wave=node-schema`.

**Только после этого** — §1 SSOT и очередь.

---

## 0. Кто ты и чего не делаешь

| Делаешь | Не делаешь |
|---------|------------|
| Очередь **16 → 17 → 18**, ветка **`semantic-schema-runtime`**, pkg на ней, spawn/resume BLD+VAL, прогон **continue-gate**, запись факта в wave MD | Product code, invent AC, push, правка `ClusterLens`, правка identity-service, recount [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) |
| При PASS gate — **сразу** следующая стори, **без** вопроса оператору | Ждать approve на запланированных G0 / G16–G18 |
| При FAIL gate — HALT очереди (не skip) | «BLOCKED → очередь дальше» из universal overnight **для этой волны** |
| При обнаружении запрещённого паттерна (ниже) — HALT | Чинить код в роли OP |
| Env `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION` (D-SSR-8) | Удаление civic engine / `ClusterLens`; GPT instruction pack (REQ-45); overlay SPA; IDX HTTP; новая SQL-миграция; публичный `GET /schema-active` |

Оператор на G0 / G16–G18 **не нужен**. Оператор нужен только: явный `стоп|stop|pause|halt`; gate FAIL после одного цикла P6 на той же стори; запрещённый паттерн в diff.

---

## 1. SSOT на диске (прочитать до очереди)

1. Этот файл.  
2. [`INDEX.md`](./INDEX.md) — D-SSR-1…**8**, §Seam validation, git branch.  
3. Стори очереди (полный markdown, таблица **Подзадачи** = порядок T00…Tn).  
4. Не SSOT: чат, память, `bullrun-launch-index.md` §«Актуальная точка» (там MVP — **не** переписывать этой волной). T-wave runbook и post-T-wave runbook — не очередь этой волны.

`builder_project: gateway`. Execution skill BLD: `python-pro`.  
`test_command` профиля: `cd doge-complaints-gateway && python3 -m pytest -q` ([`profiles.yaml`](../../../../../docs/methodology/Zeya888-builder-queue/specs/profiles.yaml) gateway).

Live hosted / `live_integration` **не** являются proof этой волны. Канон offline: `python3 -m pytest -q -m "not live_integration"` из `doge-complaints-gateway/`.

T-wave 01–05 **Done**. Post-T-wave 08–15 **Done**. Не recount pie T-wave. Dashboard: [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md) — Todo/Status с диска; pie T-wave **не** трогать.

---

## 2. Очередь (жёсткая)

**В очередь:** только node-schema product ниже, **по одной стори = один P1.3 pkg** (`input_mode: backlog_story`). Не один pkg на три стори.

| # | Story file | После неё gate | Дальше только если |
|---|------------|----------------|-------------------|
| 1 | [`STORY-GW-SSR-16-node-active-schema-config.md`](./STORY-GW-SSR-16-node-active-schema-config.md) | **G16** | G16 PASS |
| 2 | [`STORY-GW-SSR-17-intake-active-schema-gate.md`](./STORY-GW-SSR-17-intake-active-schema-gate.md) | **G17** | G17 PASS |
| 3 | [`STORY-GW-SSR-18-cluster-active-schema.md`](./STORY-GW-SSR-18-cluster-active-schema.md) | **G18** | G18 PASS → **конец волны** |

**Не в очередь:** [`STORY-GW-SSR-06-…`](./STORY-GW-SSR-06-analytical-index-later.md), [`STORY-GW-SSR-07-…`](./STORY-GW-SSR-07-processor-delivery-later.md), [`STORY-GW-SSR-12-…`](./STORY-GW-SSR-12-complementary-pair-matching.md) (D-SSR-6 / experimental). Если BLD открыл их в diff — HALT.

Параллель **16 ∥ 17 запрещена**. Порядок только 16 затем 17 затем 18. INDEX «16→17→18» читать как overnight serial.

`$queueSpec` для OP-старта (пример):

```text
Node-schema only: STORY-GW-SSR-16 then 17 then 18.
First: switch git branch named exactly semantic-schema-runtime (package folder). See runbook Шаг 0.
Follow doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md
Do NOT queue SSR-06 SSR-07 SSR-12.
Do NOT restart T-wave SSR-01…05.
Do NOT restart post-T-wave SSR-08…15.
Do NOT parallel 16 and 17.
```

---

## 3. Забор G0 — повторная проверка ветки

Создание/switch — **Шаг 0**. Здесь только verify перед P1.3 стори 16 (и перед каждой следующей стори, если OP подозревает смену ветки):

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
```

| Ожидание | Если нет |
|----------|----------|
| `HEAD` = **`semantic-schema-runtime`** | Вернуться к **Шагу 0**. Не исполнять P1.3/P3. |
| Working tree не смешивает MVP ES-04 product-fixes с SSR без явной команды | HALT и факт в wave |

На **этой** ветке P1.3 **может** переписать [`gateway-active-package.current.yaml`](../../gateway-active-package.current.yaml) на SSR `pkg-*.yaml`. На ветке MVP current.yaml на SSR **не** переключать.

Не трогать: `bullrun-launch-index.md` «Актуальная точка»; `gateway-mvp-dashboard.md`; `doge-identity-service/**`; GPT instruction pack (REQ-45).

Dashboard волны: только [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md) (recount Status с диска после Done стори). Pie T-wave 5/5 **не** менять.

**G0 PASS** → можно P1.3 стори 16. Оператору не писать.

---

## 4. Инъекция в BLD (каждая стори)

В prompt Builder, кроме fence и story file, **дословно** запреты INDEX:

- Не добавлять член в `ClusterLens` ([`types.py`](../../../../src/core/cluster/types.py) `:10–22`).
- Не удалять civic engine / `ClusterLens` (D-SSR-8: dual из активного pack.json; unbound legacy as-is).
- Не править `lens_dimension` под pack ([`engine.py`](../../../../src/core/cluster/engine.py) `:66–79`).
- Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` ([`gates.py`](../../../../src/core/promotion/gates.py) `:11–14`) и civic factory ([`service_factory.py`](../../../../src/core/infrastructure/service_factory.py) `:106–109`).
- Не класть binding-колонки в `required_columns_ready` ([`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py)).
- Не добавлять таблицы в `REQUIRED_READINESS_TABLES`.
- Не invent HTTP filter / новый intake path / IDX/QRY / публичный `GET /schema-active`.
- Не invent `DEFAULT_SCHEMA_PACK` и не «первый pack по списку». Env-имена **ровно** `NODE_SCHEMA_ID` и `NODE_SCHEMA_VERSION`.
- Не переносить `SCHEMA_PACKS_ROOT` в AppConfig в SSR-16 (остаётся `os.environ` в resolver).
- Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
- Не реализовывать SSR-06/07/12.
- Не писать новую SQL-миграцию.
- Не править GPT UI / instruction pack (REQ-45) — сеам в стори 17, не эта реализация.
- Overlay UI карточки spa-app — **не** эта волна.
- Не переименовывать geo `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` оставить.
- Не переписывать `docs/analysis/audit-gw-ssr-0*` / spa `audit-STORY-SPA-ES-*`.
- Не переписывать T-wave runbook G3 и не переписывать post-T-wave runbook как очередь.

VAL: read-only; те же rg/pytest, что в G* ниже; findings only.

---

## 5. Протокол continue-gate (G16–G18)

После P7 стори (VAL audit + story gate PASS) OP **сам** гонит команды ниже из корня `doge-complaints-gateway/` (или workspace root с `-c`).

- **PASS:** все команды exit 0 + rg-инварианты. Записать 3–6 строк в wave MD. Сразу следующая стори. Оператору не писать.  
- **FAIL:** не стартовать следующую стори. Один цикл P6 (BLD fix по VAL/gate) → повтор G*. Если снова FAIL → HALT волны, отчёт оператору (это единственная незапланированная остановка).  
- **Запрещённый паттерн в дифф** (см. §8) → HALT сразу, даже если pytest зелёный.

Полный `pytest -q -m "not live_integration"` **обязателен на G18**. После G16 — `test_gw_ssr_16_*`. После G17 — civic HTTP без binding 4xx + match/mismatch. G16 **не** требует полный suite (фикстуры HTTP без env — массовая правка в 17).

---

## 6. Стори: что выполнить и что проверить

### 6.1 SSR-16 → G16

**Сделать:** T01…T06 по стори. `NODE_SCHEMA_ID` + `NODE_SCHEMA_VERSION` в AppConfig, оба required, fail-fast. Boot `resolve_pack`. Не intake gate. Не перенос `SCHEMA_PACKS_ROOT`. Pytest helper (monkeypatch обеих переменных).

**G16 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_16_*.py
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```

**G16 PASS iff:**

- pytest `test_gw_ssr_16_*` зелёный;  
- missing env → `ConfigError`; существующий pack на диске грузится; несуществующий id → fail-fast;  
- оба поля required в `AppConfig` / `ENV_SCHEMA`;  
- `ClusterLens` members **ровно** baseline (10);  
- нет `GET /schema-active`; нет filter HTTP; нет `story_dimensions`.

**Зачем пауза:** 17 intake gate опирается на конфиг. Не стартовать 17, пока boot не fail-fast.

---

### 6.2 SSR-17 → G17

**Сделать:** T01…T05 по стори. Stash + submit: нет binding / `{}` / другой pack → `IntakeValidationError` (4xx). Совпадение → validate активного pack. Адаптировать civic HTTP fixtures (binding + env). Не GPT UI.

**G17 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_17_*.py
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "schema-active|/schema-filter|story_dimensions" src/core/api/asgi_app.py
```

**G17 PASS iff:**

- civic HTTP **без** binding → 4xx (не civic persist);  
- match `schema_binding` == `NODE_SCHEMA_*` → 202;  
- mismatch id или version → 4xx;  
- GPT UI files не в diff;  
- `ClusterLens` = 10; нет нового filter HTTP / `GET /schema-active`.

**Зачем:** без закрытого civic-входа 18 кластеризация всё ещё «клиент выбирает pack». Не стартовать 18 до G17 PASS.

---

### 6.3 SSR-18 → G18 → стоп волны

**Сделать:** T01…T05. Pack-ветка только если persist binding == конфиг ноды; иначе skip (лог). Unbound READY_FOR_PROFILE — civic as-is. Dual — флаг **активного** pack.json. Мануал склад vs рабочая. Smoke matrix: binding = env. Civic `test_clustering_engine.py` зелёный.

**G18 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_18_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration"   # полный offline — обязателен на G18
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "клиент выбирает любой pack|решает тело intake" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "NODE_SCHEMA_ID|NODE_SCHEMA_VERSION" docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```

**G18 PASS iff:**

- mismatch bound → skip (нет pack membership чужим pack.json);  
- civic unlabeled engine зелёный (`test_clustering_engine.py`);  
- полный offline pytest зелёный;  
- мануал **не** учит «клиент выбирает любой pack» / «решает тело intake» как текущий контракт; учит склад vs `NODE_SCHEMA_*` и 4xx;  
- `ClusterLens` baseline; нет filter HTTP / `GET /schema-active`;  
- не `live_integration` как proof.

**После G18 PASS:** волна node-schema **закрыта**. Не стартовать SSR-06/07/12. Dashboard: Todo 16–18 Done; pie T-wave не трогать. INDEX Status. Оператору — **итоговый** summary (очередь исчерпана). Это не запрос «можно ли 06».

---

## 7. Диаграмма

```text
Шаг 0 / G0  ветка semantic-schema-runtime
  → SSR-16 → G16         ← env + boot resolve
  → SSR-17 → G17         ← intake 4xx unless match
  → SSR-18 → G18         ← cluster only active pack; docs
  → STOP (не 06/07/12)
```

---

## 8. HALT немедленно (запрещённый паттерн)

Даже при зелёном pytest:

| Паттерн | Как увидеть |
|---------|-------------|
| Новый `ClusterLens` member **или** удаление civic engine | diff `src/core/cluster/types.py` / `engine.py` |
| Pack story через civic `_create_issue_for_cluster` без dual-флага / civic default False | diff orchestrator + `require_actionable` default |
| Binding в `required_columns_ready` | diff `db_supabase.py` |
| Новая таблица в `REQUIRED_READINESS_TABLES` | тот же файл |
| Файлы `doge-identity-service/` | `git diff --name-only` |
| Правка `gateway-mvp-dashboard.md` / bullrun «Актуальная точка» | git status |
| Код `story_dimensions` / processor delivery / SSR-12 matching | glob + story 12 files |
| Новый HTTP path filter / IDX / `GET /schema-active` | `asgi_app.py` |
| Новая SQL-миграция | `supabase/migrations/` |
| GPT UI / instruction pack | `GPT UI/` |
| Overlay UI / form builder spa | `spa-app/src` besides already-done path-rename |
| Перепись T-wave G3 / post-T-wave как очередь / closed P4 audits | `orchestrator-t-wave-runbook.md`, `orchestrator-post-t-wave-runbook.md`, `docs/analysis/audit-gw-ssr-0*` |
| Исполнение не на `semantic-schema-runtime` | Шаг 0 / G0 |
| Параллельный pkg 16 и 17 | два active P1.3 |
| Invent `DEFAULT_SCHEMA_PACK` / «первый по списку» | diff `schema.py` |

---

## 9. P8 / git

- Push **нет**, пока оператор явно не сказал.  
- P8 local — по session overnight (feat → test → docs). Не коммитить `.env` / secrets.  
- `docs/tasks/**` MVP/bullrun — не коммитить «заодно», если не часть SSR dashboard/INDEX/story.

---

## 10. Что записать в wave MD на каждом G*

```text
GATE: G<n> story=GW-SSR-<nn>
branch: semantic-schema-runtime
wave: node-schema
pytest: <command> exit=<code>
rg ClusterLens: baseline match yes/no
forbidden_pattern: none | <path>
decision: PASS continue | FAIL halt-for-P6 | HALT operator
```

Даты артефактов: `--print-utc-now` (не выдумывать).

---

## 11. После исчерпания очереди

Сообщить оператору: node-schema SSR-16, 17, 18 Done по G18; SSR-06/07/12 не запускались; ветка `semantic-schema-runtime`; рабочая схема ноды = `NODE_SCHEMA_ID` / `NODE_SCHEMA_VERSION`; merge/push/PA.2 REQ-51 — **ждут команды**. Не предлагать «заодно index».
