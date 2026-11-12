# Orchestrator runbook — Semantic Schema Runtime T-wave

**Для кого:** агент-оркестратор (роль OP). Не пишет product-код. Не invent AC.  
**Пакет:** [`INDEX.md`](./INDEX.md)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Универсальный overnight:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**Этот файл — overlay очереди и continue-gate.** Где конфликт: **побеждает этот файл** (не пропускать следующую стори при FAIL gate; не включать SSR-06/07).  
**Fences P1–P8:** дословно из [`workflow.md`](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) / workflow-console — не перефразировать. Этот runbook не заменяет fence.

> **Updated:** 2026-08-28T12:21:21Z (`--print-utc-now`)

**Имя ветки = имя пакета:** `semantic-schema-runtime`  
(папка [`backlog-stories/semantic-schema-runtime/`](./INDEX.md); не `feat/gw-…`, не MVP-ветка).

---

## Шаг 0 — создать ветку пакета и переключиться (до всего)

Это **первый** шаг OP. До него: не P1.3, не P2, не spawn BLD, не менять `gateway-active-package.current.yaml`. Оператору не писать, если команды ниже прошли.

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

Непусто и это не файлы **этого** пакета (runbook/INDEX/stories SSR) → **HALT**. Не `stash`, не `reset --hard`, не мешать MVP ES-04 с этой волной.

### 0.3 Создать или перейти

Имя **ровно:** `semantic-schema-runtime`. Блоки ниже — **сверху вниз**; после первого успеха сразу **0.4** (не гонять все три вслепую, если уже на каноне).

```bash
# Уже есть канон
git show-ref --verify --quiet refs/heads/semantic-schema-runtime && \
  git switch semantic-schema-runtime

# Наследие D-SSR-2 (старое имя) — переименовать, не плодить вторую ветку
git show-ref --verify --quiet refs/heads/feat/gw-semantic-schema-runtime && \
  git switch feat/gw-semantic-schema-runtime && \
  git branch -m semantic-schema-runtime

# Нет ни той ни другой — создать от текущего tip (обычно main/master рабочей линии)
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

В wave MD: `GATE: G0 branch=semantic-schema-runtime created_or_switched=yes`.

**Только после этого** — §1 SSOT и очередь.

---

## 0. Кто ты и чего не делаешь

| Делаешь | Не делаешь |
|---------|------------|
| Очередь SSR-01→05, ветка **`semantic-schema-runtime`**, pkg на ней, spawn/resume BLD+VAL, прогон **continue-gate**, запись факта в wave MD | Product code, invent AC, push, правка `ClusterLens`, правка identity-service, recount [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) |
| При PASS gate — **сразу** следующая стори, **без** вопроса оператору | Ждать approve на запланированных G0–G5 |
| При FAIL gate — HALT очереди (не skip на 05) | «BLOCKED → очередь дальше» из universal overnight **для этой волны** |
| При обнаружении запрещённого паттерна (ниже) — HALT | Чинить код в роли OP |

Оператор на G0–G5 **не нужен**. Оператор нужен только: явный `стоп|stop|pause|halt`; gate FAIL после одного цикла P6 на той же стори; запрещённый паттерн в diff.

---

## 1. SSOT на диске (прочитать до очереди)

1. Этот файл.  
2. [`INDEX.md`](./INDEX.md) — D-SSR-1…6, §Seam validation, git branch.  
3. Стори очереди (полный markdown, таблица **Подзадачи** = порядок T00…Tn).  
4. Не SSOT: чат, память, `bullrun-launch-index.md` §«Актуальная точка» (там MVP ES-04 / pkg-000060 — **не** переписывать этой волной).

`builder_project: gateway`. Execution skill BLD: `python-pro`.  
`test_command` профиля: `cd doge-complaints-gateway && python3 -m pytest -q` ([`profiles.yaml`](../../../../../docs/methodology/Zeya888-builder-queue/specs/profiles.yaml) gateway).

Live hosted / `live_integration` **не** являются proof T-wave. Канон offline: `python3 -m pytest -q -m "not live_integration"` из `doge-complaints-gateway/`.

---

## 2. Очередь (жёсткая)

**В очередь:** только T-wave 1–5, **по одной стори = один P1.3 pkg** (`input_mode: backlog_story`). Не один pkg на пять стори.

| # | Story file | После неё gate | Дальше только если |
|---|------------|----------------|-------------------|
| 1 | [`STORY-GW-SSR-01-schema-runtime-pack-load.md`](./STORY-GW-SSR-01-schema-runtime-pack-load.md) | **G1** | G1 PASS |
| 2 | [`STORY-GW-SSR-02-structured-payload-persist.md`](./STORY-GW-SSR-02-structured-payload-persist.md) | **G2** | G2 PASS |
| 3 | [`STORY-GW-SSR-03-optional-v2-semantic-wire.md`](./STORY-GW-SSR-03-optional-v2-semantic-wire.md) | **G3** | G3 PASS |
| 4 | [`STORY-GW-SSR-04-schema-driven-cluster-lens.md`](./STORY-GW-SSR-04-schema-driven-cluster-lens.md) | **G4** | G4 PASS |
| 5 | [`STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md`](./STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md) | **G5** | G5 PASS → **конец волны** |

**Не в очередь:** [`STORY-GW-SSR-06-…`](./STORY-GW-SSR-06-analytical-index-later.md), [`STORY-GW-SSR-07-…`](./STORY-GW-SSR-07-processor-delivery-later.md) (D-SSR-6). Если BLD открыл их в diff — HALT.

Параллель 03 ∥ 04 **запрещена этой волне** (диагностика). Порядок только 03 затем 04. INDEX «могут идти параллельно» = зависимость графа, не overnight.

Внутри стори: субтаски **по ID** (T00→T01→…). Не пропускать T00. Gate-таск стори (T07/T08) = story acceptance; continue-gate G* этого runbook — **дополнительно** после P7/VAL той стори.

`$queueSpec` для OP-старта (пример):

```text
T-wave only: STORY-GW-SSR-01 then 02 then 03 then 04 then 05.
First: create/switch git branch named exactly semantic-schema-runtime (package folder). See runbook Шаг 0.
Follow doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
Do NOT queue SSR-06 SSR-07.
```

---

## 3. Забор G0 — повторная проверка ветки

Создание/switch — **Шаг 0** в начале файла. Здесь только verify перед P1.3 стори 01 (и перед каждой следующей стори, если OP подозревает смену ветки):

```bash
cd /Users/eslinko/Development/DOGEstonia
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
```

| Ожидание | Если нет |
|----------|----------|
| `HEAD` = **`semantic-schema-runtime`** | Вернуться к **Шагу 0**. Не исполнять P1.3/P3. |
| Working tree не смешивает MVP ES-04 product-fixes с SSR без явной команды | HALT и факт в wave |

На **этой** ветке P1.3 **может** переписать [`gateway-active-package.current.yaml`](../../gateway-active-package.current.yaml) на SSR `pkg-*.yaml` — иначе `--verify` останется на pkg-000060. На ветке MVP current.yaml на SSR **не** переключать.

Не трогать: `bullrun-launch-index.md` «Актуальная точка»; `gateway-mvp-dashboard.md`; `doge-identity-service/**`; sibling GPT/SPA REQ files.

Dashboard волны: только [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md) (recount Status с диска после Done стори).

**G0 PASS** → можно P1.3 стори 01. Оператору не писать.

---

## 4. Инъекция в BLD (каждая стори)

В prompt Builder, кроме fence и story file, **дословно** запреты INDEX:

- Не добавлять член в `ClusterLens` ([`types.py`](../../../../src/core/cluster/types.py) `:10–22`).
- Не править `lens_dimension` под pack ([`engine.py`](../../../../src/core/cluster/engine.py) `:66–79`).
- Не менять default `PromotionGatePolicy.require_actionable_canonical_type=True` ([`gates.py`](../../../../src/core/promotion/gates.py) `:11–14`) и civic factory ([`service_factory.py`](../../../../src/core/infrastructure/service_factory.py) `:106–109`).
- Не класть binding-колонки в `required_columns_ready` ([`db_supabase.py`](../../../../src/core/infrastructure/db_supabase.py) `:336`).
- Не добавлять таблицы в `REQUIRED_READINESS_TABLES` ([`:29–43`](../../../../src/core/infrastructure/db_supabase.py)).
- Не invent HTTP filter / новый intake path.
- Не трогать `doge-identity-service`; `enforce_policy` без identity claims (D-SSR-3).
- Не реализовывать SSR-06/07 (`story_dimensions`, processor pipeline).
- `build_index` / `project` — stub/no-op, не «working IDX/PROC».
- Semantic persist field = `bound_schema_version`, не вторая колонка `schema_version`.
- Pack cluster_id namespace `schema:…`; не `stable_cluster_id(ClusterLens, …)`.
- Civic `_persist_memberships` / `_create_issue_for_cluster` as-is не использовать для pack.

VAL: read-only; те же rg/pytest, что в G* ниже; findings only.

---

## 5. Протокол continue-gate (G1–G5)

После P7 стори (VAL audit + story gate PASS) OP **сам** гонит команды ниже из корня `doge-complaints-gateway/` (или workspace root с `-c`).

- **PASS:** все команды exit 0 + rg-инварианты. Записать 3–6 строк в wave MD. Сразу следующая стори. Оператору не писать.  
- **FAIL:** не стартовать следующую стори. Один цикл P6 (BLD fix по VAL/gate) → повтор G*. Если снова FAIL → HALT волны, отчёт оператору (это единственная незапланированная остановка).  
- **Запрещённый паттерн в diff** (см. §8) → HALT сразу, даже если pytest зелёный.

Полный `pytest -q` профиля после G2 и G4 **желателен**; если слишком долго — минимум = бандлы ниже + полный прогон обязателен на G5.

---

## 6. Стори: что выполнить и что проверить

### 6.1 SSR-01 → G1

**Сделать:** T00…T07 по стори. Код в `src/core/schema/`. Pack data в `schema-packs/<schema_id>/<schema_version>/`. `jsonschema` в `pyproject.toml` + `requirements.txt`. Example pack несёт readiness-ключи под 3 knobs `PromotionGatePolicy` (числа **в файле пака**). Intake/clustering **не** трогать.

**G1 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_01_*.py
python3 -c "import jsonschema"
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```

**G1 PASS iff:**

- pytest SSR-01 зелёный;  
- `jsonschema` импортируется;  
- `ClusterLens` members **ровно** (baseline): `composite_primary_micro`, `civic_domain_micro`, `failure_pattern_micro`, `civic_weight_systemic`, `desired_outcome_local`, `affected_group_local`, `geographic_district_micro`, `service_object_micro`, `deep_need_local`, `ecosystem_signal_systemic`;  
- есть example pack + `schema-packs/README.md` с таблицей loader keys;  
- `src/core/intake/contracts.py` **без** `schema_binding` (это SSR-03);  
- нет вызова runtime из intake `services.py`.

**Зачем пауза:** 04/05 привяжутся к loader keys. Оператор не утверждает YAML — OP только проверяет, что таблица ключей **есть** и readiness мапится на 3 knobs, не на civic `70`/`2` в Python default пака.

---

### 6.2 SSR-02 → G2 (критический)

**Сделать:** T00…T08. Поля на `StoryRecord`; sqlite ALTER + SELECT + INSERT **и** `ON CONFLICT DO UPDATE SET`; supabase row + `_STORY_SELECT_FIELDS` + `000_full_init.sql` + migration; `advance_story_readiness` копирует новые поля (`replace` предпочтителен). Не `required_columns_ready`. Не `REQUIRED_READINESS_TABLES`.

**G2 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_02_*.py tests/test_stories_schema_cross_layer_invariant.py tests/test_story_intake_contract.py tests/test_story_intake_field_persistence.py
rg -n "bound_schema_version|structured_payload|payload_hash" src/core/application/services.py
rg -n "required_columns_ready" -A 30 src/core/infrastructure/db_supabase.py
```

**G2 PASS iff:**

- pytest бандл зелёный;  
- в `advance_story_readiness` / `replace` видны `schema_id`, `bound_schema_version`, `structured_payload`, `payload_hash` (и profile поля);  
- `required_columns_ready` **не** содержит binding-колонок;  
- civic save без binding (все None) покрыт тестом стори;  
- lifecycle advance **сохраняет** binding (тест стори).

**Зачем:** silent wipe. Если G2 пропустить, SSR-03 «пишет» binding, READY_FOR_PROFILE обнуляет, 04 кластеризует пустой `schema_id`.

---

### 6.3 SSR-03 → G3

**Сделать:** T01…T08. Optional `schema_binding` в `_parse_story_envelope_body`; поля на `StoryIntakeRequest` **и** `StoryDraftStashRequest`; validate до `save_story`; persist map INDEX; OpenAPI существующих path ([`openapi.yaml`](../../../../docs/runtime-docs/api-reference/openapi.yaml)) — не новый route.

**G3 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_03_*.py tests/test_story_intake_contract.py tests/test_gpt_signals_intake.py
rg -n "schema_binding" src/core/intake/contracts.py src/core/application/services.py
rg -n "def (GET|POST|PUT|PATCH|DELETE)|add_route|/tallinn/" src/core/api/asgi_app.py
```

**G3 PASS iff:**

- civic intake без ключа зелёный; invalid payload → 4xx, не silent drop;  
- stash и submit делят parse binding;  
- `asgi_app.py` **без** нового filter/schema-metadata path (сверить: не появилось имён вроде `dimensions`, `schema-filter`, `story_dimensions` в routes);  
- `GET /tallinn/issues` на месте (`asgi_app.py` ~462).

---

### 6.4 SSR-04 → G4 (обязателен до SSR-05)

**Сделать:** T01…T06. Pack engine; ветка в `process_story` / `process_all_pending`; **не** второй cron; membership **до** Issue; не `CLUSTERED` в этой стори; не civic `_persist_memberships`.

**G4 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_04_*.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py \
  tests/test_story_cluster_orchestrator.py \
  tests/test_cluster_cron_job.py \
  tests/test_e2e_story_cluster_issue_pipeline.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "POLICE_STATION|police_station" src/core/cluster/types.py src/core/cluster/engine.py
```

**G4 PASS iff:**

- civic clustering/orchestrator/cron/e2e зелёные (AC-008);  
- `ClusterLens` baseline как в G1; нет `POLICE_STATION` / pack lens в enum;  
- тест: schema-bound не в civic buckets; два payload с одним exact path → один `cluster_id`;  
- `cluster_cron.py` по-прежнему зовёт `process_all_pending` (не второй job).

**Зачем до 05:** красный AC-008 после совместного 04+05 неотличим от смены factory policy.

---

### 6.5 SSR-05 → G5 → стоп волны

**Сделать:** T01…T07. Mapper pack → `PromotionGatePolicy` **на вызов**; optional `gate_policy` на `IssueCreateCommand`; `submit_for_review` override; `CLUSTERED` только после успешного pack promote; не менять factory default; не добавлять `structured_payload` в `DOGEIssue.to_public_dict`.

**G5 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" \
  tests/test_gw_ssr_05_*.py \
  tests/test_promotion_canonical_type_gate.py \
  tests/test_issue_promotion_service.py \
  tests/test_clustering_engine.py \
  tests/test_gw_tax_02_cluster_axis_expansion.py
python3 -m pytest -q -m "not live_integration"   # полный offline — обязателен на G5
rg -n "require_actionable_canonical_type: bool = True" src/core/promotion/gates.py
rg -n "structured_payload" src/core/projection/dto.py
rg -n "story_dimensions|/schema-filter|generic.filter" src/core/api/asgi_app.py
```

**G5 PASS iff:**

- pack promote без civic `complaint`/`system_bug` (тест стори); civic promotion тесты зелёные;  
- default knob `require_actionable_canonical_type: bool = True` **на месте**;  
- `dto.py` без `structured_payload`;  
- нет filter HTTP;  
- полный offline pytest зелёный.

**После G5 PASS:** волна T-wave **закрыта**. Не стартовать SSR-06/07. Dashboard: active 5/5. INDEX Status. Оператору — **итоговый** summary (очередь исчерпана). Это не запрос «можно ли 06».

---

## 7. Диаграмма

```text
Шаг 0 / G0  ветка semantic-schema-runtime
  → SSR-01 → G1
  → SSR-02 → G2          ← критический persist/lifecycle
  → SSR-03 → G3
  → SSR-04 → G4          ← civic clustering; не мешать с 05
  → SSR-05 → G5
  → STOP (не 06/07)
```

---

## 8. HALT немедленно (запрещённый паттерн)

Даже при зелёном pytest:

| Паттерн | Как увидеть |
|---------|-------------|
| Новый `ClusterLens` member | diff `src/core/cluster/types.py` |
| Pack story через civic `lens_dimension` / `_create_issue_for_cluster` без override | diff orchestrator + `require_actionable` default False |
| Binding в `required_columns_ready` | diff `db_supabase.py` |
| Новая таблица в `REQUIRED_READINESS_TABLES` | тот же файл |
| Файлы `doge-identity-service/` | `git diff --name-only` |
| Правка `gateway-mvp-dashboard.md` / bullrun «Актуальная точка» | git status |
| Код `story_dimensions` / processor delivery / WASM | glob `src/core/schema/` |
| Новый HTTP path filter | `asgi_app.py` |
| Исполнение не на `semantic-schema-runtime` | Шаг 0 / G0 |

---

## 9. P8 / git

- Push **нет**, пока оператор явно не сказал.  
- P8 local — по session overnight (feat → test → docs). Не коммитить `.env` / secrets.  
- `docs/tasks/**` MVP/bullrun — не коммитить «заодно», если не часть SSR dashboard/INDEX/story.

---

## 10. Что записать в wave MD на каждом G*

```text
GATE: G<n> story=GW-SSR-0<n>
branch: semantic-schema-runtime
pytest: <command> exit=<code>
rg ClusterLens: baseline match yes/no
forbidden_pattern: none | <path>
decision: PASS continue | FAIL halt-for-P6 | HALT operator
```

Даты артефактов: `--print-utc-now` (не выдумывать).

---

## 11. После исчерпания очереди

Сообщить оператору: T-wave SSR-01…05 Done по G5; SSR-06/07 не запускались; ветка `semantic-schema-runtime`; current.yaml на этой ветке указывает на последний SSR pkg (если P1.3 так сделал); merge/push/PA.2 REQ-51 — **ждут команды**. Не предлагать «заодно index».
