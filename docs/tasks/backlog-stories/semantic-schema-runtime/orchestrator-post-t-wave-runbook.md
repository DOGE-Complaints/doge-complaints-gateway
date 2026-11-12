# Orchestrator runbook — Semantic Schema Runtime post-T-wave

**Для кого:** агент-оркестратор (роль OP). Не пишет product-код. Не invent AC.  
**Пакет:** [`INDEX.md`](./INDEX.md)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Универсальный overnight:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**Этот файл — overlay очереди и continue-gate пост-T-wave.** Где конфликт: **побеждает этот файл** (не пропускать следующую стори при FAIL gate; не включать SSR-06/07/12).  
**T-wave:** [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) — **исторический** (01–05 Done). Не стартовать 01–05 заново. **Не** переписывать G3 «`GET /tallinn/issues` stays».  
**Fences P1–P8:** дословно из [`workflow.md`](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) / workflow-console — не перефразировать. Этот runbook не заменяет fence.

> **Updated:** 2026-08-29T17:32:04Z (`--print-utc-now`)

**Имя ветки = имя пакета:** `semantic-schema-runtime`  
(папка [`backlog-stories/semantic-schema-runtime/`](./INDEX.md); не `feat/gw-…`, не MVP-ветка).

---

## Шаг 0 — ветка пакета (до всего)

Это **первый** шаг OP. До него: не P1.3, не P2, не spawn BLD, не менять `gateway-active-package.current.yaml`. Оператору не писать, если команды ниже прошли.

Ветка **уже существует** после T-wave. Цель шага: **switch** на канон, не плодить вторую ветку.

Корень git = **монорепо** `DOGEstonia` (есть `docs/methodology/Zeya888-builder-queue/` и `doge-complaints-gateway/`). **Не** `git switch` внутри nested `spa-app/` (там свой `.git`).

### 0.1 Корень и toplevel

```bash
cd /Users/eslinko/Development/DOGEstonia
ROOT="$(git rev-parse --show-toplevel)"
echo "$ROOT"
git rev-parse --abbrev-ref HEAD
```

| Факт | Действие |
|------|----------|
| `$ROOT` оканчивается на `/spa-app` | HALT. Выйти в монорепо, повторить. |
| Нет `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md` | HALT. Не тот clone. |
| Уже на `semantic-schema-runtime` | Шаг 0.4 (status) → если чисто, **G0 PASS**, дальше §1. |

### 0.2 Грязное дерево

```bash
git status --porcelain
```

Непусто и это не файлы **этого** пакета (runbook/INDEX/stories SSR / dashboard волны) → **HALT**. Не `stash`, не `reset --hard`, не мешать MVP ES-04 с этой волной.

### 0.3 Создать или перейти

Имя **ровно:** `semantic-schema-runtime`. Блоки ниже — **сверху вниз**; после первого успеха сразу **0.4**.

```bash
# Уже есть канон (ожидаемо после T-wave)
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
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
git status -sb
```

В wave MD: `GATE: G0 branch=semantic-schema-runtime created_or_switched=yes wave=post-t-wave`.

**Только после этого** — §1 SSOT и очередь.

---

## 0. Кто ты и чего не делаешь

| Делаешь | Не делаешь |
|---------|------------|
| Очередь **08 → 09 → 10 → 13 → 11 → 14 → 15**, ветка **`semantic-schema-runtime`**, pkg на ней, spawn/resume BLD+VAL, прогон **continue-gate**, запись факта в wave MD | Product code, invent AC, push, правка `ClusterLens`, правка identity-service, recount [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) |
| При PASS gate — **сразу** следующая стори, **без** вопроса оператору | Ждать approve на запланированных G0 / G8–G15 |
| При FAIL gate — HALT очереди (не skip) | «BLOCKED → очередь дальше» из universal overnight **для этой волны** |
| При обнаружении запрещённого паттерна (ниже) — HALT | Чинить код в роли OP |
| SPA path-rename **трёх** Gateway*Repository + spa-16/15 path strings (D-SSR-7) | Overlay UI карточки; form builder; GPT instruction pack |

Оператор на G0 / G8–G15 **не нужен**. Оператор нужен только: явный `стоп|stop|pause|halt`; gate FAIL после одного цикла P6 на той же стори; запрещённый паттерн в diff.

---

## 1. SSOT на диске (прочитать до очереди)

1. Этот файл.  
2. [`INDEX.md`](./INDEX.md) — D-SSR-1…**7**, §Seam validation, git branch.  
3. Стори очереди (полный markdown, таблица **Подзадачи** = порядок T00…Tn).  
4. Не SSOT: чат, память, `bullrun-launch-index.md` §«Актуальная точка» (там MVP — **не** переписывать этой волной). T-wave runbook — не очередь этой волны.

`builder_project: gateway`. Execution skill BLD: `python-pro`.  
`test_command` профиля: `cd doge-complaints-gateway && python3 -m pytest -q` ([`profiles.yaml`](../../../../../docs/methodology/Zeya888-builder-queue/specs/profiles.yaml) gateway).

Live hosted / `live_integration` **не** являются proof этой волны. Канон offline: `python3 -m pytest -q -m "not live_integration"` из `doge-complaints-gateway/`.

T-wave 01–05 **Done**. Не recount pie T-wave. Dashboard: [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md) — Todo/Status с диска; pie T-wave **не** трогать.

---

## 2. Очередь (жёсткая)

**В очередь:** только post-T-wave product ниже, **по одной стори = один P1.3 pkg** (`input_mode: backlog_story`). Не один pkg на семь стори.

| # | Story file | После неё gate | Дальше только если |
|---|------------|----------------|-------------------|
| 1 | [`STORY-GW-SSR-08-tallinn-civic-schema-pack.md`](./STORY-GW-SSR-08-tallinn-civic-schema-pack.md) | **G8** | G8 PASS |
| 2 | [`STORY-GW-SSR-09-hosted-apply-and-pack-image.md`](./STORY-GW-SSR-09-hosted-apply-and-pack-image.md) | **G9** | G9 PASS |
| 3 | [`STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md`](./STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) | **G10** | G10 PASS |
| 4 | [`STORY-GW-SSR-13-abstract-node-public-api.md`](./STORY-GW-SSR-13-abstract-node-public-api.md) | **G13** | G13 PASS |
| 5 | [`STORY-GW-SSR-11-pack-declared-issue-projection.md`](./STORY-GW-SSR-11-pack-declared-issue-projection.md) | **G11** | G11 PASS |
| 6 | [`STORY-GW-SSR-14-docs-abstract-node-paradigm.md`](./STORY-GW-SSR-14-docs-abstract-node-paradigm.md) | **G14** | G14 PASS |
| 7 | [`STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md`](./STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) | **G15** | G15 PASS → **конец волны** |

**Не в очередь:** [`STORY-GW-SSR-06-…`](./STORY-GW-SSR-06-analytical-index-later.md), [`STORY-GW-SSR-07-…`](./STORY-GW-SSR-07-processor-delivery-later.md), [`STORY-GW-SSR-12-…`](./STORY-GW-SSR-12-complementary-pair-matching.md) (D-SSR-6 / experimental). Если BLD открыл их в diff — HALT.

Параллель **08 ∥ 09 запрещена overnight** (как 03 ∥ 04 в T-wave). Порядок только 08 затем 09. INDEX «08 ∥ 09» как граф **не** читать как overnight.

SSR-11 **после** SSR-13 (D-SSR-7: канон `/node/issues`). Не исполнять 11 до G13 PASS.

Внутри стори: субтаски **по ID**. Не пропускать T00/T01. Gate-таск стори = story acceptance; continue-gate G* этого runbook — **дополнительно** после P7/VAL той стори.

`$queueSpec` для OP-старта (пример):

```text
Post-T-wave only: STORY-GW-SSR-08 then 09 then 10 then 13 then 11 then 14 then 15.
First: switch git branch named exactly semantic-schema-runtime (package folder). See runbook Шаг 0.
Follow doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-post-t-wave-runbook.md
Do NOT queue SSR-06 SSR-07 SSR-12.
Do NOT restart T-wave SSR-01…05.
Do NOT parallel 08 and 09.
```

---

## 3. Забор G0 — повторная проверка ветки

Создание/switch — **Шаг 0**. Здесь только verify перед P1.3 стори 08 (и перед каждой следующей стори, если OP подозревает смену ветки):

```bash
cd /Users/eslinko/Development/DOGEstonia
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
```

| Ожидание | Если нет |
|----------|----------|
| `HEAD` = **`semantic-schema-runtime`** | Вернуться к **Шагу 0**. Не исполнять P1.3/P3. |
| Working tree не смешивает MVP ES-04 product-fixes с SSR без явной команды | HALT и факт в wave |

На **этой** ветке P1.3 **может** переписать [`gateway-active-package.current.yaml`](../../gateway-active-package.current.yaml) на SSR `pkg-*.yaml`. На ветке MVP current.yaml на SSR **не** переключать.

Не трогать: `bullrun-launch-index.md` «Актуальная точка»; `gateway-mvp-dashboard.md`; `doge-identity-service/**`; GPT instruction pack (REQ-45).

Dashboard волны: только [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md) (recount Status с диска после Done стори). Pie T-wave 5/5 **не** менять.

**G0 PASS** → можно P1.3 стори 08. Оператору не писать.

---

## 4. Инъекция в BLD (каждая стори)

В prompt Builder, кроме fence и story file, **дословно** запреты INDEX:

- Не добавлять член в `ClusterLens` ([`types.py`](../../../../src/core/cluster/types.py) `:10–22`).
- Не править `lens_dimension` под pack ([`engine.py`](../../../../src/core/cluster/engine.py) `:66–79`).
- Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` ([`gates.py`](../../../../src/core/promotion/gates.py) `:11–14`) и civic factory ([`service_factory.py`](../../../../src/core/infrastructure/service_factory.py) `:106–109`).
- Не класть binding-колонки в `required_columns_ready` ([`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py)).
- Не добавлять таблицы в `REQUIRED_READINESS_TABLES`.
- Не invent HTTP filter / новый intake path / IDX/QRY.
- Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
- Не реализовывать SSR-06/07/12.
- Не переименовывать geo `CLUSTER_GEO_SCOPE=settlement:tallinn`; pack id `tallinn_civic` оставить.
- Не оставлять alias `/tallinn/*` после SSR-13 (D-SSR-7 hard cut).
- Overlay UI карточки spa-app — **не** эта волна (кроме URL трёх репозиториев в SSR-13).
- Не переписывать `docs/analysis/audit-gw-ssr-0*` / spa `audit-STORY-SPA-ES-*`.
- Не переписывать T-wave runbook G3.

VAL: read-only; те же rg/pytest, что в G* ниже; findings only.

---

## 5. Протокол continue-gate (G8–G15)

После P7 стори (VAL audit + story gate PASS) OP **сам** гонит команды ниже из корня `doge-complaints-gateway/` (или workspace root с `-c`).

- **PASS:** все команды exit 0 + rg-инварианты. Записать 3–6 строк в wave MD. Сразу следующая стори. Оператору не писать.  
- **FAIL:** не стартовать следующую стори. Один цикл P6 (BLD fix по VAL/gate) → повтор G*. Если снова FAIL → HALT волны, отчёт оператору (это единственная незапланированная остановка).  
- **Запрещённый паттерн в diff** (см. §8) → HALT сразу, даже если pytest зелёный.

Полный `pytest -q -m "not live_integration"` **обязателен на G15**. После G8 и G10 — бандл стори + civic regression. G13 **не** требует полный suite URL (pytest paths — G15). G9 **не** требует live hosted apply.

---

## 6. Стори: что выполнить и что проверить

### 6.1 SSR-08 → G8

**Сделать:** T00…T06 по стори. Pack `schema-packs/tallinn_civic/v1/`. Civic path без binding **не** ломать. Не HTTP. Не `ClusterLens`.

**G8 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_08_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py tests/test_gw_tax_02_cluster_axis_expansion.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
```

**G8 PASS iff:**

- pytest SSR-08 зелёный; civic clustering regression зелёный;  
- каталог `tallinn_civic/v1` резолвится;  
- `ClusterLens` members **ровно** baseline T-wave (10);  
- нет нового filter HTTP; нет `story_dimensions`.

**Зачем пауза:** 10 dual и 15 pack-сценарий опираются на этот pack. Не стартовать 09, пока pack не load.

---

### 6.2 SSR-09 → G9

**Сделать:** T01…T03 по стори. **Live hosted apply не proof** (как `live_integration` в T-wave). G9 = артефакты на диске + инварианты omit-probe / `/ready`.

**G9 команды:**

```bash
cd doge-complaints-gateway
test -f supabase/migrations/20260828_1400_gw_ssr_02_stories_schema_binding.sql
rg -n "required_columns_ready" -A 40 src/core/infrastructure/db_supabase.py
rg -n "schema_id|bound_schema_version|structured_payload" src/core/infrastructure/db_supabase.py
test -d schema-packs
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```

**G9 PASS iff:**

- migration SQL на диске;  
- `required_columns_ready` **не** содержит binding-колонок;  
- `schema-packs/` в дереве gateway (resolver default);  
- нет нового HTTP;  
- в gate/wave: явная пометка hosted apply = оператор/деплой, не overnight proof.

**Зачем:** без этого 08 pack на host молча теряет payload; overnight не ждёт Railway.

---

### 6.3 SSR-10 → G10

**Сделать:** T01…T03 / R1 по стори. Dual **opt-in** в pack.json; default = exact-only (legal_process). Не расширять `ClusterLens`.

**G10 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_10_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py tests/test_gw_ssr_04_*.py tests/test_gw_ssr_05_*.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```

**G10 PASS iff:**

- dual fixture: civic lens value **и** pack `lens_id` на одном `story_id`;  
- pack без dual-ключа = T-wave exact-only (legal_process зелёный);  
- civic unbound зелёный; `ClusterLens` = 10; нет pack lens в enum;  
- нет нового HTTP.

---

### 6.4 SSR-13 → G13 (до SSR-11)

**Сделать:** T01…T06. Роуты `/node/*` + rename handlers; SPA три repository + unit tests; spa-16 + REQ-51 sibling path. **Hard cut** `/tallinn/*`. Полный pytest URL — **не** этот gate (→ G15).

**G13 команды:**

```bash
cd /Users/eslinko/Development/DOGEstonia
rg -n "/tallinn/" doge-complaints-gateway/src/core/api
rg -n "/node/issues|/node/network-pulse|/node/emerging-signals" doge-complaints-gateway/src/core/api/asgi_app.py
rg -n "/tallinn/" spa-app/src/repositories/GatewayIssueRepository.js spa-app/src/repositories/GatewayNetworkPulseRepository.js spa-app/src/repositories/GatewayEmergingSignalsRepository.js
rg -n "GET /node/issues|/tallinn/issues" spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md
```

**G13 PASS iff:**

- `/tallinn/` **отсутствует** в `doge-complaints-gateway/src/core/api`;  
- канон пять семейств на `/node/…` в `asgi_app.py` (GET/POST issues, get by id, Pulse, Emerging) + `PUBLIC_ROUTES`;  
- три SPA repository **без** `/tallinn/` в URL;  
- spa-16 называет `GET /node/issues`, не «keep `/tallinn/issues`»;  
- нет alias (нет второго префикса в asgi).

Красный gateway pytest на старый path **допустим** до G15. Не HALT G13 из-за `test_req24_*` / `test_gw_ssr_05_*` assert `@app.get("/tallinn/issues")`.

---

### 6.5 SSR-11 → G11

**Сделать:** R1, T01…T03. Allowlist полей на карточку pack Issue. Public read = **`GET /node/issues`**. Overlay UI spa — нет.

**G11 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_11_*.py
rg -n "structured_payload" src/core/projection/dto.py
rg -n "/node/issues" src/core/api/asgi_app.py
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
```

**G11 PASS iff:**

- public dict **не** содержит целиком `structured_payload`;  
- civic Issues без новых required keys;  
- path канон `/node/issues` (не `/tallinn/issues`);  
- factory civic default на месте;  
- spa overlay UI не в diff (кроме уже сделанного path-rename в 13).

---

### 6.6 SSR-14 → G14

**Сделать:** инвентарь T01 стори (каждый файл patched или N/A). Не аудиты. Не geo `settlement:tallinn`. Не T-wave G3.

**G14 команды:**

```bash
cd /Users/eslinko/Development/DOGEstonia
rg -n "/tallinn/(issues|network-pulse|emerging-signals)" \
  doge-complaints-gateway/docs/runtime-docs \
  doge-complaints-gateway/docs/requirements/51-semantic-schema-runtime.md \
  doge-complaints-gateway/docs/requirements/49-early-signal-network-pulse-l1-api.md \
  doge-complaints-gateway/docs/requirements/50-early-signal-emerging-l2-api.md \
  spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md \
  spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```

**G14 PASS iff:**

- операционные runtime-docs / REQ 49/50/51 / spa-15/16 **не** учат `/tallinn/…` как текущий контракт (N/A в gate только если файл без публичного URL);  
- T-wave runbook G3 строка **на месте** (исторический);  
- `docs/analysis/audit-gw-ssr-0*` не в diff этой стори;  
- `CLUSTER_GEO_SCOPE` примеры с городом живы.

---

### 6.7 SSR-15 → G15 → стоп волны

**Сделать:** T01…T06 / T-dual. Pytest paths `/node/…`; сценарии civic / pack / Pulse≠issues / 404 `/tallinn/issues`. Rename `test_req24_tallinn_issues_read_api.py` предпочтителен. Dual: если 10 Done — тест; иначе skip с пометкой в gate.

**G15 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration"   # полный offline — обязателен на G15
rg -n '@app.get\("/tallinn' tests --glob '*.py'
rg -n 'client\.(get|post)\("/tallinn' tests --glob '*.py'
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter" src/core/api/asgi_app.py
```

**G15 PASS iff:**

- полный offline pytest зелёный;  
- публичные URL в pytest = `/node/…`; единственные `/tallinn/issues` в tests — **негатив 404** (не `@app.get("/tallinn"`);  
- сценарии стори 1–3 и 5; T-dual по правилу стори;  
- `ClusterLens` baseline; нет filter HTTP;  
- не `live_integration` как proof.

**После G15 PASS:** волна post-T-wave **закрыта**. Не стартовать SSR-06/07/12. Dashboard: Todo 08–15 Done; pie T-wave не трогать. INDEX Status. Оператору — **итоговый** summary (очередь исчерпана). Это не запрос «можно ли 06».

---

## 7. Диаграмма

```text
Шаг 0 / G0  ветка semantic-schema-runtime
  → SSR-08 → G8          ← civic-as-pack data
  → SSR-09 → G9          ← hosted/image; не live proof
  → SSR-10 → G10         ← dual opt-in
  → SSR-13 → G13         ← /node/* + SPA paths; до 11
  → SSR-11 → G11         ← named card fields
  → SSR-14 → G14         ← docs inventory
  → SSR-15 → G15
  → STOP (не 06/07/12)
```

---

## 8. HALT немедленно (запрещённый паттерн)

Даже при зелёном pytest:

| Паттерн | Как увидеть |
|---------|-------------|
| Новый `ClusterLens` member | diff `src/core/cluster/types.py` |
| Pack story через civic `_create_issue_for_cluster` без dual-флага / civic default False | diff orchestrator + `require_actionable` default |
| Binding в `required_columns_ready` | diff `db_supabase.py` |
| Новая таблица в `REQUIRED_READINESS_TABLES` | тот же файл |
| Файлы `doge-identity-service/` | `git diff --name-only` |
| Правка `gateway-mvp-dashboard.md` / bullrun «Актуальная точка» | git status |
| Код `story_dimensions` / processor delivery / SSR-12 matching | glob + story 12 files |
| Новый HTTP path filter / IDX | `asgi_app.py` |
| Alias `/tallinn/*` после SSR-13 | `src/core/api` |
| Overlay UI / form builder spa (не URL репозиториев) | `spa-app/src` кроме трёх Gateway*Repository |
| Перепись T-wave G3 / closed P4 audits | `orchestrator-t-wave-runbook.md`, `docs/analysis/audit-gw-ssr-0*` |
| Исполнение не на `semantic-schema-runtime` | Шаг 0 / G0 |
| Параллельный pkg 08 и 09 | два active P1.3 |

---

## 9. P8 / git

- Push **нет**, пока оператор явно не сказал.  
- P8 local — по session overnight (feat → test → docs). Не коммитить `.env` / secrets.  
- `docs/tasks/**` MVP/bullrun — не коммитить «заодно», если не часть SSR dashboard/INDEX/story.

SPA path-rename (D-SSR-7) живёт в nested `spa-app/` git: коммит там **только** по явной команде оператора; OP не invent второй remote.

---

## 10. Что записать в wave MD на каждом G*

```text
GATE: G<n> story=GW-SSR-<nn>
branch: semantic-schema-runtime
wave: post-t-wave
pytest: <command> exit=<code>
rg ClusterLens: baseline match yes/no
forbidden_pattern: none | <path>
decision: PASS continue | FAIL halt-for-P6 | HALT operator
```

Даты артефактов: `--print-utc-now` (не выдумывать).

---

## 11. После исчерпания очереди

Сообщить оператору: post-T-wave SSR-08, 09, 10, 13, 11, 14, 15 Done по G15; SSR-06/07/12 не запускались; ветка `semantic-schema-runtime`; канон публичного API `/node/*`; merge/push/PA.2 REQ-51 — **ждут команды**. Не предлагать «заодно index».
