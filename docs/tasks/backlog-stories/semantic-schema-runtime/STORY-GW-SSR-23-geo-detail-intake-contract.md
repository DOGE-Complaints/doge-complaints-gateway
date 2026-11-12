# STORY-GW-SSR-23 — geo_detail wire + pack geo_intake

## Meta
- **Key:** `STORY-GW-SSR-23-geo-detail-intake-contract`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — geo-detail wave (sequence **23**)
- **Тип:** implement (intake parse + pack policy)
- **Parent REQ:** 51 FLOW / SCHEMA; INDEX **D-SSR-10**
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [geo-detail Шаг 0](./orchestrator-geo-detail-runbook.md)
- **Зависит от:** SSR-22

## Зачем простыми словами

Клиент должен уметь слать **стандартизированную** геодетализацию (координаты + адрес до глубины: улица, диапазон домов, несколько домов), не только свободный `location_query`. Обязательность решает **pack** (`geo_intake`), не глобальный хардкод.

## Scope / Out of scope

**In:** объект **`geo_detail`** на envelope (предпочтение: **root sidecar рядом с narrative / schema_binding**, класс изменения как `gpt_signals` — не invent второй binding). Поля (этот loader): optional pair `latitude`/`longitude`; `address` components: country / region / settlement / district / street / `house` **или** `house_range` **или** `houses[]`; `normalized_label`; optional `confidence` / `provider`. Pack блок **`geo_intake`**: `mode` = `optional` \| `require_location_or_detail` \| `require_detail`; `merge` (client detail wins over provider miss); `mirror_to_payload` (bool). Parse в [`contracts.py`](../../../../src/core/intake/contracts.py) (stash+submit share); validate vs pack; merge с `location_query` → resolve. Обновить example packs + payload.schema `geo.*` paths. Документ в [`schema-packs/README.md`](../../../../schema-packs/README.md). Тесты `test_gw_ssr_23_*`: accept detail; invalid → 4xx; optional omit → 202; `require_detail` miss → 4xx.

**Out:** SQL columns street/houses beyond map-to-existing snapshot fields если ещё нет (→24); ClusterLens; GPT UI files.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-23 pkg-000080):** root sidecar `geo_detail` parse (stash+submit); invalid → `IntakeValidationError` | [`contracts.py:151–162`](../../../../src/core/intake/contracts.py), [`:650–654`](../../../../src/core/intake/contracts.py) |
| **As-of-Done:** pack `geo_intake` required; three packs `mode=optional` | [`resolver.py:254`](../../../../src/core/schema/resolver.py), [`:343`](../../../../src/core/schema/resolver.py); `schema-packs/*/v1/pack.json` |
| **As-of-Done:** merge `geo_detail` + `location_query` (fuzzy resolve stays) | [`services.py:220–227`](../../../../src/core/application/services.py), [`:281–286`](../../../../src/core/application/services.py) |
| **As-of-Done:** Tallinn payload `geo.*` (district…houses) | [`payload.schema.json:23–38`](../../../../schema-packs/tallinn_civic/v1/payload.schema.json) |
| **Historical (pre-SSR-23):** Wire geo = `narrative.location_query` only | [`contracts.py:43`](../../../../src/core/intake/contracts.py) pre-P3 |
| **Historical (pre-SSR-23):** Tallinn payload `geo.district` only | [`payload.schema.json`](../../../../schema-packs/tallinn_civic/v1/payload.schema.json) pre-P3 |
| Snapshot без street/houses (persist →24) | [`domain/contracts.py:28–40`](../../../../src/core/domain/contracts.py) |

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

- SSR-22. Persist columns — SSR-24. Clustering/docs — SSR-25.
