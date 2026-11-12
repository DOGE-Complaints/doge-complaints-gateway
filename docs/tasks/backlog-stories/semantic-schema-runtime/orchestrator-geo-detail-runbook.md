# Orchestrator runbook — Semantic Schema Runtime geo-detail (SSR-22…25)

**Для кого:** агент-оркестратор (роль OP). Не пишет product-код. Не invent AC.  
**Пакет:** [`INDEX.md`](./INDEX.md)  
**Метод claims:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)  
**Универсальный overnight:** [`orchestrator-builder-reference.md`](../../../../../docs/methodology/Zeya888-builder-queue/guides/orchestrator-builder-reference.md)  
**Этот файл — overlay очереди и continue-gate волны «geo gaps + geo_detail».** Где конфликт: **побеждает этот файл** (не пропускать следующую стори при FAIL gate; не включать SSR-06/07/12).  
**T-wave:** [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) — **исторический** (01–05 Done). Не стартовать заново. Не переписывать G3.  
**Post-T-wave:** [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — **исторический** (08–15 Done).  
**Node-schema:** [`orchestrator-node-schema-runbook.md`](./orchestrator-node-schema-runbook.md) — **исторический** (16–18 Done).  
**Cluster-knobs:** [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md) — очередь **19 → 20 → 21**; **G21 PASS обязателен** до старта этой волны. Не переписывать cluster-knobs как geo-очередь.  
**Process:** [`OP-gateway.process.md`](../../run-reports/operator-sessions/OP-gateway.process.md)  
**Fences P1–P8:** дословно из [`workflow.md`](../../../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) / workflow-console — не перефразировать. Этот runbook не заменяет fence.

> **Updated:** 2026-08-30T18:55:28Z (`--print-utc-now`)

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

### 0.4 Подтверждение (G0) + precondition G21

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
git status -sb
```

**Precondition:** cluster-knobs **G21 PASS** (SSR-19…21 Done). Если 19–21 ещё Todo — **не** стартовать эту волну; вернуться в [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md).

В wave MD: `GATE: G0 branch=semantic-schema-runtime created_or_switched=yes wave=geo-detail precondition=G21`.

---

## 0. Кто ты и чего не делаешь

| Делаешь | Не делаешь |
|---------|------------|
| Очередь **22 → 23 → 24 → 25**, ветка **`semantic-schema-runtime`**, pkg, spawn/resume BLD+VAL, continue-gate, факт в wave MD | Product code, invent AC, push, правка `ClusterLens`, identity, recount [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) |
| PASS gate → сразу следующая стори | Ждать approve на G0 / G22–G25 |
| FAIL gate → HALT (не skip) | «BLOCKED → очередь дальше» для G* FAIL |
| Запрещённый паттерн → HALT | Чинить код в роли OP |
| D-SSR-10: `geo_detail` + `geo_intake`; harden scope | Глобальный «без geo → 4xx»; invent HTTP filter; GPT UI; IDX; `GET /schema-active` |

Оператор на G0 / G22–G25 **не нужен**. Нужен только: `стоп|stop|pause|halt`; gate FAIL после одного P6; запрещённый паттерн.

---

## 1. SSOT на диске

1. Этот файл.  
2. [`INDEX.md`](./INDEX.md) — D-SSR-1…**10**, §Seam validation (civic geo gate).  
3. Стори очереди (полный markdown, **Подзадачи**).  
4. Не SSOT: чат, `bullrun-launch-index.md` §«Актуальная точка», исторические runbook как очередь.

`builder_project: gateway`. Skill BLD: `python-pro`.  
Offline: `python3 -m pytest -q -m "not live_integration"` из `doge-complaints-gateway/`.

T-wave / post-T-wave / node-schema **Done**. Cluster-knobs **Done (G21)** перед стартом. Pie T-wave **не** трогать. Dashboard: [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md).

---

## 2. Очередь (жёсткая)

| # | Story file | Gate | Дальше только если |
|---|------------|------|-------------------|
| 1 | [`STORY-GW-SSR-22-civic-geo-gate-hardening.md`](./STORY-GW-SSR-22-civic-geo-gate-hardening.md) | **G22** | G22 PASS |
| 2 | [`STORY-GW-SSR-23-geo-detail-intake-contract.md`](./STORY-GW-SSR-23-geo-detail-intake-contract.md) | **G23** | G23 PASS |
| 3 | [`STORY-GW-SSR-24-geo-detail-persist.md`](./STORY-GW-SSR-24-geo-detail-persist.md) | **G24** | G24 PASS |
| 4 | [`STORY-GW-SSR-25-geo-detail-clustering-docs.md`](./STORY-GW-SSR-25-geo-detail-clustering-docs.md) | **G25** | G25 PASS → **конец волны** |

**Не в очередь:** SSR-06, SSR-07, SSR-12. Параллель **22 ∥ 23 запрещена**. Не 19–21 (уже закрыты или ещё в cluster-knobs).

`$queueSpec`:

```text
Geo-detail only: STORY-GW-SSR-22 then 23 then 24 then 25.
Precondition: cluster-knobs G21 PASS.
First: switch git branch named exactly semantic-schema-runtime. See runbook Шаг 0.
Follow doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md
Do NOT queue SSR-06 SSR-07 SSR-12.
Do NOT restart T-wave / post-T-wave / node-schema / cluster-knobs.
Do NOT parallel 22 and 23.
```

---

## 3. Забор G0

```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
test "$(git rev-parse --abbrev-ref HEAD)" = "semantic-schema-runtime"
```

Не трогать: bullrun «Актуальная точка»; `gateway-mvp-dashboard.md`; identity; GPT pack. Pie T-wave не менять.

**G0 PASS** + G21 Done → P1.3 стори 22.

---

## 4. Инъекция в BLD

- Не добавлять / удалять `ClusterLens` members.
- Не invent HTTP geo-filter / `GET /schema-active` / IDX / QRY.
- Не глобальный require-geo без pack `geo_intake`.
- Не silent skip при `geo_service is None` когда scope/required активны (цель 22 — убрать).
- Не класть новые geo cols в `required_columns_ready`.
- Не dump raw `geo_detail` в public Issue card.
- Не трогать identity (D-SSR-3).
- Не реализовывать SSR-06/07/12.
- Не переписывать T-wave G3 / historical runbooks as queue.
- Два контура cluster: civic snapshot ≠ pack exact `geo.*` lenses.

VAL: read-only; те же rg/pytest, что G*.

---

## 5. Протокол continue-gate (G22–G25)

После P7: OP гонит команды ниже.

- **PASS:** запись в wave → следующая стори.  
- **FAIL:** один P6 → повтор G*; снова FAIL → HALT.  
- Запрещённый паттерн → HALT сразу.

Полный offline pytest **обязателен на G24** (persist) и **G25** (cluster). На G22/G23 — story tests + релевантные req35 / intake.

---

## 6. Стори: что выполнить и что проверить

### 6.1 SSR-22 → G22

**Сделать:** T00…T04. Убрать silent skip scope; fail при no service / require path. Не полный `geo_detail`.

**G22 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_22_*.py
python3 -m pytest -q -m "not live_integration" tests/test_req35_geo_scope_and_filter.py
rg -n "geo_service is None" src/core/api/handlers.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```

**G22 PASS iff:** scope+no service не accept; optional/no-scope path зелёный; ClusterLens=10; нет полного geo_detail wire (это 23).

---

### 6.2 SSR-23 → G23

**Сделать:** T00…T05. Parse `geo_detail`; pack `geo_intake`; merge; three packs; README.

**G23 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_23_*.py
rg -n "geo_intake|geo_detail" schema-packs/README.md src/core/
rg -n "geo_intake" schema-packs/tallinn_civic/v1/pack.json schema-packs/legal_process/v1/pack.json schema-packs/mobility_observation/v1/pack.json
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
```

**G23 PASS iff:** accept detail; invalid/require miss → 4xx; optional omit → 202; packs с `geo_intake`; ClusterLens=10.

---

### 6.3 SSR-24 → G24

**Сделать:** T01…T07. StoryGeoSnapshot depth; sqlite/supabase; migration; omit-probe; mirror; lifecycle preserve.

**G24 команды:**

```bash
cd doge-complaints-gateway
python3 -m pytest -q -m "not live_integration" tests/test_gw_ssr_24_*.py
python3 -m pytest -q -m "not live_integration" tests/test_stories_schema_cross_layer_invariant.py
python3 -m pytest -q -m "not live_integration"
rg -n "required_columns_ready" -A 20 src/core/infrastructure/db_supabase.py
rg -n "class ClusterLens" -A 14 src/core/cluster/types.py
ls supabase/migrations/*geo* 2>/dev/null || ls supabase/migrations/ | tail -5
```

**G24 PASS iff:** round-trip street/range/houses/coords; new cols не в required_columns_ready; migration на диске; полный offline pytest зелёный; ClusterLens=10.

---

### 6.4 SSR-25 → G25 → стоп волны

**Сделать:** T01…T05. Civic/pack cluster regression; мануал geo_intake; README/matrix.

**G25 команды:**

```bash
cd /Users/eslinko/Development/DOGEstonia
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_gw_ssr_25_*.py
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway/tests/test_clustering_engine.py
python3 -m pytest -q -m "not live_integration" doge-complaints-gateway
rg -n "geo_intake|geo_detail" doge-complaints-gateway/docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md
rg -n "GET /tallinn/issues stays" doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md
rg -n "class ClusterLens" -A 14 doge-complaints-gateway/src/core/cluster/types.py
```

**G25 PASS iff:**

- civic clustering зелёный; pack membership по `geo.*` где настроено;  
- мануал: modes / mirror / два пути cluster;  
- T-wave G3 строка на месте;  
- offline suite зелёный; ClusterLens=10.

**После G25 PASS:** волна geo-detail **закрыта**. Не стартовать 06/07/12. Dashboard Todo 22–25 Done. Оператору — итоговый summary.

---

## 7. Диаграмма

```text
Шаг 0 / G0  ветка semantic-schema-runtime (+ G21 Done)
  → SSR-22 → G22         ← civic geo-gate hardening
  → SSR-23 → G23         ← geo_detail wire + geo_intake
  → SSR-24 → G24         ← persist address depth
  → SSR-25 → G25         ← clustering + docs
  → STOP (не 06/07/12)
```

---

## 8. HALT немедленно

| Паттерн | Как увидеть |
|---------|-------------|
| Новый/удалённый `ClusterLens` | diff `types.py` |
| Глобальный require-geo без pack | handlers без geo_intake |
| Silent skip `geo_service is None` при scope | handlers.py |
| Binding/geo new cols в `required_columns_ready` | `db_supabase.py` |
| `doge-identity-service/` | git diff names |
| MVP dashboard / bullrun «Актуальная точка» | git status |
| SSR-06/07/12 code | glob |
| `GET /schema-active` / filter HTTP | `asgi_app.py` |
| Перепись T-wave G3 / historical runbooks as queue | those files |
| Не на `semantic-schema-runtime` | G0 |
| Старт без G21 | INDEX / wave |
| Параллельный pkg 22 и 23 | два active P1.3 |

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
wave: geo-detail
pytest: <command> exit=<code>
rg ClusterLens: baseline match yes/no
forbidden_pattern: none | <path>
decision: PASS continue | FAIL halt-for-P6 | HALT operator
```

Даты: `--print-utc-now`.

---

## 11. После исчерпания очереди

Сообщить оператору: geo-detail SSR-22, 23, 24, 25 Done по G25; SSR-06/07/12 не запускались; ветка `semantic-schema-runtime`; `geo_detail` + pack `geo_intake`; civic scope harden; persist depth; cluster civic/pack; merge/push/PA.2 REQ-51 — **ждут команды**. Не предлагать «заодно index».
