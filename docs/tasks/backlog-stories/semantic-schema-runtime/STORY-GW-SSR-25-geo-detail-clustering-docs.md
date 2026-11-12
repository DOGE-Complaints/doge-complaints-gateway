# STORY-GW-SSR-25 — Geo detail clustering + docs

## Meta
- **Key:** `STORY-GW-SSR-25-geo-detail-clustering-docs`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **25**; конец overnight)
- **Тип:** implement (cluster regression) + docs
- **Parent REQ:** 51 CL; INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](./orchestrator-geo-detail-runbook.md)
- **Pipeline:** [`../../../epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-25-geo-detail-clustering-docs/STORY-GW-SSR-25-geo-detail-clustering-docs.md`](../../../epics/EPIC-semantic-schema-runtime/stories/STORY-GW-SSR-25-geo-detail-clustering-docs/STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Operative queue:** [`../../gateway-active-packages/pkg-000082-20260830-gw-ssr-25-geo-detail-clustering-docs.yaml`](../../gateway-active-packages/pkg-000082-20260830-gw-ssr-25-geo-detail-clustering-docs.yaml)
- **Зависит от:** SSR-24
- **Scaffolded:** 2026-08-30T21:20:50Z

## Зачем простыми словами

Нормализованное geo должно участвовать в кластеризации: civic — через snapshot/`geo_filter`; pack — через `exact_lenses` на `geo.*`, если линзы объявлены. Мануал — как настроить `geo_intake` и lenses на ноде.

## Scope / Out of scope

**In:** civic `test_clustering_engine.py` зелёный с расширенным snapshot; pack exact membership по `geo.street` / `geo.district` / … (fixture + optional tallinn pack lens update если нужно для demo). Документы: глава в [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) — `geo_detail`, `geo_intake` modes, mirror, два пути cluster (civic vs exact); [`schema-packs/README.md`](../../../../schema-packs/README.md) сверка; smoke / [test-matrix](../../../runtime-docs/testing/test-matrix-by-type-layer-mocks.md) одна правка. Тесты `test_gw_ssr_25_*`.

**Out:** GPT instruction pack; SPA map overlay UI; invent HTTP geo-filter API; расширение `ClusterLens` enum.

## Verified current state

| Fact | Ref |
|------|-----|
| Civic key + `geo_filter_bucket` | [`engine.py`](../../../../src/core/cluster/engine.py), [`scope.py:94–101`](../../../../src/core/geo/scope.py) |
| Pack exact только payload paths | [`pack_engine.py`](../../../../src/core/schema/pack_engine.py) |
| Tallinn lens geo.district | [`pack.json`](../../../../schema-packs/tallinn_civic/v1/pack.json) geographic_district_micro |

## Стыковка

Не учить dual-source env+pack для geo knobs (D-SSR-9). Не учить «клиент любой pack». D-SSR-10: optional vs require — pack.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T01** | Civic cluster | Regression unlabeled + snapshot depth | New ClusterLens |
| **T02** | Pack cluster | exact lens на geo.* с mirrored payload | Second cron |
| **T03** | Manual | Глава geo_intake / detail / cluster | Invent schema-active |
| **T04** | README/matrix | Сверка | T-wave G3 rewrite |
| **T05** | Gate | civic green; pack membership; docs; ClusterLens=10 | |

## Target / AC

- [x] Civic clustering зелёный с новым snapshot.
- [x] Pack exact membership по настроенным `geo.*` lenses.
- [x] Мануал: modes, mirror, civic vs exact.
- [x] T-wave G3 / closed audits не в diff.
- [x] Offline suite / story tests зелёные.

## Verified As-of-Done (P3 2026-08-30T21:27:05Z)

Civic snapshot depth не ломает `geo_filter_bucket` (admin_* only). Pack exact membership на `structured_payload.geo.*` (tallinn `geo.district` + fixture `geo.street`). Manual §geo_detail: modes / mirror / civic vs exact. G25: **811 passed**, 18 skipped, 10 deselected; ClusterLens=10. T-wave G3 `:271` не переписан.

## Dependencies

- SSR-24. Refine 06/07/12 **не** эта стори.
