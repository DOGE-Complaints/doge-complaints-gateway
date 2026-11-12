# STORY-GW-SSR-18 — Кластеризация от активной схемы ноды

## Meta
- **Key:** `STORY-GW-SSR-18-cluster-active-schema`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — node-schema wave (sequence **18**; конец overnight)
- **Тип:** implement (orchestrator + docs)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-18-cluster-active-schema.md)
- **Parent REQ:** 51 CL; INDEX **D-SSR-8**
- **Decision:** INDEX **D-SSR-8**
- **decision_ref:** backlog SSR-18 + INDEX **D-SSR-8**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-17](../STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000075-20260830-gw-ssr-18-cluster-active-schema.yaml`](../../../../gateway-active-packages/pkg-000075-20260830-gw-ssr-18-cluster-active-schema.yaml)
- **Git:** только `semantic-schema-runtime` — [node-schema Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-node-schema-runbook.md)
- **Зависит от:** SSR-17 ([pipeline](../STORY-GW-SSR-17-intake-active-schema-gate/STORY-GW-SSR-17-intake-active-schema-gate.md))
- **Scaffolded:** 2026-08-30T14:55:04Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 CL | INDEX **D-SSR-8** |
| Decision | INDEX **D-SSR-8** | pack-ветка только если persist == `NODE_SCHEMA_*` |

- **Разблокирует:** G18 → STOP волны (не 06/07/12).
- **Не reopen:** SSR-01…05 / 08–17 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; new SQL; bullrun §«Актуальная точка»

## Nested tasks (pkg-000075)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-18-t01-pack-iff-active-pair`](./task-gw-ssr-18-t01-pack-iff-active-pair/README.md) |
| T02 | [`task-gw-ssr-18-t02-civic-unbound-legacy`](./task-gw-ssr-18-t02-civic-unbound-legacy/README.md) |
| T03 | [`task-gw-ssr-18-t03-tests`](./task-gw-ssr-18-t03-tests/README.md) |
| T04 | [`task-gw-ssr-18-t04-docs-warehouse-vs-env`](./task-gw-ssr-18-t04-docs-warehouse-vs-env/README.md) |
| T05 | [`task-gw-ssr-18-t05-story-acceptance-gate`](./task-gw-ssr-18-t05-story-acceptance-gate/README.md) |
| T06 | [`task-gw-ssr-18-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-18-t06-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Кастомизация кластеризации **уже** в pack.json (`exact_lenses`, `readiness_policy`, `dual_civic_lenses`). Сейчас pack берётся с **story**. После 17 новые stories совпадают с env; эта стори — защита и смысл «сервер»: pack-ветка только если persist binding == `NODE_SCHEMA_*`. Чужой bound (старые rows) — skip, не кластеризовать чужим pack. Unbound legacy — civic engine as-is. `ClusterLens` не удалять.

## Scope / Out of scope

**In:** [`cluster_orchestrator.py`](../../../../../../src/core/application/cluster_orchestrator.py) `process_story` (`:303–307` bound match → `_process_bound_story`; mismatch skip). Pack engine + dual только если `(story.schema_id, story.bound_schema_version)` == конфиг. Иначе лог skip, не membership. `_civic_ready` по-прежнему unbound only. Dual — флаг **активного** pack.json ([`pack_engine.py`](../../../../../../src/core/schema/pack_engine.py) `dual_civic_lenses_for_ref`). Тесты `test_gw_ssr_18_*`: mismatch bound skip; match pack membership; unlabeled civic `test_clustering_engine.py` зелёный. Docs: [`schema-packs-node-data-model-ru.md`](../../../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) — склад vs рабочая env; 4xx intake; кластеризация. Smoke matrix: canvas/smoke payload `schema_binding` = env сервера ([test-matrix](../../../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md)).

**Out:** новый cron; IDX; удаление civic engine; GPT UI; invent filter HTTP.

**Сеам GPT:** без emit `schema_binding` с id **этой** ноды прод-intake из GPT сломается. Правка GPT UI **не** эта реализация.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-18 pkg-000075):** bound == `NODE_SCHEMA_*` → pack/dual; mismatch bound → skip+log `cluster.skipped_schema_mismatch` (не civic, не чужой pack.json) | [`cluster_orchestrator.py:303–307`](../../../../../../src/core/application/cluster_orchestrator.py), `:93–111` |
| **As-of-Done:** dual from **active** pack.json (`NODE_SCHEMA_*`), not foreign story pack | [`:113–124`](../../../../../../src/core/application/cluster_orchestrator.py); [`pack_engine.py:71–79`](../../../../../../src/core/schema/pack_engine.py) |
| **As-of-Done:** unbound READY_FOR_PROFILE civic as-is (`_civic_ready` unbound-only) | [`:89–91`](../../../../../../src/core/application/cluster_orchestrator.py) |
| Cron | [`cluster_cron.py:64`](../../../../../../src/core/scheduler/cluster_cron.py) `process_all_pending` |
| Civic unlabeled tests | `tests/test_clustering_engine.py` |
| **Historical (pre-SSR-18):** Bound → pack **этой** story (`:274–275`); dual from story pack | same paths pre-P3 |

## Стыковка

Не подменять `story.schema_id` на env при кластеризации чужого payload (legal_process vs tallinn schema). Skip безопаснее.

Новый intake после 17 mismatch не persist — mismatch rows только **legacy**.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Orchestrator | Pack/dual iff binding == NODE_SCHEMA_*; else skip | ClusterLens member |
| **T02** | Civic legacy | Unbound READY_FOR_PROFILE civic as-is | Migrate civic rows |
| **T03** | Tests | mismatch skip; match pack; civic unlabeled green | Второй cron |
| **T04** | Docs | Мануал человеческий; test-matrix smoke binding=env | Перепись T-wave G3 |
| **T05** | Gate | skip log; civic engine green; offline pytest; мануал не учит «клиент любой pack» | |

## Target / AC

- [x] Bound ≠ активная пара → нет pack membership / не чужой pack.json.
- [x] Bound == активная → exact-lenses **этого** pack (dual если pack.json true).
- [x] Unbound legacy → civic path; `ClusterLens` 10.
- [x] Мануал: склад vs `NODE_SCHEMA_*`; intake 4xx; кластеризация с сервера.
- [x] Smoke docs: binding в payload = env процесса.

## Dependencies

- SSR-17. Refine 06/07/12 **не** эта стори.
