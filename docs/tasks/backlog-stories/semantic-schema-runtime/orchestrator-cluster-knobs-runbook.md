# Orchestrator runbook — Semantic Schema Runtime cluster-knobs (SSR-19…21)

**Для кого:** агент-оркестратор (роль OP). Не пишет product-код. Не invent AC.  
**Пакет:** [`INDEX.md`](./INDEX.md)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Универсальный overnight:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**Этот файл — overlay очереди и continue-gate волны «CLUSTER_* → pack».** Где конфликт: **побеждает этот файл** (не пропускать следующую стори при FAIL gate; не включать SSR-06/07/12).  
**T-wave:** [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) — **исторический** (01–05 Done). Не стартовать заново. Не переписывать G3.  
**Post-T-wave:** [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — **исторический** (08–15 Done).  
**Node-schema:** [`orchestrator-node-schema-runbook.md`](./orchestrator-node-schema-runbook.md) — **исторический** (16–18 Done). Не стартовать заново.  
**Process:** [`OP-gateway.process.md`](../../run-reports/operator-sessions/OP-gateway.process.md)  
**Fences P1–P8:** дословно из [`workflow.md`](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) / workflow-console — не перефразировать. Этот runbook не заменяет fence.

> **Updated:** 2026-08-30T18:33:11Z (`--print-utc-now`)

**Имя ветки = имя пакета:** `semantic-schema-runtime`

---

## Шаг 0 — ветка пакета (до всего)

Это **первый** шаг OP. До него: не P1.3, не P2, не spawn BLD, не менять `gateway-active-package.current.yaml`. Оператору не писать, если команды ниже прошли.

Ветка **уже существует**. Цель: **switch** на канон, не плодить вторую ветку.

**Product git:** workspace `DOGEstonia` **может не быть** git-корнем. Канон ветки SSR — nested [`doge-complaints-gateway/`](../../../../). Не `git switch` внутри nested `spa-app/`.

### 0.1 Корень и toplevel

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test -f docs/tasks/backlog-stories/semantic-schema-runtime/INDEX.md
git rev-parse --abbrev-ref HEAD
```

| Факт | Действие |
|------|----------|
| cwd оканчивается на `/spa-app` | HALT. Выйти, повторить из gateway. |
| Нет INDEX.md пакета | HALT. Не тот clone. |
| Уже на `semantic-schema-runtime` | Шаг 0.4 → **G0 PASS**, дальше §1. |

### 0.2 Грязное дерево

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
git status --porcelain
```

Не `stash`, не `reset --hard`. Isolation = ветка `semantic-schema-runtime`; MVP dirt **не** коммитить в SSR P8.

### 0.3 Создать или перейти

Имя **ровно:** `semantic-schema-runtime`.

```bash
git show-ref --verify --quiet refs/heads/semantic-schema-runtime && \
  git switch semantic-schema-runtime

git show-ref --verify --quiet refs/heads/feat/gw-semantic-schema-runtime && \
  git switch feat/gw-semantic-schema-runtime && \
  git branch -m semantic-schema-runtime

git show-ref --verify --quiet refs/heads/semantic-schema-runtime || \
  git switch -c semantic-schema-runtime
```

Не делать: `push`, `--force`, создавать ветку из `spa-app`.

### 0.4 Подтверждение (G0)

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
git status -sb
```

В wave MD: `GATE: G0 branch=semantic-schema-runtime created_or_switched=yes wave=cluster-knobs`.

---

## 0. Кто ты и чего не делаешь

| Делаешь | Не делаешь |
|---------|------------|
| Очередь **19 → 20 → 21**, ветка **`semantic-schema-runtime`**, pkg, spawn/resume BLD+VAL, continue-gate, факт в wave MD | Product code, invent AC, push, правка `ClusterLens`, identity, recount [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) |
| PASS gate → сразу следующая стори | Ждать approve на G0 / G19–G21 |
| FAIL gate → HALT (не skip) | «BLOCKED → очередь дальше» для G* FAIL |
| Запрещённый паттерн → HALT | Чинить код в роли OP |
| `node_clustering.civic` в pack (D-SSR-9) | Перенос cron в pack; env override поверх pack; GPT UI; IDX; `GET /schema-active` |

Оператор на G0 / G19–G21 **не нужен**. Нужен только: `стоп|stop|pause|halt`; gate FAIL после одного P6; запрещённый паттерн.

---

## 1. SSOT на диске

1. Этот файл.  
2. [`INDEX.md`](./INDEX.md) — D-SSR-1…**9**, §Seam validation.  
3. Стори очереди (полный markdown, **Подзадачи**).  
4. Не SSOT: чат, `bullrun-launch-index.md` §«Актуальная точка», исторические runbook как очередь.

`builder_project: gateway`. Skill BLD: `python-pro`.  
Offline: `python3 -m pytest -q -m "not live_integration"` из `doge-complaints-gateway/`.

T-wave / post-T-wave / node-schema **Done**. Pie T-wave **не** трогать. Dashboard: [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md).

---

## 2. Очередь (жёсткая)

| # | Story file | Gate | Дальше только если |
|---|------------|------|-------------------|
| 1 | [`STORY-GW-SSR-19-node-clustering-pack-contract.md`](./STORY-GW-SSR-19-node-clustering-pack-contract.md) | **G19** | G19 PASS |
| 2 | [`STORY-GW-SSR-20-node-clustering-runtime-wire.md`](./STORY-GW-SSR-20-node-clustering-runtime-wire.md) | **G20** | G20 PASS |
| 3 | [`STORY-GW-SSR-21-node-clustering-docs.md`](./STORY-GW-SSR-21-node-clustering-docs.md) | **G21** | G21 PASS → **конец волны** |

**Не в очередь:** SSR-06, SSR-07, SSR-12. Параллель **19 ∥ 20 запрещена**.

`$queueSpec`:

```text
Cluster-knobs only: STORY-GW-SSR-19 then 20 then 21.
First: switch git branch named exactly semantic-schema-runtime. See runbook Шаг 0.
Follow doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md
Do NOT queue SSR-06 SSR-07 SSR-12.
Do NOT restart T-wave / post-T-wave / node-schema.
Do NOT parallel 19 and 20.
```

---

## 3. Забор G0

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
```

Не трогать: bullrun «Актуальная точка»; `gateway-mvp-dashboard.md`; identity; GPT pack. Pie T-wave не менять.

**G0 PASS** → P1.3 стори 19.

---

## 4. Инъекция в BLD

- Не добавлять / удалять `ClusterLens` members.
- Не переносить `CLUSTER_CRON_*` в pack.
- Не invent env override поверх `node_clustering.civic`.
- Не invent HTTP / `GET /schema-active` / IDX / QRY.
- Не менять default `require_actionable_canonical_type=True` на civic factory type (только числа из pack civic block).
- Не трогать identity (D-SSR-3).
- Не реализовывать SSR-06/07/12.
- Не переписывать T-wave G3 / post-T-wave / node-schema как очередь.
- Значения example pack — из текущих EnvSpec/conftest defaults, не invent пороги.
- Два контура: `exact_lenses` ≠ `node_clustering.civic`.

VAL: read-only; те же rg/pytest, что G*.

---

## 5. Протокол continue-gate (G19–G21)

После P7: OP гонит команды ниже.

- **PASS:** запись в wave → следующая стори.  
- **FAIL:** один P6 → повтор G*; снова FAIL → HALT.  
- Запрещённый паттерн → HALT сразу.

Полный offline pytest **обязателен на G20** (и желателен на G21 docs-only если suite не трогали — минимум docs rg).

---

## 6. Стори: что выполнить и что проверить

### 6.1 SSR-19 → G19

**Сделать:** T00…T05. `node_clustering.civic` в SchemaContext + resolver; три pack; README. Не factory wire.

**G19 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_19_*.py
rg -n "node_clustering" schema-packs/README.md src/core/schema/
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
test -f schema-packs/tallinn_civic/v1/pack.json
rg -n "node_clustering" schema-packs/tallinn_civic/v1/pack.json schema-packs/legal_process/v1/pack.json schema-packs/mobility_observation/v1/pack.json
```

**G19 PASS iff:** pytest 19 зелёный; три pack с блоком; README ключ; ClusterLens=10; factory ещё может читать AppConfig CLUSTER_* (wire = 20).

---

### 6.2 SSR-20 → G20

**Сделать:** T01…T06. Factory + handlers из активного pack; убрать семантические CLUSTER_* из AppConfig; cron stay; suite/fixtures.

**G20 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_20_*.py
python3 -m pytest -q -m "not live_integration" tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration"
rg -n "cluster_min_size|CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES" src/core/config/schema.py
rg -n "CLUSTER_CRON_ENABLED|CLUSTER_CRON_INTERVAL_S" src/core/config/schema.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
rg -n "story_dimensions|/schema-filter|schema-active" src/core/api/asgi_app.py
```

**G20 PASS iff:**

- civic engine / gate / min_size из pack активного NODE_SCHEMA;  
- семантические CLUSTER_* **не** required в AppConfig (нет полей / нет EnvSpec);  
- `CLUSTER_CRON_*` на месте;  
- missing `node_clustering` на активном pack → ConfigError;  
- полный offline pytest зелёный; ClusterLens=10; нет filter HTTP.

---

### 6.3 SSR-21 → G21 → стоп волны

**Сделать:** T01…T04. Мануал двух контуров; 05-env + server-env; README/matrix сверка.

**G21 команды:**

```bash
cd /Users/eslinko/Development/DOGEstonia
rg -n "node_clustering|exact_lenses" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "CLUSTER_MIN_SIZE|CLUSTER_ACTIVE_LENSES|CLUSTER_PRIMARY_LENS|CLUSTER_GEO_SCOPE" \
  doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "CLUSTER_CRON" doge-complaints-gateway/docs/runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
```

**G21 PASS iff:**

- мануал описывает оба контура и путь «правка pack + рестарт»;  
- 05-env **не** учит семантические CLUSTER_* как текущий SSOT (пометка moved / pack); cron documented;  
- T-wave G3 строка на месте;  
- closed audits не в diff этой стори.

**После G21 PASS:** волна cluster-knobs **закрыта**. Следующая overnight — [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) (**22 → 25**). Не стартовать 06/07/12. Dashboard Todo 19–21 Done. Оператору — итоговый summary + указание на geo-detail.

---

## 7. Диаграмма

```text
Шаг 0 / G0  ветка semantic-schema-runtime
  → SSR-19 → G19         ← pack contract + loader + data
  → SSR-20 → G20         ← factory/handlers; AppConfig cleanup
  → SSR-21 → G21         ← docs two contours + env inventory
  → STOP (не 06/07/12)
```

---

## 8. HALT немедленно

| Паттерн | Как увидеть |
|---------|-------------|
| Новый/удалённый `ClusterLens` | diff `types.py` |
| Cron knobs в pack.json | pack / resolver |
| Env override поверх pack для семантики | factory dual-read |
| Binding в `required_columns_ready` | `db_supabase.py` |
| `doge-identity-service/` | git diff names |
| MVP dashboard / bullrun «Актуальная точка» | git status |
| SSR-06/07/12 code | glob |
| `GET /schema-active` / filter HTTP | `asgi_app.py` |
| Перепись T-wave G3 / historical runbooks as queue | those files |
| Не на `semantic-schema-runtime` | G0 |
| Параллельный pkg 19 и 20 | два active P1.3 |

---

## 9. P8 / git

- Push **нет**, пока оператор явно не сказал.  
- P8 local; не коммитить `.env` / secrets.  
- `docs/tasks/**` MVP/bullrun — не «заодно».

---

## 10. Запись в wave MD

```text
GATE: G<n> story=GW-SSR-<nn>
branch: semantic-schema-runtime
wave: cluster-knobs
pytest: <command> exit=<code>
rg ClusterLens: baseline match yes/no
forbidden_pattern: none | <path>
decision: PASS continue | FAIL halt-for-P6 | HALT operator
```

Даты: `--print-utc-now`.

---

## 11. После исчерпания очереди

Сообщить оператору: cluster-knobs SSR-19, 20, 21 Done по G21; SSR-06/07/12 не запускались; ветка `semantic-schema-runtime`; civic knobs = `node_clustering.civic` активного pack; cron = env; следующая волна — [geo-detail](./orchestrator-geo-detail-runbook.md) SSR-22…25; merge/push/PA.2 REQ-51 — **ждут команды**. Не предлагать «заодно index».
