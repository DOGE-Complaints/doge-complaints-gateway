# STORY-GW-SSR-21 — Node clustering docs (кастомизация ноды)

## Meta
- **Key:** `STORY-GW-SSR-21-node-clustering-docs`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — cluster-knobs wave (sequence **21**; конец overnight)
- **Тип:** docs (runtime manuals + env inventory)
- **Parent REQ:** 51 SCHEMA; INDEX **D-SSR-9**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [cluster-knobs Шаг 0](./orchestrator-cluster-knobs-runbook.md)
- **Зависит от:** SSR-20

## Зачем простыми словами

После wiring оператор должен понимать: пороги civic и exact — **в pack**, cron — в `.env`. Старые таблицы env не должны учить семантические `CLUSTER_*` как текущий контракт. Мануал ноды — глубоко про кастомизацию двух контуров.

## Scope / Out of scope

**In:** глубокая глава в [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md): склад vs рабочая `NODE_SCHEMA_*`; **два контура** (`exact_lenses` vs `node_clustering.civic`); как сменить пороги/линзы/geo **без** `.env` (правка pack + рестарт); dual; unbound legacy; cron = процесс. [`05-env-config-and-launch.md`](../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md) строки про семантические CLUSTER_* (≈111–120) → «перенесено в pack / см. мануал»; оставить `CLUSTER_CRON_*`. [`server-env-quickstart.md`](../../../runtime-docs/manuals/server-env-quickstart.md) — убрать обязательность/инструкции семантических CLUSTER_* как текущий путь. Сверка [`schema-packs/README.md`](../../../../schema-packs/README.md) (ключ уже с 19). Smoke / [`test-matrix`](../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md) — одна правка если упоминает CLUSTER_ACTIVE_LENSES как единственный способ. INDEX/дашборд Status после Done этой стори (постановка D-SSR-9 уже на диске).

**Out:** product code кроме doc-driven typos; перепись T-wave G3; bullrun «Актуальная точка»; `gateway-mvp-dashboard.md`; GPT UI.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-21 pkg-000078):** 05-env semantic CLUSTER_* = **Не текущий SSOT** / pack; `CLUSTER_CRON_*` stay | [`05-env-config-and-launch.md:111–113`](../../../runtime-docs/bootstrap-infrastructure/05-env-config-and-launch.md) |
| **As-of-Done:** server-env не требует semantic CLUSTER_* для кастомизации | [`server-env-quickstart.md:118`](../../../runtime-docs/manuals/server-env-quickstart.md) |
| **As-of-Done:** мануал два контура + how-to pack+рестарт | [`schema-packs-node-data-model-ru.md:59–80`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) |
| **As-of-Done:** README factory from pack civic; test-matrix pack `active_lenses` | [`schema-packs/README.md:30`](../../../../schema-packs/README.md); [`test-matrix-by-type-layer-mocks.md:79`](../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md) |
| **Historical (pre-SSR-21):** 05-env учит CLUSTER_* из env; server-env `CLUSTER_ACTIVE_LENSES` обязателен; мануал мало про CLUSTER_* | same paths pre-P3 |

## Стыковка

Не учить «клиент выбирает pack». Не учить dual-source env+pack. Geo `settlement:tallinn` в pack tallinn — данные зоны, не URL `/tallinn`.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Manual | Глава двух контуров + how-to смены knobs | Invent HTTP schema-active |
| **T02** | Env docs | 05-env + server-env: семантика → pack; cron stay | Удалить cron из docs |
| **T03** | README/matrix | Сверка README; test-matrix при необходимости | Перепись audits |
| **T04** | Gate | 05 не учит семантические CLUSTER_* как текущий контракт; мануал оба контура; cron env | |

## Target / AC

- [x] Мануал явно разделяет exact_lenses vs `node_clustering.civic`.
- [x] Операторский путь смены порогов/линз/geo = правка активного pack + рестарт.
- [x] `05-env-config-and-launch.md` не учит строки 111–120 как текущий SSOT; cron documented.
- [x] `server-env-quickstart.md` не требует семантические CLUSTER_* для кастомизации.
- [x] T-wave G3 / closed audits не в diff.

## Dependencies

- SSR-20. Refine 06/07/12 **не** эта стори.
