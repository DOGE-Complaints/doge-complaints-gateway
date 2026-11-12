# STORY-GW-SSR-08 — Tallinn civic model as schema pack

## Meta
- **Key:** `STORY-GW-SSR-08-tallinn-civic-schema-pack`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — post-T-wave product (sequence **8**, **перед** refine SSR-06/07)
- **Тип:** implement (pack **data** + tests; civic code path preserved)
- **Parent REQ:** 51 SCHEMA / CL (pack as data); sibling GPT [`REQ-45`](../../../../../GPT%20UI/docs/requirements/REQ-45-semantic-schema-intake-envelope-compatibility.md) — только пример envelope
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [пост-T-wave Шаг 0](./orchestrator-post-t-wave-runbook.md)
- **Зависит от:** SSR-01…05 (T-wave Done)

## Зачем простыми словами

Hardcoded civic-модель Tallinn (ярлыки + 10 `ClusterLens`) остаётся для stories **без** `schema_binding`. Для *новых* bound stories та же семантика должна жить как **pack data** (`tallinn_civic/v1`), потому что pack engine **не видит** labels. Это не «включить civic в pack.json копированием enum».

## Scope / Out of scope

**In:** новый каталог pack (например `schema-packs/tallinn_civic/v1/`); JSON Schema, отражающий измерения, которые сегодня живут в taxonomy/labels/canonical; явная таблица map (ниже) `SignalDimension` / taxonomy axis → dotted path payload; `exact_lenses` + `readiness_policy` как данные (3 knobs, числа **в файле пака**); тесты: pack load + membership по payload; civic tests **без** binding остаются зелёными; пример intake JSON с `schema_binding` (контракт sibling REQ-45) — **в этой стори gateway**, не правка GPT UI.

**Out:** миграция существующих civic rows в pack; смена factory `PromotionGatePolicy` / default civic knobs; новый HTTP path; таблица `story_dimensions` (→ SSR-06 Draft); удаление или расширение `ClusterLens`; IDX/processors (`build_index`/`project` остаются `NotImplementedError`); overlay SPA (sibling spa-16).

**Инвариант:** civic path для stories без binding **не** удалять и не заменять.

## Честная постановка (иначе иллюзия)

| Civic сегодня | Pack engine сегодня |
|---------------|---------------------|
| Сигналы из `infer_signals_from_canonical` / `signals_from_story_labels` ([`enrichment.py:39–106`](../../../../src/core/profile/enrichment.py), [`story_labels.py:156–196`](../../../../src/core/taxonomy/story_labels.py)) | Только `StoryRecord.structured_payload` + dotted `source_fields` ([`pack_engine.py:103–105`](../../../../src/core/schema/pack_engine.py)) |
| `ClusterLens` 10 членов ([`types.py:10–22`](../../../../src/core/cluster/types.py)); `lens_dimension` ([`engine.py:66–79`](../../../../src/core/cluster/engine.py)) | `lens` = строка `lens_id` пака; enum **не** трогать |
| Promote: `complaint`/`system_bug` + factory civic policy ([`gates.py:7–14`](../../../../src/core/promotion/gates.py)) | `readiness_policy` из файла; civic factory **не** менять ([`pack_policy.py`](../../../../src/core/schema/pack_policy.py)) |
| `SERVICE_OBJECT` / `NEED` / `ECOSYSTEM_SIGNAL` в `infer_signals_from_canonical` часто `"unknown"` ([`enrichment.py:79–81`](../../../../src/core/profile/enrichment.py)) | Если эти линзы должны кластеризовать bound stories — значения **в payload**, не надеяться на labels |

`composite_primary_micro` civic берёт **пару** civic_domain + failure_pattern ([`composite_primary_signal_pair`](../../../../src/core/cluster/engine.py) `:82–87`). Pack exact-lens склеивает `source_fields` через `\|` ([`pack_cluster_id`](../../../../src/core/schema/pack_engine.py) `:44–46`). Модель: два dotted path в одном `exact_lenses[]`, не новый член enum.

Geo civic: `geo.normalized_label` ([`enrichment.py:98–105`](../../../../src/core/profile/enrichment.py)). Pack не читает `StoryGeoSnapshot` — geo в payload (например `geo.district`) или линза skip.

## Map: civic axis → payload path (черновик контракта пака)

Имена путей — **этот** pack loader (как `institution.office_id` у `legal_process`). Не invent YAML-диалект сверх [`schema-packs/README.md`](../../../../schema-packs/README.md).

| Civic `SignalDimension` | Taxonomy axis (`story_labels.axis` / [`axes.py`](../../../../src/core/taxonomy/axes.py)) | Civic lens (`ClusterLens` value, **не** копировать в enum) | Предлагаемый dotted path в `structured_payload` |
|-------------------------|------------------------------------------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------|
| `civic_domain` | `topic_domain` | `civic_domain_micro` | `signals.civic_domain` |
| `failure_pattern` | `failure_mode` | `failure_pattern_micro` | `signals.failure_pattern` |
| `civic_weight` | `civic_signal` | `civic_weight_systemic` | `signals.civic_weight` |
| `desired_outcome` | `desired_outcome` | `desired_outcome_local` | `signals.desired_outcome` |
| `affected_group` | `affected_scope` | `affected_group_local` | `signals.affected_group` |
| `geographic_district` | (не axis: geo snapshot) | `geographic_district_micro` | `geo.district` |
| `service_object` | `service_object` | `service_object_micro` | `signals.service_object` |
| `need` | `deep_need` | `deep_need_local` | `signals.need` |
| `ecosystem_signal` | `ecosystem_signal` | `ecosystem_signal_systemic` | `signals.ecosystem_signal` |
| `canonical_type` | envelope `narrative.canonical_type` | (civic promote types, не lens) | `signals.canonical_type` (optional в schema; pack promote **не** требует civic types) |
| pair domain+pattern | — | `composite_primary_micro` | `signals.civic_domain` + `signals.failure_pattern` (два `source_fields`) |

Словари значений civic: [`vocabulary.py`](../../../../src/core/cluster/vocabulary.py). JSON Schema MAY enum’ить те же токены; не обязан дублировать весь vocab, если pack `field_policy` + tests покрывают membership.

Оси taxonomy **без** `SignalDimension` map (`location_context`, `issue_archetype_support`, `governance_signal`, `risk_privacy_safety`, `confidence_state`) — **не** обязательны в T-wave-shape pack; не invent IDX.

## Verified current state

| Fact | Ref |
|------|-----|
| Example packs | `schema-packs/legal_process/v1`, `mobility_observation/v1` |
| Loader keys | [`schema-packs/README.md`](../../../../schema-packs/README.md) |
| `tallinn_civic` on disk | **As-of-Done** `schema-packs/tallinn_civic/v1/` (pkg-000066) |
| Pack не читает labels | [`pack_engine.py:103`](../../../../src/core/schema/pack_engine.py) `payload = story.structured_payload` |
| Civic default policy / factory | [`gates.py:11–14`](../../../../src/core/promotion/gates.py); [`service_factory.py:108–111`](../../../../src/core/infrastructure/service_factory.py) |
| Orchestrator split | [`cluster_orchestrator.py:236–241`](../../../../src/core/application/cluster_orchestrator.py) |
| Cron | [`cluster_cron.py:64`](../../../../src/core/scheduler/cluster_cron.py) `process_all_pending` only |
| `build_index` / `project` | [`runtime.py:62–72`](../../../../src/core/schema/runtime.py) `NotImplementedError` |
| Public Issue card | [`dto.py:26–36`](../../../../src/core/projection/dto.py) без `structured_payload` |
| Операторский мануал | [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md) |

## Стыковка с кодом

Новый pack = данные + JSON Schema + тесты. **Не** новый Python engine. Civic `ClusteringEngine` / `test_clustering_engine.py` не расширять enum.

Bound story с `tallinn_civic`/`v1` идёт pack-веткой. Unbound civic fixtures остаются civic.

GPT: gateway уже парсит `schema_binding` (SSR-03). Instruction pack emit — sibling REQ-45, **не** эта реализация. В AC: пример JSON envelope (ниже). Без GPT UI pack-intake = ручной JSON.

Числа `readiness_policy` — в `pack.json` этого пака, не civic `70`/`2`.

## Пример envelope (gateway; не GPT UI)

```json
{
  "schema_version": "m2.story_intake_envelope.v2",
  "submitter": {
    "external_user_id": "telegram:123456789",
    "identity_issuer": "telegram"
  },
  "narrative": {
    "original_text": "Pothole on the tram line.",
    "language": "en",
    "title": { "en": "Tram pothole" },
    "description": { "en": "Recurring pothole on the tram line." },
    "canonical_type": "complaint"
  },
  "schema_binding": {
    "schema_id": "tallinn_civic",
    "schema_version": "v1",
    "structured_payload": {
      "signals": {
        "civic_domain": "transport",
        "failure_pattern": "broken_infrastructure",
        "civic_weight": "recurring_issue",
        "desired_outcome": "better_maintenance",
        "affected_group": "residents",
        "service_object": "tram_line",
        "need": "unknown",
        "ecosystem_signal": "unknown",
        "canonical_type": "complaint"
      },
      "geo": { "district": "kesklinn" }
    }
  }
}
```

Нарратив (title/description) по-прежнему обязателен. Payload **не** заменяет civic envelope.

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T00** | Pack data | Каталог `tallinn_civic/v1/`: `pack.json` + `payload.schema.json` по loader keys; map таблицы выше в schema properties. | `schema-packs/tallinn_civic/v1/` | Новый YAML-диалект; править `ClusterLens` |
| **T01** | Lenses | `exact_lenses` для civic-эквивалентов (включая composite как два `source_fields`). `lens_id` строки, не enum. | тот же pack | `lens_dimension` dict; civic `_persist_memberships` |
| **T02** | Policy | `readiness_policy` 3 knobs в файле пака; mapper SSR-05 as-is. | `pack.json` | Менять factory civic `PromotionGatePolicy` |
| **T03** | Tests | Load pack; две stories с одинаковым payload path → один `cluster_id`; missing path → skip/policy. | `tests/test_gw_ssr_08_*` | Прогонять bound story через civic engine |
| **T04** | Civic regression | Existing clustering/promotion tests **без** binding зелёные. | `tests/test_clustering_engine.py` etc. | Миграция старых civic rows |
| **T05** | Wire example | Пример envelope в этой стори / мануал; не менять GPT UI. | docs + optional contract test fixture | `GPT UI/` instruction pack |
| **T06** | Gate | Pack load + membership; civic path intact; нет нового HTTP / `story_dimensions`. | | |

## Target / AC

- [x] Pack `tallinn_civic/v1` резолвится loader’ом (`SCHEMA_PACKS_ROOT` / default).
- [x] JSON Schema покрывает map SignalDimension/label keys → dotted paths (таблица выше).
- [x] Exact membership для bound stories с этим pack; `cluster_memberships.lens` = pack `lens_id`.
- [x] Civic stories без binding: тесты зелёные; `ClusterLens` по-прежнему 10 членов.
- [x] Pack promote использует knobs файла пака; factory civic default не изменён.
- [x] Пример `schema_binding` envelope в репозитории gateway (не GPT UI).
- [x] Нет: migrate civic rows; новый HTTP; `story_dimensions`; IDX/processor delivery.

## Точки в коде

- Loader / runtime: [`resolver.py`](../../../../src/core/schema/resolver.py), [`pack_engine.py`](../../../../src/core/schema/pack_engine.py), [`pack_policy.py`](../../../../src/core/schema/pack_policy.py)
- Civic (не ломать): [`types.py`](../../../../src/core/cluster/types.py), [`enrichment.py`](../../../../src/core/profile/enrichment.py), [`gates.py`](../../../../src/core/promotion/gates.py)
- Мануал: [`schema-packs-node-data-model-ru.md`](../../../runtime-docs/manuals/schema-packs-node-data-model-ru.md)

## Dependencies

- SSR-01…05 Done. Refine SSR-06/07 **после** этой стори (INDEX sequence).
- Sibling REQ-45 emit `schema_binding` — иначе прод-intake пака только ручной JSON.
- Sibling spa-16 overlay карточки — payload не на Issue.
- Опционально позже: hosted apply + packs в image — понимание INDEX (SSR-09), **не** эта стори.
