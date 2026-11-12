# Semantic Schema Runtime (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/semantic-schema-runtime/`  
**Тип:** backlog (постановки; глубина — при активации на **отдельной git-ветке**).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`51-semantic-schema-runtime.md`](../../../requirements/51-semantic-schema-runtime.md) (Accepted — package delivered; PA.2 closed 2026-09-01)  
**Parent product:** [`REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md`](../../../../../docs/requirements%20backlog/REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md)  
**Scope dashboard (не MVP):** [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md)  
**Siblings (seams only, не этот пакет):** identity [`20-…`](../../../../doge-identity-service/docs/requirements/20-semantic-schema-identity-boundary.md) · spa [`16-…`](../../../../spa-app/docs/requirements/16-semantic-schema-spa-compatibility.md) · GPT [`REQ-45-…`](../../../../GPT%20UI/docs/requirements/REQ-45-semantic-schema-intake-envelope-compatibility.md) — **synced 2026-08-31T09:40:45Z** (REQ-45 / spa-16 / identity-20 + gateway [`51`](../../../requirements/51-semantic-schema-runtime.md) seam mirror; requirements only; SSR-06/07 still Draft).  
**Эпик-дом:** нет `EPIC-M2-*` на диске — не invent.  
**Оркестратор T-wave (01–05 Done):** [`orchestrator-t-wave-runbook.md`](./orchestrator-t-wave-runbook.md) — историческая очередь; G3 «`/tallinn/issues` stays» не менять.  
**Оркестратор пост-T-wave (08–15 Done):** [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — историческая очередь; не переписывать как текущую. Overlay той волны: FAIL gate ≠ skip.  
**Оркестратор node-schema (16–18 Done):** [`orchestrator-node-schema-runbook.md`](./orchestrator-node-schema-runbook.md) — историческая очередь; не переписывать как текущую.  
**Оркестратор cluster-knobs (19–21 Done):** [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md) — историческая очередь; не переписывать. Не 06/07/12.  
**Оркестратор geo-detail (22–25 Done):** [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) — историческая очередь; не переписывать. Не 06/07/12.

> **Updated:** 2026-08-31T09:40:45Z · sibling REQ seam sync (45 / spa-16 / identity-20 / 51); package Done except SSR-06/07 Draft

---

## Git branch (обязателен до P1.3 / P3)

Этот пакет **не исполнять на ветке MVP**. Цель — не смешать Schema Runtime с закрывающимся MVP (Pulse/Emerging / TASK-ES-04).

Перед любой материализацией pipeline (P1.3 pkg, P2 window, P3/P6 code) волны geo-detail — **Шаг 0** в [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) (тот же канон ветки). Cluster-knobs overnight — [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md) до G21. Исторические runbook (T-wave / post-T-wave / node-schema) не очередь:

1. Имя ветки = имя пакета: **`semantic-schema-runtime`**.
2. Создать (`git switch -c`) или перейти (`git switch`). Не исполнять на MVP-ветке.
3. Вести стори SSR-* только там. На **этой** ветке current.yaml MAY указывать на SSR pkg; на MVP-ветке — нет.
4. Дашборд этой волны — только [`gateway-semantic-schema-runtime-dashboard.md`](../../gateway-semantic-schema-runtime-dashboard.md). Файл [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) **не** пересчитывать этими стори.

---

## Контекст одной фразой

Добавление node-specific semantic model = публикация **schema pack** + in-process `SchemaRuntime`, а не правка `StoryRecord` / intake parser / колонок `stories` / `ClusterLens` на каждое поле. T-wave (REQ3-WAVE-001 / 51 §2) закрывается без generic filter HTTP и без processor delivery.

---

## Решения оператора (2026-08-28; D-SSR-7: 2026-08-29; D-SSR-8/9/10: 2026-08-30)

| ID | Решение |
|----|---------|
| **D-SSR-1** | Optional v2 wire = **один** sidecar-объект `schema_binding` (класс изменения как `gpt_signals`). Внутри — только persist-токены parent PR-002 / DATA-002/003. Корневой `schema_version` остаётся envelope `m2.story_intake_envelope.v2`. Внутренний `schema_version` = semantic model. `envelope_version` в persist берётся с корневого envelope id. `payload_hash` **не** на проводе (считает gateway). |
| **D-SSR-2** | Исполнение на ветке **`semantic-schema-runtime`** (имя = пакет); отдельный dashboard; MVP snapshot не трогать. (Прежнее имя `feat/gw-semantic-schema-runtime` не использовать — rename, не вторая ветка.) |
| **D-SSR-3** | Identity **не трогаем** (нет claim keys, нет правок `doge-identity-service`, нет FLOW-002 policy_context в этих стори). |
| **D-SSR-4** | Runtime code: `src/core/schema/`. Pack **data**: `doge-complaints-gateway/schema-packs/<schema_id>/<schema_version>/`. Loader резолвит по `(schema_id, schema_version)`; корень паков — конфиг, чтобы позже подменить Local → Remote/sidecar без смены identity пака. |
| **D-SSR-5** | `payload_hash` (DATA-004) — **делаем** в SSR-02. |
| **D-SSR-6** | SSR-06 / SSR-07 пишем **сейчас** как **Draft (post-T-wave refine)**; всегда в **конце** порядкового процесса; не входят в T-wave close / active %. Refine **после** geo-detail 22–25. |
| **D-SSR-7** | Публичный HTTP **не** город: канон `/node/issues`, `/node/issues/{issue_id}`, `POST /node/issues`, `/node/network-pulse`, `/node/emerging-signals`. Hard cut `/tallinn/*` (нет alias). SPA path-rename репозиториев + spa-16/51 sibling — **эта волна** (не form builder, не overlay карточки). Geo `settlement:tallinn` и pack id `tallinn_civic` **не** переименовывать. |
| **D-SSR-8** | На ноде **одна рабочая** модель. Несколько каталогов в `schema-packs/` можно держать для отладки. Рабочая = пара из `.env`: **`NODE_SCHEMA_ID`**, **`NODE_SCHEMA_VERSION`** (оба required в `AppConfig`, без default, fail-fast). Новый intake **без** binding или с другим `(schema_id, schema_version)` → **4xx**. Civic engine в коде **не** удалять (dual из pack.json активного пака; уже лежащие unbound rows). Новый civic-вход закрыт. Не invent `DEFAULT_SCHEMA_PACK` и не «первый по списку». |
| **D-SSR-9** | Семантика civic-кластеризации (`min_size`, `readiness_threshold`, `active_lenses`, `primary_lens`, `signal_source`, `id_algorithm`, `geo_filter`, `geo_scope`, `tie_breaker`, `type_resolution`, `min_size_by_lens`) — в активном pack.json блок **`node_clustering.civic`**, не в `.env`. **Два контура:** `exact_lenses` = pack exact; `node_clustering.civic` = `ClusterLens` (dual + unbound). В env остаются только **`CLUSTER_CRON_ENABLED`**, **`CLUSTER_CRON_INTERVAL_S`** (+ `NODE_SCHEMA_*`, `SCHEMA_PACKS_ROOT`). Нет dual-source env+pack. Missing/битый блок на активном pack → fail-fast. |
| **D-SSR-10** | Стандартизированный intake **`geo_detail`** (sidecar рядом с narrative / root; координаты + address depth: street / house \| house_range \| houses[]) + pack **`geo_intake`** (`optional` \| `require_location_or_detail` \| `require_detail`; merge; `mirror_to_payload`). Persist в расширенный `StoryGeoSnapshot` + dual-write `structured_payload.geo` при mirror. Civic scope-gate: нет silent skip при активном scope / required geo (`geo_service is None` → fail). Кластеризация: civic из snapshot; pack — `exact_lenses` на `geo.*`. Жёсткость «без geo → 4xx» **только если pack так настроил**. Не invent HTTP filter; не расширять `ClusterLens`. |
| **D-SSR-11** | **Node-specific taxonomy axes** (2026-09-04). Contour2 `taxonomy.json` axes = pack-defined (не lockstep к 13). Contour1 wire `normalize_axis` = любая непустая ось; civic **skip** unmapped. `TAXONOMY_AXIS_VALUES` = tallinn/reference set, не reject SSOT. Arch: [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md). Stories **31→33**. Sibling GPT-SSR-15 (lock meta to 13) → supersede/invert later. |
| **D-SSR-12** | **Local warehouse + Railway Volume + federation consume** (2026-09-07). Local: корень = `doge-complaints-gateway/schema-packs/` (default; `SCHEMA_PACKS_ROOT` обычно unset); active = `NODE_SCHEMA_*`; **node packs (uus…) не в git**; demo/seed tracked. Railway: Volume mount → **`SCHEMA_PACKS_ROOT`** + те же `NODE_SCHEMA_*`. **`SCHEMA_ROOT_URL` ≠ mount path** — http(s) URL удалённого federation registry (**SSR-35 shipped** pkg-000092: boot fetch + `SCHEMA_PACK_REFRESH` stub). Stories **34** (ops) → **35** (remote consume). |

---

## Layout (зафиксировано)

```text
src/core/schema/                          # код рантайма (Protocol, LocalSchemaRuntime, resolver, validator)
doge-complaints-gateway/schema-packs/
  <schema_id>/<schema_version>/           # data-only pack (JSON Schema + SCHEMA-003 states + exact lens block)
```

Pack YAML/JSON key names parent **не** замораживает — не invent в стори сверх SCHEMA-005 / CL-001 example **shape**.

---

## Стори пакета

### T-wave (sequence 1–5) — active этого scope

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 1 | [GW-SSR-01 — SchemaRuntime + pack load](./STORY-GW-SSR-01-schema-runtime-pack-load.md) | RUNTIME + SCHEMA-005 + AC-001/004/013 | 🔵 Done (Awaiting Commits) | — |
| 2 | [GW-SSR-02 — structured_payload persist](./STORY-GW-SSR-02-structured-payload-persist.md) | DATA-001…004; AC-002/003; payload_hash | 🔵 Done (Awaiting Commits) | SSR-01 |
| 3 | [GW-SSR-03 — optional `schema_binding` on v2](./STORY-GW-SSR-03-optional-v2-semantic-wire.md) | FLOW-003; AC-015; COMPAT-001 | 🔵 Done (Awaiting Commits) | SSR-01, SSR-02 |
| 4 | [GW-SSR-04 — schema-driven exact lens](./STORY-GW-SSR-04-schema-driven-cluster-lens.md) | CL-001…005; AC-007/008 | 🔵 Done (Awaiting Commits) | SSR-02 |
| 5 | [GW-SSR-05 — pack promotion + T-wave close](./STORY-GW-SSR-05-schema-lens-promotion-t-wave-close.md) | CL-006; AC-014/018 | 🔵 Done (Awaiting Commits) | SSR-04 |

03 и 04 после 02 могут идти параллельно.

### Post-T-wave product (sequence 8–15) — Done; перед node-schema 16–18

Civic `ClusterLens` **не** удалять. Не T-wave DoD. Первый слой постановки (не P1.3). Overnight той волны **закрыт:** [`orchestrator-post-t-wave-runbook.md`](./orchestrator-post-t-wave-runbook.md) — не очередь.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 8 | [GW-SSR-08 — Tallinn civic as schema pack](./STORY-GW-SSR-08-tallinn-civic-schema-pack.md) | Civic-модель как `tallinn_civic/v1` data (путь A) | 🔵 Done (Awaiting Commits) | SSR-05 |
| 9 | [GW-SSR-09 — hosted apply + packs in image](./STORY-GW-SSR-09-hosted-apply-and-pack-image.md) | Миграция binding + паки в деплое | 🔵 Done (Awaiting Commits) | SSR-02 |
| 10 | [GW-SSR-10 — taxonomy + exact on one story](./STORY-GW-SSR-10-civic-taxonomy-and-exact-lenses.md) | Dual civic+exact; enum не расширять | 🔵 Done (Awaiting Commits) | SSR-04, SSR-05 |
| 13 | [GW-SSR-13 — abstract `/node/*` public API](./STORY-GW-SSR-13-abstract-node-public-api.md) | Hard cut `/tallinn/*`; SPA path-rename | 🔵 Done (Awaiting Commits) | SSR-05 |
| 11 | [GW-SSR-11 — pack-declared Issue projection](./STORY-GW-SSR-11-pack-declared-issue-projection.md) | Allowlist полей на `/node/issues`; не dump | 🔵 Done (Awaiting Commits) | SSR-05, **SSR-13** |
| 14 | [GW-SSR-14 — docs abstract node paradigm](./STORY-GW-SSR-14-docs-abstract-node-paradigm.md) | Инвентарь runtime-docs / REQ / spa-15/16 | 🔵 Done (Awaiting Commits) | SSR-13 |
| 15 | [GW-SSR-15 — tests `/node` + scenarios](./STORY-GW-SSR-15-tests-abstract-node-and-scenarios.md) | pytest paths + civic/pack/404 | 🔵 Done (Awaiting Commits) | SSR-13 |

Операторский мануал: [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) (перепись «склад vs рабочая env» — SSR-18).

**Не overnight той волны:** GPT emit (REQ-45). Overlay UI карточки — spa-16 later (не path).

### Node-schema (sequence 16–18) — одна активная схема ноды

**D-SSR-8.** Не T-wave DoD. Не pie T-wave. Overnight той волны **закрыт:** [`orchestrator-node-schema-runbook.md`](./orchestrator-node-schema-runbook.md) — не очередь.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 16 | [GW-SSR-16 — node active schema config](./STORY-GW-SSR-16-node-active-schema-config.md) | `NODE_SCHEMA_ID`/`VERSION` в AppConfig; boot `resolve_pack` | 🔵 Done (Awaiting Commits) | SSR-15 |
| 17 | [GW-SSR-17 — intake active schema gate](./STORY-GW-SSR-17-intake-active-schema-gate.md) | Нет/mismatch binding → 4xx; match → validate активного pack | 🔵 Done (Awaiting Commits) | SSR-16 |
| 18 | [GW-SSR-18 — cluster active schema](./STORY-GW-SSR-18-cluster-active-schema.md) | Pack-ветка только если persist == env; unbound civic; мануал | 🔵 Done (Awaiting Commits) | SSR-17 |

**Не overnight той волны:** GPT emit (REQ-45). Overlay SPA. IDX HTTP. Новая SQL-миграция. `GET /schema-active`. Удаление `ClusterLens`.

### Cluster-knobs (sequence 19–21) — CLUSTER_* → pack

**D-SSR-9.** Не T-wave DoD. Не pie T-wave. Первый слой постановки (не P1.3). Overnight: [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md). Параллель 19∥20 **запрещена**.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 19 | [GW-SSR-19 — node clustering pack contract](./STORY-GW-SSR-19-node-clustering-pack-contract.md) | `node_clustering.civic` в pack.json + loader | 🔵 Done (Awaiting Commits) | SSR-18 |
| 20 | [GW-SSR-20 — node clustering runtime wire](./STORY-GW-SSR-20-node-clustering-runtime-wire.md) | Factory/handlers из активного pack; убрать семантические CLUSTER_* из AppConfig | 🔵 Done (Awaiting Commits) | SSR-19 |
| 21 | [GW-SSR-21 — node clustering docs](./STORY-GW-SSR-21-node-clustering-docs.md) | Мануал двух контуров; 05-env / server-env | 🔵 Done (Awaiting Commits) | SSR-20 |

**Не overnight:** GPT emit. Overlay SPA. IDX HTTP. Удаление `ClusterLens`. Env override поверх pack. Перенос cron в pack.

### Geo-detail (sequence 22–25) — gaps + standardized geo_detail

**D-SSR-10.** Не T-wave DoD. Не pie T-wave. Первый слой постановки (не P1.3). Overnight: [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) **после** G21. Параллель 22∥23 **запрещена**. Зависит от cluster-knobs 19–21 (`geo_scope` в pack после 20).

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 22 | [GW-SSR-22 — civic geo-gate hardening](./STORY-GW-SSR-22-civic-geo-gate-hardening.md) | Убрать silent skip scope; fail при no service | 🔵 Done (Awaiting Commits) | SSR-20 (overnight after 21) |
| 23 | [GW-SSR-23 — geo_detail wire + geo_intake](./STORY-GW-SSR-23-geo-detail-intake-contract.md) | Wire `geo_detail` + pack policy | 🔵 Done (Awaiting Commits) | SSR-22 |
| 24 | [GW-SSR-24 — geo detail persist](./STORY-GW-SSR-24-geo-detail-persist.md) | Snapshot depth + SQL + mirror | 🔵 Done (Awaiting Commits) | SSR-23 |
| 25 | [GW-SSR-25 — geo clustering + docs](./STORY-GW-SSR-25-geo-detail-clustering-docs.md) | Civic/pack cluster + мануал | 🔵 Done (Awaiting Commits) | SSR-24 |

**Не overnight:** GPT emit. Overlay SPA map. IDX HTTP. Удаление `ClusterLens`. Invent HTTP geo-filter.

### Taxonomy-pack (sequence 26, 28–29) — copy-paste SSOT для GPT wave 2

**Цель:** on-disk `taxonomy.json` в `schema-packs/` + loader; tallinn seed; operator copy-paste seam с GPT ([GPT-SSR-05](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-05-taxonomy-json-pack-copy-paste.md)).

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 26 | [GW-SSR-26 — taxonomy.json pack contract + loader](./STORY-GW-SSR-26-taxonomy-json-pack-contract.md) | `taxonomy_schema` + loader; SchemaContext | 🔵 Done (Awaiting Commits) | SSR-25 |
| 28 | [GW-SSR-28 — tallinn_civic taxonomy.json seed](./STORY-GW-SSR-28-tallinn-civic-taxonomy-json-seed.md) | Pack data SSOT для copy-paste | Done (Awaiting Commits) | SSR-26 |
| 29 | [GW-SSR-29 — taxonomy docs + operator seam](./STORY-GW-SSR-29-taxonomy-docs-operator-copy-paste-seam.md) | Manual + GPT lockstep checklist | Done (Awaiting Commits) | SSR-26, SSR-28 |

**Siblings (GPT):** [GPT-SSR-05](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-05-taxonomy-json-pack-copy-paste.md) · [GPT-SSR-06](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-06-inbound-validation-post-ssr-delta.md) · [GPT-SSR-09](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-09-use-case-audit-core-consume-json.md) · gap [G-TAX-01](../../../../../docs/analysis/cross-project-node-model-portability-gap-2026-09-01.md).

**Не в этой волне:** runtime read `vocabulary.py` from pack; HTTP 422 label reject; mobility/legal taxonomy seed.

### Geo-precision (sequence 27) — precision index + GPT instance territory

**Цель:** pack contract `geo_model` / `gpt_instance_territory`; optional `detail_level` persist/projection; GPT lockstep ([GPT-SSR-08](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-08-geo-precision-instance-territory.md)). **Не** taxonomy. **Не** дублировать node `geo_scope` (SSR-22 Done).

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 27 | [GW-SSR-27 — geo precision + instance territory](./STORY-GW-SSR-27-geo-precision-instance-territory.md) | `detail_level` + `gpt_instance_territory` pack blocks | Done (Awaiting Commits) | SSR-25 |

**Parallel safe** с taxonomy 26/28/29 после SSR-25.

**Не в этой волне:** polygon territory; spa-16 UI; gateway mandatory instance gate (may stay GPT-only); taxonomy.json.

### SPA overlay data readiness (sequence 30) — Declare + tallinn pack

**Цель:** **Declare** `card_fields` на `tallinn_civic/v1` (MVP: `signals.desired_outcome` / `affected_group` / `service_object`), чтобы sibling spa SSR-02 имел named leaves на live Tallinn Issues. Mechanism уже [SSR-11](./STORY-GW-SSR-11-pack-declared-issue-projection.md) — **не** redesign. Gap: [G-CARD-01](../../../../../docs/analysis/cross-project-node-model-portability-gap-2026-09-01.md). Operator 2026-09-02: WAIVE cancelled.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 30 | [GW-SSR-30 — tallinn card_fields / SPA overlay readiness](./STORY-GW-SSR-30-tallinn-card-fields-spa-overlay-readiness.md) | Declare MVP allowlist in tallinn pack | Done (Awaiting Commits) pkg-000087 | SSR-11 |

**Sibling (SPA):** [STORY-SPA-SSR-api-requirements.md](../../../../spa-app/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-SPA-SSR-api-requirements.md) · SSR-02.

**Не в этой стори:** SPA overlay UI; invent HTTP; менять SSR-11 / `field_policy` shape; auto-backfill всех Issues.

### Node-taxonomy axes (sequence 31–33) — D-SSR-11

**Цель:** убрать code-lock «ровно 13 осей»; Contour2 = pack-defined axes; Contour1 wire open; docs/setup/usage.  
**Architecture SSOT:** [`architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md`](../../../analysis/architecture-node-specific-taxonomy-vs-hardcoded-axes-2026-09-04.md).  
**Depends:** SSR-26 Done. **Parallel P3:** 31 ∥ 32; **33 after** both.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 31 | [GW-SSR-31 — Contour2 pack axes node-specific](./STORY-GW-SSR-31-node-specific-contour2-taxonomy-axes.md) | Loader: drop lockstep; adapt SSR-26/28 tests | Done (Awaiting Commits) pkg-000088 | SSR-26 |
| 32 | [GW-SSR-32 — Contour1 wire axes open](./STORY-GW-SSR-32-node-specific-contour1-wire-axes.md) | `normalize_axis` free; intake tests; civic skip | Done (Awaiting Commits) pkg-000089 | soft 31 Done |
| 33 | [GW-SSR-33 — docs / setup / usage / test hygiene](./STORY-GW-SSR-33-node-specific-taxonomy-docs-setup-tests-hygiene.md) | README, manual, inventory; GPT-SSR-15 invert note | Done (Awaiting Commits) pkg-000090 | SSR-31 + SSR-32 Done |

**Test inventory (hygiene):**

| Area | Owner story | Notes |
|------|-------------|-------|
| Contour2 load N-axes / structural fails | SSR-31 | `test_gw_ssr_26_*` / `test_gw_ssr_31_*` / SSR-28 seed content |
| Contour1 wire custom axis | SSR-32 | `test_gw_ssr_32_*` (+ tax_01 Contour1 adapt) |
| Docs-only | SSR-33 | README / manual / INDEX / gap handoff; no pytest required |
| uus pack.json readiness/civic | **Not** 31–33 | Separate repair |

**Sibling GPT handoff (gateway records only):** [GPT-SSR-15](../../../../GPT%20UI/docs/tasks/backlog-stories/semantic-schema-runtime/STORY-GPT-SSR-15-taxonomy-meta-axis-lockstep.md) (lock Pack Builder meta to 13) must be **superseded/inverted** so meta stays free/structural — **gateway D-SSR-11 wins**. Do **not** edit GPT files in GW-SSR-33.

**Не в этой волне:** uus `pack.json` readiness/civic lens repair; `ClusterLens` expand; pack→`vocabulary.py`; GPT meta P3 (sibling invert GPT-SSR-15 executes in GPT wave).

### REQ4 §5.3 Volume / remote packs (sequence 34–35) — **D-SSR-12**

**Цель:** git = code; local warehouse = in-tree `schema-packs/` + `NODE_SCHEMA_*` (node packs не в git); Railway = Volume + **`SCHEMA_PACKS_ROOT`**; remote registry URL — **потом**.  
**Parent:** [`REQ4` §5.3](../../../../../docs/requirements%20backlog/REQ4-Node-Onboarding-Schema-Pack-Federation-Gate.md).  
**Evidence (ops without remote):** [`uus-veerenni-civic-v2-active-volume-smoke-2026-09-06.md`](../../../analysis/uus-veerenni-civic-v2-active-volume-smoke-2026-09-06.md).  
**Precondition:** loadable nested uus pack — **operator repair + retest вне** этих стори.  
**Plan trimmed from:** [`.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md`](../../../../../.cursor/plans/ssr-34_uus_v2_volume_be7b0334.plan.md).

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 34 | [GW-SSR-34 — local warehouse + Volume ops](./STORY-GW-SSR-34-uus-active-schema-packs-volume-ops.md) | Local path + gitignore node packs + Railway `SCHEMA_PACKS_ROOT` | Done (Awaiting Commits) pkg-000091 | SSR-16; loadable pack; **D-SSR-12** |
| 35 | [GW-SSR-35 — SCHEMA_ROOT_URL + refresh](./STORY-GW-SSR-35-schema-root-url-pack-refresh.md) | Federation remote registry fetch | 🔵 Done (Awaiting Commits) pkg-000092 G35 PASS 2026-09-07T08:54:22Z | soft 34 Done |

**AC split:** 34 = AC-ops (local + Volume; URL unset). 35 = AC-remote federation consume stub (**shipped**); **не** silent drop.

**Не в этой волне:** pack.json geo/content repair; GPT-PB / SCR geo validators; F4 upload; treat `SCHEMA_ROOT_URL` as Volume path; вынос local warehouse вне `schema-packs/`.

**Progress (T-wave active):** Stories **5/5 Done**. Post-T-wave product **SSR-08 + SSR-09 + SSR-10 + SSR-13 + SSR-11 + SSR-14 + SSR-15 Done**. Node-schema **SSR-16 + SSR-17 + SSR-18 Done**. Cluster-knobs **SSR-19 + SSR-20 + SSR-21 Done**. Geo-detail **SSR-22 + SSR-23 + SSR-24 + SSR-25 Done**. Taxonomy-pack **SSR-26 + SSR-28 + SSR-29 Done (Awaiting Commits)** (3/3). Geo-precision **SSR-27 Done (Awaiting Commits)** pkg-000084. SPA overlay data **SSR-30 Done (Awaiting Commits)** pkg-000087 (Declare MVP `card_fields` tallinn). **Node-taxonomy D-SSR-11: SSR-31 Done (Awaiting Commits) pkg-000088; SSR-32 Done (Awaiting Commits) pkg-000089; SSR-33 Done (Awaiting Commits) pkg-000090**. **REQ4 D-SSR-12: SSR-34 Done (Awaiting Commits) pkg-000091; SSR-35 Done (Awaiting Commits) pkg-000092 G35 PASS**. Experimental **SSR-12 Draft**. Later **06/07 Draft**.

### Experimental draft (sequence 12) — не IDX, не T-wave

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 12 | [GW-SSR-12 — complementary pair matching](./STORY-GW-SSR-12-complementary-pair-matching.md) | lost↔found / знак+схожесть; **не** exact-lens | 📝 Draft (experimental) | SSR-02 |

### Post-T-wave drafts (sequence 6–7) — refine **после** geo-detail 22–25 (без 12)

Помечены **Draft (post-T-wave refine)**. Не T-wave DoD. Не active %. Дорабатывать **после** geo-detail 22–25.

| Order | Story | Цель | Status | Depends |
|------:|-------|------|--------|---------|
| 6 | [GW-SSR-06 — analytical index later](./STORY-GW-SSR-06-analytical-index-later.md) | IDX; AC-005/006/012; **без** HTTP path | 📝 Draft (post-T-wave refine) | SSR-02; refine after 22–25 |
| 7 | [GW-SSR-07 — processor delivery later](./STORY-GW-SSR-07-processor-delivery-later.md) | PROC; AC-009/010; SEC-003 | 📝 Draft (post-T-wave refine) | SSR-01; refine after SSR-06 |

## Границы пакета

- **In scope:** T-wave + post-T-wave 08–11, 13–15 + node-schema 16–18 + cluster-knobs 19–21 + **geo-detail 22–25** + **taxonomy-pack 26/28–29** + **geo-precision 27** + **node-taxonomy 31–33 (D-SSR-11)** + **REQ4 Volume/remote 34–35** + experimental 12 + later 06/07.
- **НЕ трогаем:** `doge-identity-service`; invent filter HTTP; MVP pkg; `gateway-mvp-dashboard.md`; WASM / federation upload (F4) / form builder / GPT pack files (REQ-45); удаление `ClusterLens`; публичный `GET /schema-active`; перенос `CLUSTER_CRON_*` в pack; dual-source env+pack для семантических knobs; **pack content repair** внутри 34/35 (precondition operator).
- **Исключение D-SSR-7 (post-T-wave, Done):** URL в spa-app **трёх** Gateway*Repository (+ unit tests) и path-строки spa-16 / spa-15 sibling. **Не** overlay карточки.
- **Исключение D-SSR-8 (node-schema, Done):** новый intake без matching binding → 4xx; civic engine **остаётся**.
- **Исключение D-SSR-9 (cluster-knobs):** семантические CLUSTER_* → `node_clustering.civic` активного pack; cron остаётся env.
- **Исключение D-SSR-10 (geo-detail):** `geo_detail` + `geo_intake`; harden civic scope-gate; persist address depth; cluster via snapshot / exact_lenses `geo.*`.
- **Исключение D-SSR-11 (node-taxonomy):** Contour2/Contour1 axes node-defined; `TAXONOMY_AXIS_VALUES` reference-only; **не** расширять `ClusterLens`; **не** pack→civic vocab runtime в этой волне.
- **Исключение D-SSR-12 (Volume/local + federation consume):** local `schema-packs/` + gitignore node packs; Railway `SCHEMA_PACKS_ROOT`; `SCHEMA_ROOT_URL` = federation registry URL (**SSR-35 shipped**), не mount.
- P1.3/P3 волны geo-detail — [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) (после G21). Cluster-knobs — [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md). T-wave / post-T-wave / node-schema — исторические runbook, не очередь.

## Порядок

Граф зависимости: SSR-01 → … → SSR-05 → **08 затем 09** → **10** → **13** → **11** → **14** → **15** → **16 → 17 → 18** → **19 → 20 → 21** (cluster-knobs не ∥) → **22 → 23 → 24 → 25** (geo-detail не ∥) → **26 → 28 → 29** (taxonomy) **∥ 27** (geo-precision, after 25) → **30** → **31 ∥ 32 → 33** (node-taxonomy D-SSR-11) → **34 → 35** (REQ4 Volume ops → remote fetch) → refine 12 (opt) → refine 06 → 07.

**Исполнение overnight (OP):** сначала [`orchestrator-cluster-knobs-runbook.md`](./orchestrator-cluster-knobs-runbook.md) (19–21); затем [`orchestrator-geo-detail-runbook.md`](./orchestrator-geo-detail-runbook.md) (22–25). Исторические runbook не стартовать заново. **Не** 06/07/12.

### Продолжение (понимание → деплой → кастом нод)

| # | Item | Зачем |
|---|------|--------|
| 08 | SSR-08 civic-as-pack | Tallinn как data (путь A) |
| 09 | SSR-09 hosted apply + packs | Pack на host |
| 10 | SSR-10 dual taxonomy+exact | Ярлыки и кастомные поля |
| 13 | SSR-13 `/node/*` API | Убрать город из URL; SPA clients |
| 11 | SSR-11 pack → Issue fields | Именованные поля на `/node/issues` |
| 14 | SSR-14 docs | Инвентарь документации |
| 15 | SSR-15 tests | Paths + сценарии |
| 16 | SSR-16 node env + boot | `NODE_SCHEMA_*`; fail-fast pack |
| 17 | SSR-17 intake gate | Binding == env иначе 4xx |
| 18 | SSR-18 cluster + docs | Pack только активный; мануал |
| 19 | SSR-19 clustering pack contract | `node_clustering.civic` loader |
| 20 | SSR-20 clustering runtime wire | Factory из активного pack |
| 21 | SSR-21 clustering docs | Два контура; env inventory |
| 22 | SSR-22 civic geo-gate | Убрать silent skip scope |
| 23 | SSR-23 geo_detail wire | Wire + pack `geo_intake` |
| 24 | SSR-24 geo persist | Snapshot depth + SQL |
| 25 | SSR-25 geo cluster + docs | Civic/pack + мануал |
| 34 | SSR-34 local + Volume ops | D-SSR-12; `SCHEMA_PACKS_ROOT` / `NODE_SCHEMA_*` |
| 35 | SSR-35 remote fetch/refresh | Federation `SCHEMA_ROOT_URL` (**shipped** stub consume) |
| 12 | SSR-12 pair matching | Draft; не overnight |
| 06/07 | Draft later | IDX / processors; после 22–25 |
| Sibling | GPT REQ-45 | Pack intake из GPT |
| Sibling | spa-16 overlay | После 11; пути уже 13 |

---

## Seam validation (2026-08-28) — не стоп

Проверено по коду (`analysis.mdc`). **Нерешаемой архитектурной блокировки нет**, если держать инварианты ниже. Иллюзорных тасков «добавить член в `ClusterLens`» / «всегда прогонять pack-story через civic engine» **не** ставить (dual только SSR-10 opt-in).

| Шов | Факт | Следствие для стори |
|-----|------|---------------------|
| Envelope vs persist `schema_version` | Intake требует корневой `schema_version == m2.story_intake_envelope.v2` ([`contracts.py:236–246`](../../../../src/core/intake/contracts.py)). `StoryRecord.schema_version` пишется из request ([`services.py:236–238`](../../../../src/core/application/services.py)). | Не переиспользовать корневой ключ для semantic version. Persist: новые nullable поля; `schema_version` колонки **остаётся envelope**. |
| Civic clustering | `ClusteringEngine.active_lenses: tuple[ClusterLens, …]` ([`engine.py:215`](../../../../src/core/cluster/engine.py)); `lens_dimension` — полный dict enum→`SignalDimension` ([`:66–79`](../../../../src/core/cluster/engine.py)); `Cluster.lens: ClusterLens` ([`types.py:45`](../../../../src/core/cluster/types.py)). Сигналы только из labels/canonical ([`enrichment.py:87–106`](../../../../src/core/profile/enrichment.py)). | **Не** расширять `ClusterLens`. Pack exact-lens = отдельный engine + `ClusterMembershipStore.lens: str` ([`contracts.py:206–208`](../../../../src/core/domain/contracts.py), sqlite `cluster_memberships.lens TEXT` [`db_sqlite.py:351–356`](../../../../src/core/infrastructure/db_sqlite.py)). |
| Civic orchestrator | **As-of-Done (SSR-05 pkg-000065):** schema-bound `process_story` → `_process_pack_bound_story` (may return issue_id after pack promote) ([`cluster_orchestrator.py:236–237`](../../../../src/core/application/cluster_orchestrator.py)); civic pool `_civic_ready` ([`:86–87`](../../../../src/core/application/cluster_orchestrator.py)). **As-of-Done (SSR-04 pkg-000064) / Historical for SSR-05:** pack branch then return None ([`:143–145`](../../../../src/core/application/cluster_orchestrator.py) pre-promote). **Historical (pre-SSR-04):** `process_story` брал **все** READY_FOR_PROFILE без фильтра. **As-of-Done (SSR-18 pkg-000075):** pack-ветка только если persist binding == `NODE_SCHEMA_*`; mismatch bound → skip+log (`cluster.skipped_schema_mismatch`); unbound legacy civic as-is; dual from **active** pack.json. G18 PASS 2026-08-30T15:06:33Z. | Pack-bound исключены из civic engine (AC-008). Pack issue_id только после gate pass. Не кластеризовать чужим pack.json. |
| Promotion | **As-of-Done (SSR-05 pkg-000065):** Default `require_actionable_canonical_type=True` + `complaint`/`system_bug` ([`gates.py:7–14`](../../../../src/core/promotion/gates.py)). `_create_issue` passes `policy=command.gate_policy` ([`issue_create.py:232`](../../../../src/core/application/issue_create.py)); `None` = civic. **Historical (pre-SSR-05):** `_create_issue` всегда civic `submit_for_review` без `policy=` ([`:226–229`](../../../../src/core/application/issue_create.py)). | Pack promotion: **override policy** на вызове, не менять default civic. |
| Persist constructors | **As-of-Done (SSR-17 pkg-000074):** omit/`{}`/null binding → 4xx; match `NODE_SCHEMA_*` → validate active pack then persist client pair. **As-of-Done (SSR-03 pkg-000063):** intake create writes binding when `schema_binding` present (`services.py` validate + `StoryRecord(` map). **Historical (pre-SSR-17):** civic omit stayed None. **As-of-Done (SSR-02 pkg-000062):** `advance_story_readiness` `dataclasses.replace`; sqlite INSERT + `ON CONFLICT DO UPDATE SET` including binding; supabase row + omit-probe. **Historical (pre-SSR-03):** intake omitted binding. **Historical (pre-SSR-02 P3):** lifecycle copy без новых полей. | Binding persist + wire closed. Забыть `replace` = silent wipe. **Не** класть binding в `required_columns_ready`. |
| sqlite vs memory lifecycle | sqlite/supabase `update_lifecycle_status` меняет только `lifecycle_status` ([`db_sqlite.py:670`](../../../../src/core/infrastructure/db_sqlite.py)); in-memory — `replace()` ([`repositories.py:95–101`](../../../../src/core/infrastructure/repositories.py)). | Статус CLUSTERED **не** стирает extra columns. Опасен `save_story` полного реконструкта. |
| Hosted SELECT | **As-of-Done (SSR-02 pkg-000062):** `_STORY_SELECT_FIELDS` includes binding [`db_supabase.py:67–76`](../../../../src/core/infrastructure/db_supabase.py); omit-probe omits `geo_admin_*` **and** `_STORIES_BINDING_COLUMNS` [`:470–476`](../../../../src/core/infrastructure/db_supabase.py); `required_columns_ready` [`:388`](../../../../src/core/infrastructure/db_supabase.py) does **not** include binding names. Cross-layer: [`000_full_init.sql`](../../../../supabase/bootstrap/000_full_init.sql) ↔ SELECT ([`test_stories_schema_cross_layer_invariant.py`](../../../../tests/test_stories_schema_cross_layer_invariant.py)). **Historical (pre-P3):** omit-probe только для `geo_admin_*` [`:418–427`](../../../../src/core/infrastructure/db_supabase.py); `required_columns_ready` cite `:336`. | Binding omit-probe допустим до hosted apply. **Не** класть binding в `/ready` required set (урок GAP-07 / L10N-03). |
| JSON Schema lib | **As-of-Done (SSR-01 pkg-000061):** `jsonschema>=4.18.0` in [`pyproject.toml:16`](../../../../pyproject.toml) and [`requirements.txt:5`](../../../../requirements.txt); importable (`Draft202012Validator`). **Historical (pre-P3):** dependency отсутствовала. | SSR-01 T01 closed; не самописный «почти JSON Schema». |
| `/ready` tables | `REQUIRED_READINESS_TABLES` уже содержит `stories` ([`db_supabase.py:29–43`](../../../../src/core/infrastructure/db_supabase.py)). | ALTER колонок `stories` ≠ новая таблица. **Не** класть later `story_dimensions` в REQUIRED без отдельного решения (SSR-06 refine). |
| Civic membership vs Issue | **As-of-Done (SSR-05 pkg-000065):** pack `_process_pack_bound_story` saves membership then `_promote_pack_membership`; `CLUSTERED` only after successful pack `create_issue` ([`cluster_orchestrator.py:90–91`](../../../../src/core/application/cluster_orchestrator.py), [`:188–193`](../../../../src/core/application/cluster_orchestrator.py)). Civic `_persist_memberships` still only after civic `create_issue`. **As-of-Done (SSR-04) / Historical for SSR-05:** pack `save_membership` without Issue/`CLUSTERED` ([`:89–123`](../../../../src/core/application/cluster_orchestrator.py) pre-promote). **Historical:** `_persist_memberships` вызывался **только после** успешного civic `create_issue`. | Pack membership до Issue; pack `CLUSTERED` после pack promote. Civic path unchanged. Engine идемпотентен на повтор cron. |
| Cron invocation | [`cluster_cron.py:64`](../../../../src/core/scheduler/cluster_cron.py) зовёт только `StoryClusterOrchestrator.process_all_pending`. | **Не** второй cron. Ветка schema-bound **внутри** `process_story` / `process_all_pending`. Иначе pack membership в проде никогда не бежит. |
| Civic readiness formula | `readiness_score_for_cluster(*, lens: ClusterLens, …)` [`engine.py:192–206`](../../../../src/core/cluster/engine.py). | Pack **не** вызывать. Score T-wave — из pack `readiness policy` / `min_size` (loader contract SSR-01 T00), не формула `20 + size*15`. |
| Promotion knobs | **As-of-Done (SSR-05 pkg-000065):** `PromotionGatePolicy` = 3 поля ([`gates.py:11–14`](../../../../src/core/promotion/gates.py)). Factory civic singleton [`service_factory.py:108–111`](../../../../src/core/infrastructure/service_factory.py). Mapper [`pack_policy.py`](../../../../src/core/schema/pack_policy.py). `submit_for_review` `effective_policy` ([`service.py:85`](../../../../src/core/promotion/service.py)). **Historical:** `submit_for_review` всегда `self.gate_policy` ([`service.py:84–86`](../../../../src/core/promotion/service.py) pre-override). | T-wave pack policy **мапится на эти 3 knobs** (`require_actionable_canonical_type=False` + числа из example pack). Не invent новые `reasons` и не менять factory default. Override на вызов `submit_for_review`. |
| Identity | Intake уже подменяет submitter из introspection ([`handlers.py:221–228`](../../../../src/core/api/handlers.py)). | **D-SSR-3:** не трогать. `enforce_policy(..., policy_context)` без identity claims. |
| Draft stash | **As-of-Done (SSR-17 pkg-000074):** Null/`{}` / absent → `IntakeValidationError`; mismatch vs `NODE_SCHEMA_*` → 4xx; match → validate active pack. Stash + submit share parse. **As-of-Done (SSR-03 pkg-000063):** `_parse_story_envelope_body` returns binding with `gpt_signals`; `intake_request_from_stash_and_submitter` copies `schema_binding`. **Historical:** 6-tuple without binding; Null/`{}` = civic. | Stash must keep matching `NODE_SCHEMA_*` through submit. |
| Civic geo gate | **As-of-Done (SSR-25 pkg-000082):** civic snapshot depth не ломает `geo_filter_bucket` (admin_*); pack exact membership на `structured_payload.geo.*`; manual §geo_detail; G25 PASS 2026-08-30T21:27:05Z; ClusterLens=10. **As-of-Done (SSR-24 pkg-000081):** `StoryGeoSnapshot` street/house/house_range/houses/address_line persist sqlite+supabase; omit-probe; not in `required_columns_ready`; G24 PASS 2026-08-30T21:00:56Z. **As-of-Done (SSR-23 pkg-000080):** root sidecar `geo_detail` + pack `geo_intake` (`optional` default); merge with `location_query`; invalid/require miss → 4xx; optional omit → 202; ClusterLens=10. G23 PASS 2026-08-30T20:40:50Z. **As-of-Done (SSR-22 pkg-000079):** scope + `geo_service is None` → `IntakeValidationError("geo unavailable")` ([`handlers.py:258–260`](../../../../src/core/api/handlers.py)); scope-check только если `geo_scope` **и** непустой `location_query`. **Historical (pre-SSR-22):** silent skip when `geo_service is None`. **Historical (pre-SSR-24):** `StoryGeoSnapshot` без street/houses ([`contracts.py:28–40`](../../../../src/core/domain/contracts.py) pre-P3). **Historical (pre-SSR-25):** no `test_gw_ssr_25_*`; manual без `geo_intake` chapter. | **D-SSR-10:** geo-detail wave closed after G25. REQ-35 omit stays 202 while pack `mode=optional`. |

**Жёсткий запрет на «удобные» таски:** новый `ClusterLens.*`; удаление civic engine; domain fields в parser; HTTP filter; смена default `PromotionGatePolicy` / factory civic policy type; правка identity; «Generic Processor = validate()»; `story_dimensions` в T-wave; membership pack через civic `_persist_memberships` после Issue; invent `DEFAULT_SCHEMA_PACK`; публичный `GET /schema-active`; dual-source env+pack для семантических cluster knobs; перенос cron в pack; глобальный «без geo → 4xx» без pack `geo_intake`. **Исключение (SSR-10):** civic engine на bound story только если pack **явно** dual; default = T-wave (exact-only). **Исключение (D-SSR-7):** URL трёх spa Gateway*Repository + spa-16/15 path strings; не overlay карточки; не alias `/tallinn/*`. **Исключение (D-SSR-8):** новый intake без matching binding → 4xx; civic engine остаётся для dual активного pack и unbound legacy. **Исключение (D-SSR-9):** семантические CLUSTER_* → `node_clustering.civic`; cron остаётся env. **Исключение (D-SSR-10):** `geo_detail` + `geo_intake`; harden scope-gate; persist address depth; cluster via snapshot / `geo.*` lenses. **Исключение (D-SSR-11):** Contour2/Contour1 axes node-defined (SSR-31…33); не расширять ClusterLens под имена осей.
