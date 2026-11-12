# STORY-GW-SSR-01 — SchemaRuntime local-first + SCHEMA-005 pack load

## Meta
- **Key:** `STORY-GW-SSR-01-schema-runtime-pack-load`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits) — P3 Execute PASS 2026-08-28T13:18:56Z pkg-000061
- **Приоритет:** 🟠 MED — T-wave foundation (sequence **1**)
- **Тип:** implement (in-process runtime + pack loader)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../../../requirements/51-semantic-schema-runtime.md) §2 T-wave, §4.1–4.2
- **Parent product:** [`REQ3-…`](../../../../../../../docs/requirements%20backlog/REQ3-Semantic-Schema-Runtime-and-Node-Specific-Data-Processing.md) RUNTIME-001…005, SCHEMA-005, SEC-001/002, WAVE-001
- **Siblings in package:** SSR-02 persist; SSR-03 wire; SSR-04 lens (backlog; not this pkg)
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-ES-03](../../../../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000061-20260828-gw-ssr-01-schema-runtime-pack-load.yaml`](../../../../gateway-active-packages/pkg-000061-20260828-gw-ssr-01-schema-runtime-pack-load.yaml)
- **Git:** исполнять только на `semantic-schema-runtime` — [runbook Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md)
- **decision_ref:** backlog SSR-01 + INDEX **D-SSR-4** / **D-SSR-3** + REQ 51 §2/§4.1–4.2 + parent REQ3 RUNTIME/SCHEMA-005/SEC

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 §1 Goal, §2 runtime, §4.1–4.2, §5 AC-01/04/13 | |
| Parent | RUNTIME-001…005; SCHEMA-005; AC-001/004/013; SEC-001/002; COMPAT-001 adapter name | |
| Decision | INDEX **D-SSR-4** pack/runtime split | |

- **Зависит от:** —
- **Разблокирует:** SSR-02, SSR-03, SSR-04
- **Не reopen:** civic `ClusterLens` enum; `GET /tallinn/issues`
- **Не трогаем:** identity-service / claim keys (**D-SSR-3**)

## Nested tasks (pkg-000061)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-01-t00-pack-layout-manifest`](./task-gw-ssr-01-t00-pack-layout-manifest/README.md) |
| T01 | [`task-gw-ssr-01-t01-jsonschema-dependency`](./task-gw-ssr-01-t01-jsonschema-dependency/README.md) |
| T02 | [`task-gw-ssr-01-t02-schema-runtime-protocol`](./task-gw-ssr-01-t02-schema-runtime-protocol/README.md) |
| T03 | [`task-gw-ssr-01-t03-pack-resolver`](./task-gw-ssr-01-t03-pack-resolver/README.md) |
| T04 | [`task-gw-ssr-01-t04-jsonschema-validate`](./task-gw-ssr-01-t04-jsonschema-validate/README.md) |
| T05 | [`task-gw-ssr-01-t05-legacy-m2-compat-type`](./task-gw-ssr-01-t05-legacy-m2-compat-type/README.md) |
| T06 | [`task-gw-ssr-01-t06-unit-tests`](./task-gw-ssr-01-t06-unit-tests/README.md) |
| T07 | [`task-gw-ssr-01-t07-story-acceptance-gate`](./task-gw-ssr-01-t07-story-acceptance-gate/README.md) |
| T08 | [`task-gw-ssr-01-t08-audit-g1-as-of-done-ssot`](./task-gw-ssr-01-t08-audit-g1-as-of-done-ssot/README.md) — P6 `run_mode=gw_ssr_01_audit_followup` |
| T09 | [`task-gw-ssr-01-t09-audit-g2-readme-dod-checkboxes`](./task-gw-ssr-01-t09-audit-g2-readme-dod-checkboxes/README.md) |
| T10 | [`task-gw-ssr-01-t10-audit-g3-nesting-depth-test`](./task-gw-ssr-01-t10-audit-g3-nesting-depth-test/README.md) |

## Зачем простыми словами

Новая node-модель = файл пака + рантайм, который его грузит и валидирует. Не плодить колонки и ветки parser на каждое поле.

## Scope / Out of scope

**In:** `SchemaRuntime` abstraction (parent Protocol — signatures MAY differ); код в `src/core/schema/`; загрузка SCHEMA-005 pack из `schema-packs/<schema_id>/<schema_version>/` по `(schema_id, schema_version)`; configurable packs root (позже Local → Remote без смены id пака); validate/reject без silent coerce (RUNTIME-005, AC-004); schema = data not code (SEC-001); resource limits (SEC-002); conceptual `LegacyM2StorySchema` как тип/путь (COMPAT-001); v2 не удалять.

**Out:** persist columns (→ SSR-02); `schema_binding` parser (→ SSR-03); cluster membership (→ SSR-04); promotion (→ SSR-05); IDX/QRY HTTP; processors; WASM; federation; invent pack YAML key names; invent HTTP paths; identity claims.

## Verified current state (As-of-Done, pkg-000061)

| Fact | Ref |
|------|-----|
| Intake envelope constant | [`contracts.py:19`](../../../../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"` |
| Parser | [`contracts.py:413`](../../../../../../src/core/intake/contracts.py) `parse_story_intake_request` |
| `src/core/schema/` | **Exists** — 8 modules (`contracts.py`, `runtime.py`, `resolver.py`, `validator.py`, `field_policy.py`, `legacy.py`, `errors.py`, `__init__.py`) |
| `SchemaRuntime` / `LocalSchemaRuntime` | [`contracts.py:61`](../../../../../../src/core/schema/contracts.py) Protocol; [`runtime.py:18`](../../../../../../src/core/schema/runtime.py) |
| Packs on disk | `schema-packs/legal_process/v1`, `schema-packs/mobility_observation/v1`, [`schema-packs/README.md`](../../../../../../schema-packs/README.md) |
| `jsonschema` в deps | `jsonschema>=4.18.0` — [`pyproject.toml:16`](../../../../../../pyproject.toml); [`requirements.txt:5`](../../../../../../requirements.txt) |
| `ClusterLens` hard-coded | [`types.py:10–22`](../../../../../../src/core/cluster/types.py) — **unchanged** (SSR-01 out of civic enum) |
| Civic engine enum-keyed | [`engine.py:66–79`](../../../../../../src/core/cluster/engine.py) `lens_dimension` mapping |
| Gate | PASS 2026-08-28T13:18:56Z · pkg-000061 |

## Verified current state — Historical (pre-P3)

> **Historical.** Снимок **до** SSR-01 P3. Не текущее runtime-состояние.

| Fact | Ref (as of pre-P3) |
|------|-----|
| Intake envelope constant | [`contracts.py:19`](../../../../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION = "m2.story_intake_envelope.v2"` |
| Parser | [`contracts.py:413`](../../../../../../src/core/intake/contracts.py) `parse_story_intake_request` |
| `src/core/schema/` | **Not found** (Glob) |
| `SchemaRuntime` in `src/` | **Not found** (Grep) |
| `ClusterLens` hard-coded | [`types.py:10–22`](../../../../../../src/core/cluster/types.py) |
| `jsonschema` в deps | **Not found** — [`pyproject.toml:11–16`](../../../../../../pyproject.toml) |
| Civic engine enum-keyed | [`engine.py:66–79`](../../../../../../src/core/cluster/engine.py) `lens_dimension` mapping |

## Стыковка с кодом

Эта стори **не** вшивается в intake/clustering. Точка стыка позже: SSR-03 вызывает `validate`; SSR-04 читает lens **block** из уже загруженного pack. Не менять `parse_story_intake_request` и не трогать `ClusteringEngine` здесь.

T00 фиксирует **gateway-internal pack on-disk contract** (loader-only). Parent SCHEMA-003 YAML keys не frozen — это не invent product OpenAPI, это контракт одного loader (parent SCHEMA-005: syntax implementation-specific for a single gateway loader).

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T00** | Contract | Зафиксировать pack layout: `schema-packs/<schema_id>/<schema_version>/` + манифест, который loader умеет (JSON Schema file + representable field-policy states + ≥1 exact-lens block **shape** как CL-001 example). Example lens block **обязан** нести CL-003 conceptual tokens, которые SSR-05 мапит на существующий `PromotionGatePolicy` (только 3 knobs: `min_readiness_score`, `min_stories` ← `min_size`, `require_actionable_canonical_type=false` для pack). Числа — **в файле example pack**, не копировать civic `70`/`2` в Python default. Имена ключей манифеста — **только этот loader**, таблица в README. | new `schema-packs/README.md` + example pack ids `legal_process.v1` / `mobility_observation.v1` (parent §29 Integration) | Frozen «универсальный YAML диалект»; domain fields в parser; второй диалект readiness в SSR-05 |
| **T01** | Dep | Добавить `jsonschema` в `pyproject.toml` + `requirements.txt`. | [`pyproject.toml`](../../../../../../pyproject.toml) | Самописный validator «как JSON Schema» |
| **T02** | Runtime | `SchemaRuntime` Protocol + `LocalSchemaRuntime`: `resolve` / `validate` / `canonicalize` / `enforce_policy` (policy_context **без** identity claims). `build_index` / `project` — stub `NotImplemented` или no-op с явным later (SSR-06/07), не притворяться working IDX/PROC. | new `src/core/schema/` | Вызов из intake |
| **T03** | Loader | Resolver: packs root из config/env default `schema-packs/`; unknown schema / unsupported version → typed error (RUNTIME-005). | `src/core/schema/resolver.py` | Hardcode path только без config hook |
| **T04** | Validate | JSON Schema validate `structured_payload`; no silent coerce; forbidden/missing/type errors. SEC-002: reject cyclic `$ref` / oversized payload (лимиты в коде, числа — константы модуля, не invent product threshold в REQ). | `validator.py` | `eval` / import pack as Python |
| **T05** | Compat type | Тип/адаптер `LegacyM2StorySchema` (маркер civic envelope). Без удаления v2. | `src/core/schema/` | Менять `INTAKE_SCHEMA_VERSION` |
| **T06** | Tests | Unit: resolve, validate pass/fail, two packs same runtime, no code exec from pack bytes. Civic parser tests **не** трогать (ещё нет wire). | `tests/test_gw_ssr_01_*` | Менять `test_clustering_engine.py` |
| **T07** | Gate | Story acceptance: packs load; AC-004; SEC-001; `ClusterLens` enum **не** изменён (`rg ClusterLens src/core/cluster/types.py`). | gate md | |

## Target / AC

- [x] AC-GW-REQ3-01 / parent AC-001+013: SCHEMA-005 pack loads; valid payload without new domain field on `StoryRecord` / per-field parser / `stories` column / clustering engine change for that pack’s exact lens **declaration**. Parser-once FLOW-003 = **SSR-03**.
- [x] AC-GW-REQ3-04 / AC-004: violating payload rejected; no required value invented; distinguish at least unknown schema / unsupported version / invalid type / missing required / forbidden / invalid constraint / policy violation / profile incompatibility (RUNTIME-005).
- [x] SEC-001: pack YAML/JSON cannot execute arbitrary Python/JS/shell.
- [x] SEC-002: limits against abusive recursion/nesting/oversized payload / cyclic `$ref` (as applicable).
- [x] Conceptual `LegacyM2StorySchema` named in code/docs (COMPAT-001).
- [x] Packs live under `schema-packs/` (data); runtime under `src/core/schema/` (code) — **D-SSR-4**.
- [x] Tests §29 Unit that apply: schema resolution, JSON Schema validation, canonicalization, field-policy as represented in pack.

## Точки в коде

- New: `src/core/schema/` (parent RUNTIME-002 example).
- Packs: `doge-complaints-gateway/schema-packs/` — сейчас нет; создать при execute.
- Do not add domain fields to `StoryRecord` ([`contracts.py:44–46`](../../../../../../src/core/domain/contracts.py)).
- Do not add a `ClusterLens` member ([`types.py:10–22`](../../../../../../src/core/cluster/types.py)).
- Do not edit [`engine.py`](../../../../../../src/core/cluster/engine.py) / [`cluster_orchestrator.py`](../../../../../../src/core/application/cluster_orchestrator.py) в этой стори.

## Dependencies

- None. CL-001 YAML в parent — example **shape**, не frozen keys.
