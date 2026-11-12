# STORY-GW-SSR-25 — Geo detail clustering + docs

## Meta
- **Key:** `STORY-GW-SSR-25-geo-detail-clustering-docs`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **25**; конец волны после G25)
- **Тип:** implement (cluster regression) + docs
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-25-geo-detail-clustering-docs.md)
- **Parent REQ:** 51 CL; INDEX **D-SSR-10**
- **Decision:** INDEX **D-SSR-10**
- **decision_ref:** backlog SSR-25 + INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-24](../STORY-GW-SSR-24-geo-detail-persist/STORY-GW-SSR-24-geo-detail-persist.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000082-20260830-gw-ssr-25-geo-detail-clustering-docs.yaml`](../../../../gateway-active-packages/pkg-000082-20260830-gw-ssr-25-geo-detail-clustering-docs.yaml)
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-24 ([pipeline](../STORY-GW-SSR-24-geo-detail-persist/STORY-GW-SSR-24-geo-detail-persist.md)); G24 PASS
- **Scaffolded:** 2026-08-30T21:20:50Z
- **P4 audit:** 2026-08-30T21:31:59Z [`audit-gw-ssr-25-geo-detail-clustering-docs-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-25-geo-detail-clustering-docs-2026-08-30.md) · product AC yes · G1 n/a (SSOT already As-of-Done) · G2 WAIVED-likely operator

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 CL | INDEX **D-SSR-10** |
| Decision | INDEX **D-SSR-10** | civic/pack cluster + `geo_intake` docs |

- **Разблокирует:** G25 → стоп волны geo-detail (не 06/07/12).
- **Не reopen:** SSR-01…05 / 08–24 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; invent HTTP geo-filter; IDX / `story_dimensions`; bullrun §«Актуальная точка»

## Nested tasks (pkg-000082)

| ID | Folder |
|----|--------|
| T01 | [`task-gw-ssr-25-t01-civic-cluster-regression`](./task-gw-ssr-25-t01-civic-cluster-regression/README.md) |
| T02 | [`task-gw-ssr-25-t02-pack-exact-geo-lenses`](./task-gw-ssr-25-t02-pack-exact-geo-lenses/README.md) |
| T03 | [`task-gw-ssr-25-t03-manual-geo-intake`](./task-gw-ssr-25-t03-manual-geo-intake/README.md) |
| T04 | [`task-gw-ssr-25-t04-readme-matrix`](./task-gw-ssr-25-t04-readme-matrix/README.md) |
| T05 | [`task-gw-ssr-25-t05-story-acceptance-gate`](./task-gw-ssr-25-t05-story-acceptance-gate/README.md) |

## Зачем простыми словами

Нормализованное geo должно участвовать в кластеризации: civic — через snapshot/`geo_filter`; pack — через `exact_lenses` на `geo.*`, если линзы объявлены. Мануал — как настроить `geo_intake` и lenses на ноде.

## Scope / Out of scope

**In:** civic `test_clustering_engine.py` зелёный с расширенным snapshot; pack exact membership по `geo.street` / `geo.district` / … (fixture + optional tallinn pack lens update если нужно для demo). Документы: глава в [`schema-packs-node-data-model-ru.md`](../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) — `geo_detail`, `geo_intake` modes, mirror, два пути cluster (civic vs exact); [`schema-packs/README.md`](../../../../../../schema-packs/README.md) сверка; smoke / [test-matrix](../../../../../../docs/runtime-docs/testing/test-matrix-by-type-layer-mocks.md) одна правка. Тесты `test_gw_ssr_25_*`.

**Out:** GPT instruction pack; SPA map overlay UI; invent HTTP geo-filter API; расширение `ClusterLens` enum.

## Verified current state

| Fact | Ref |
|------|-----|
| Civic `geo_filter_bucket` = admin_* only | [`scope.py:55–63`](../../../../../../src/core/geo/scope.py), [`:94–101`](../../../../../../src/core/geo/scope.py); [`engine.py:101`](../../../../../../src/core/cluster/engine.py) |
| Pack exact = payload `source_fields` | [`pack_engine.py:57`](../../../../../../src/core/schema/pack_engine.py), [`:129–140`](../../../../../../src/core/schema/pack_engine.py) |
| Tallinn lens `geo.district`; payload `geo.street` optional | [`pack.json:15–19`](../../../../../../schema-packs/tallinn_civic/v1/pack.json), [`:101–102`](../../../../../../schema-packs/tallinn_civic/v1/pack.json) |
| **As-of-Done:** manual §geo_detail / `geo_intake` | [`schema-packs-node-data-model-ru.md`](../../../../../../docs/runtime-docs/manuals/schema-packs-node-data-model-ru.md) |
| README SSR-23 sidecar + SSR-25 clustering сверка | [`schema-packs/README.md`](../../../../../../schema-packs/README.md) |
| **As-of-Done:** `test_gw_ssr_25_*` | [`test_gw_ssr_25_geo_detail_clustering.py`](../../../../../../tests/test_gw_ssr_25_geo_detail_clustering.py) |
| Snapshot depth persist (SSR-24) | [`contracts.py:41–45`](../../../../../../src/core/domain/contracts.py) |
| G24 PASS | pkg-000081; `2026-08-30T21:00:56Z` |
| `ClusterLens` = 10 | [`types.py:10–22`](../../../../../../src/core/cluster/types.py) |

## Стыковка

Не учить dual-source env+pack для geo knobs (D-SSR-9). Не учить «клиент любой pack». D-SSR-10: optional vs require — pack. Civic `geo_filter_bucket` остаётся `admin_*`.

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

Civic snapshot depth не ломает `geo_filter_bucket`. Pack exact на `geo.*`. Manual §geo_detail. G25 **811 passed**, 18 skipped, 10 deselected; ClusterLens=10. T-wave G3 stays.

## Dependencies

- SSR-24 Done (G24). Refine 06/07/12 **не** эта стори. После G25 — стоп волны.
