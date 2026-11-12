# STORY-GW-SSR-23 — geo_detail wire + pack geo_intake

## Meta
- **Key:** `STORY-GW-SSR-23-geo-detail-intake-contract`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **23**)
- **Тип:** implement (intake parse + pack policy)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-23-geo-detail-intake-contract.md)
- **Parent REQ:** 51 FLOW / SCHEMA; INDEX **D-SSR-10**
- **Decision:** INDEX **D-SSR-10**
- **decision_ref:** backlog SSR-23 + INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-22](../STORY-GW-SSR-22-civic-geo-gate-hardening/STORY-GW-SSR-22-civic-geo-gate-hardening.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000080-20260830-gw-ssr-23-geo-detail-intake-contract.yaml`](../../../../gateway-active-packages/pkg-000080-20260830-gw-ssr-23-geo-detail-intake-contract.yaml)
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-22 ([pipeline](../STORY-GW-SSR-22-civic-geo-gate-hardening/STORY-GW-SSR-22-civic-geo-gate-hardening.md)); G22 PASS
- **Scaffolded:** 2026-08-30T20:29:24Z
- **P4 audit:** 2026-08-30T20:44:21Z [`audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md`](../../../../../../analysis/audit-gw-ssr-23-geo-detail-intake-contract-2026-08-30.md) · product AC yes · G1 OPEN SSOT · G2 WAIVED-likely operator

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 FLOW / SCHEMA | INDEX **D-SSR-10** |
| Decision | INDEX **D-SSR-10** | `geo_detail` + pack `geo_intake` |

- **Разблокирует:** G23 → SSR-24 (не этот pkg).
- **Не reopen:** SSR-01…05 / 08–22 product; T-wave G3 historical
- **Не трогаем:** GPT UI; `ClusterLens`; `GET /schema-active`; SQL street/houses (→24); глобальный require-geo; bullrun §«Актуальная точка»

## Nested tasks (pkg-000080)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-23-t00-contract-readme`](./task-gw-ssr-23-t00-contract-readme/README.md) |
| T01 | [`task-gw-ssr-23-t01-parse-sidecar`](./task-gw-ssr-23-t01-parse-sidecar/README.md) |
| T02 | [`task-gw-ssr-23-t02-pack-geo-intake`](./task-gw-ssr-23-t02-pack-geo-intake/README.md) |
| T03 | [`task-gw-ssr-23-t03-merge-location`](./task-gw-ssr-23-t03-merge-location/README.md) |
| T04 | [`task-gw-ssr-23-t04-tests`](./task-gw-ssr-23-t04-tests/README.md) |
| T05 | [`task-gw-ssr-23-t05-story-acceptance-gate`](./task-gw-ssr-23-t05-story-acceptance-gate/README.md) |
| T06 | [`task-gw-ssr-23-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-23-t06-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

Клиент должен уметь слать **стандартизированную** геодетализацию (координаты + адрес до глубины: улица, диапазон домов, несколько домов), не только свободный `location_query`. Обязательность решает **pack** (`geo_intake`), не глобальный хардкод.

## Scope / Out of scope

**In:** объект **`geo_detail`** на envelope (предпочтение: **root sidecar рядом с narrative / schema_binding**, класс изменения как `gpt_signals` — не invent второй binding). Поля (этот loader): optional pair `latitude`/`longitude`; `address` components: country / region / settlement / district / street / `house` **или** `house_range` **или** `houses[]`; `normalized_label`; optional `confidence` / `provider`. Pack блок **`geo_intake`**: `mode` = `optional` \| `require_location_or_detail` \| `require_detail`; `merge` (client detail wins over provider miss); `mirror_to_payload` (bool). Parse в [`contracts.py`](../../../../../../src/core/intake/contracts.py) (stash+submit share); validate vs pack; merge с `location_query` → resolve. Обновить example packs + payload.schema `geo.*` paths. Документ в [`schema-packs/README.md`](../../../../../../schema-packs/README.md). Тесты `test_gw_ssr_23_*`: accept detail; invalid → 4xx; optional omit → 202; `require_detail` miss → 4xx.

**Out:** SQL columns street/houses beyond map-to-existing snapshot fields если ещё нет (→24); ClusterLens; GPT UI files.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-23 pkg-000080):** root sidecar `geo_detail` parse (stash+submit); invalid → `IntakeValidationError` | [`contracts.py:151–162`](../../../../../../src/core/intake/contracts.py), [`:650–654`](../../../../../../src/core/intake/contracts.py) |
| **As-of-Done:** sidecars `gpt_signals` + `schema_binding` + optional `geo_detail` | [`contracts.py:193`](../../../../../../src/core/intake/contracts.py), [`:209`](../../../../../../src/core/intake/contracts.py) |
| **As-of-Done:** pack `geo_intake` required; three packs `mode=optional` | [`resolver.py:254`](../../../../../../src/core/schema/resolver.py), [`:343`](../../../../../../src/core/schema/resolver.py) |
| **As-of-Done:** merge `geo_detail` + `location_query` (fuzzy resolve stays) | [`services.py:220–227`](../../../../../../src/core/application/services.py), [`:281–286`](../../../../../../src/core/application/services.py) |
| **As-of-Done:** Tallinn payload `geo.*` (district…houses) | [`payload.schema.json:23–38`](../../../../../../schema-packs/tallinn_civic/v1/payload.schema.json) |
| **Historical (pre-SSR-23):** Wire geo = `narrative.location_query` only; sidecars without `geo_detail` | pre-P3 |
| **Historical (pre-SSR-23):** Tallinn payload `geo.district` only | [`payload.schema.json:23–28`](../../../../../../schema-packs/tallinn_civic/v1/payload.schema.json) pre-P3 |
| **As-of-Done (SSR-24):** snapshot depth persist — street/house/houses (см. SSR-24) | [`domain/contracts.py:28–45`](../../../../../../src/core/domain/contracts.py) |
| **Historical (pre-SSR-24):** snapshot без street/houses | [`domain/contracts.py:28–40`](../../../../../../src/core/domain/contracts.py) pre-P3 |
| SSR-22: scope + no service → geo unavailable | [`handlers.py:258–260`](../../../../../../src/core/api/handlers.py) |

## Стыковка

Не silent coerce чужого pack. `location_query` остаётся для fuzzy resolve. `mirror_to_payload` готовит exact-lenses; полный persist depth — SSR-24. Scope gate из 22 остаётся.

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T00** | Contract | Shape `geo_detail` + `geo_intake` в README | Frozen dialect invent |
| **T01** | Parse | Root/narrative sidecar; stash+submit | Новый intake path |
| **T02** | Pack | Loader `geo_intake`; three packs modes | Env override |
| **T03** | Merge | Detail + location_query → snapshot draft | Drop location_query |
| **T04** | Tests | `test_gw_ssr_23_*` | SQL migration (→24) |
| **T05** | Gate | modes; invalid 4xx; ClusterLens=10 | |
| **T06** | Docs | As-of-Done vs Historical §Verified / T00–T03 Code Facts | Runtime; §Актуальная точка |

## Target / AC

- [x] `geo_detail` парсится; invalid → IntakeValidationError.
- [x] `geo_intake.mode` управляет обязательностью.
- [x] Optional omit зелёный; require_detail miss → 4xx.
- [x] Merge с `location_query` задокументирован и покрыт тестом.
- [x] README ключи; три packs с `geo_intake` (хотя бы optional).

## Dependencies

- SSR-22 Done (G22). Persist columns — SSR-24. Clustering/docs — SSR-25.
