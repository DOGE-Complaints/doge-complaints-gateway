# STORY-GW-SSR-19 — Node clustering pack contract

## Meta
- **Key:** `STORY-GW-SSR-19-node-clustering-pack-contract`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — cluster-knobs wave (sequence **19**)
- **Тип:** implement (pack contract + loader + pack data; первый слой)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-19-node-clustering-pack-contract.md)
- **Parent REQ:** 51 SCHEMA / CL; INDEX **D-SSR-9**
- **Decision:** INDEX **D-SSR-9**
- **decision_ref:** backlog SSR-19 + INDEX **D-SSR-9**
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-18](../STORY-GW-SSR-18-cluster-active-schema/STORY-GW-SSR-18-cluster-active-schema.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000076-20260830-gw-ssr-19-node-clustering-pack-contract.yaml`](../../../../gateway-active-packages/pkg-000076-20260830-gw-ssr-19-node-clustering-pack-contract.yaml)
- **Git:** только `semantic-schema-runtime` — [cluster-knobs Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-cluster-knobs-runbook.md)
- **Зависит от:** SSR-18 ([pipeline](../STORY-GW-SSR-18-cluster-active-schema/STORY-GW-SSR-18-cluster-active-schema.md))
- **Scaffolded:** 2026-08-30T19:16:21Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 SCHEMA / CL | INDEX **D-SSR-9** |
| Decision | INDEX **D-SSR-9** | civic knobs → `node_clustering.civic` в активном pack.json |

- **Разблокирует:** G19 → SSR-20 (не этот pkg).
- **Не reopen:** SSR-01…05 / 08–18 product; T-wave G3 historical
- **Не трогаем:** factory wire (→20); GPT UI; `ClusterLens`; `GET /schema-active`; cron in pack; bullrun §«Актуальная точка»

## Nested tasks (pkg-000076)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-19-t00-contract-readme`](./task-gw-ssr-19-t00-contract-readme/README.md) |
| T01 | [`task-gw-ssr-19-t01-types-schema-context`](./task-gw-ssr-19-t01-types-schema-context/README.md) |
| T02 | [`task-gw-ssr-19-t02-loader-parse-validate`](./task-gw-ssr-19-t02-loader-parse-validate/README.md) |
| T03 | [`task-gw-ssr-19-t03-pack-data-defaults`](./task-gw-ssr-19-t03-pack-data-defaults/README.md) |
| T04 | [`task-gw-ssr-19-t04-tests`](./task-gw-ssr-19-t04-tests/README.md) |
| T05 | [`task-gw-ssr-19-t05-story-acceptance-gate`](./task-gw-ssr-19-t05-story-acceptance-gate/README.md) |
| T06 | [`task-gw-ssr-19-t06-audit-g1-as-of-done-ssot`](./task-gw-ssr-19-t06-audit-g1-as-of-done-ssot/README.md) |

## Зачем простыми словами

После D-SSR-8 рабочая модель ноды — активный pack. Но пороги и линзы **civic** `ClusterLens` всё ещё в `.env` (`CLUSTER_*`), а pack exact уже в `exact_lenses`. Кастомизация ноды должна жить в **одном** месте: `pack.json`. Эта стори — контракт и loader; wiring factory — SSR-20.

## Scope / Out of scope

**In:** блок **`node_clustering.civic`** в pack.json (этот loader only, SCHEMA-005). Поля: `active_lenses`, `primary_lens`, `min_size`, `min_size_by_lens`, `readiness_threshold`, `signal_source`, `id_algorithm`, `geo_filter`, `geo_scope` (optional/`null` как сейчас `CLUSTER_GEO_SCOPE`), `tie_breaker`, `type_resolution`. Dataclass на [`SchemaContext`](../../../../../../src/core/schema/contracts.py); parse в [`resolver.py`](../../../../../../src/core/schema/resolver.py). Валидация зеркалит парсеры [`schema.py`](../../../../../../src/core/config/schema.py) (`primary ∈ active`, known lens ids, ranges 1–100). Заполнить блок у `tallinn_civic/v1` (`geo_scope`: `settlement:tallinn`), `legal_process/v1`, `mobility_observation/v1` — значения из **текущих** EnvSpec defaults / conftest (не invent новые пороги). Документ ключа в [`schema-packs/README.md`](../../../../../../schema-packs/README.md). Тесты `tests/test_gw_ssr_19_*`: load ok; missing `node_clustering` → loader error; invalid primary → error; `ClusterLens` enum не расширен.

**Out:** wiring `service_factory` / handlers (→20); удаление `CLUSTER_*` из AppConfig (→20); глубокий мануал ноды (→21); смена `exact_lenses` семантики; HTTP; GPT UI.

## Verified current state

| Fact | Ref |
|------|-----|
| **As-of-Done (SSR-19 pkg-000076):** `node_clustering.civic` required parse → `SchemaContext.node_clustering`; missing/invalid → `UnsupportedVersionError` | [`resolver.py:82–85,310`](../../../../../../src/core/schema/resolver.py); [`contracts.py:51–85`](../../../../../../src/core/schema/contracts.py) |
| **As-of-Done:** три example pack из EnvSpec defaults; tallinn `geo_scope=settlement:tallinn`; legal/mobility `null` | `schema-packs/{tallinn_civic,legal_process,mobility_observation}/v1/pack.json` |
| **As-of-Done:** factory / AppConfig civic knobs **ещё** `CLUSTER_*` (wire →20); `ClusterLens` = 10 | [`service_factory.py:93–113`](../../../../../../src/core/infrastructure/service_factory.py); [`types.py:10–22`](../../../../../../src/core/cluster/types.py) |
| Pack exact knobs уже в файле | [`tallinn_civic/v1/pack.json`](../../../../../../schema-packs/tallinn_civic/v1/pack.json) `exact_lenses[].min_size` + `readiness_policy` |
| Defaults conftest (test overlay, не pack SSOT) | [`conftest.py:60–74`](../../../../../../tests/conftest.py) — 10 lenses; `MIN_SIZE_BY_LENS` без `composite_primary_micro=8` |
| **Historical (pre-SSR-19):** Нет `node_clustering` в loader — `exact_lenses`, `dual_civic_lenses`, `card_fields`; civic knobs только AppConfig/env | same paths pre-P3 |

## Стыковка

**Два контура (не смешивать):**
- `exact_lenses[]` — pack exact engine + pack promote.
- `node_clustering.civic` — `ClusteringEngine` / civic promote / dual + unbound legacy.

Не invent override env «поверх pack» в этой стори. Boot fail-fast на missing block — в loader; `ConfigError` на старте процесса — SSR-20 (когда factory обязан читать pack).

## Подзадачи

| ID | Слой | Задача | Не делать |
|----|------|--------|-----------|
| **T00** | Contract | Зафиксировать shape `node_clustering.civic` в README | Frozen YAML dialect invent |
| **T01** | Types | Dataclass(es) на SchemaContext | Новые `ClusterLens` members |
| **T02** | Loader | Parse + validate; missing/invalid → UnsupportedVersionError (или loader error as-of SSR-01) | Silent default без блока |
| **T03** | Pack data | Три example pack с блоком из текущих defaults | Новые пороги «на глаз» |
| **T04** | Tests | `test_gw_ssr_19_*` load / missing / invalid primary | Factory wire (→20) |
| **T05** | Gate | load ok; ClusterLens=10; README ключ | |
| **T06** | Docs | As-of-Done vs Historical §Verified (G1) | Factory wire; ClusterLens |

## Target / AC

- [x] `node_clustering.civic` парсится в SchemaContext.
- [x] Нет блока / битый primary → loader error.
- [x] Три example pack на диске с заполненным блоком (tallinn: `geo_scope=settlement:tallinn`).
- [x] `schema-packs/README.md` документирует ключ.
- [x] `ClusterLens` members ровно baseline (10).
- [x] Factory/AppConfig **не** переведены на pack в этой стори.

## Dependencies

- SSR-18 Done. Runtime wire — SSR-20. Docs — SSR-21.
