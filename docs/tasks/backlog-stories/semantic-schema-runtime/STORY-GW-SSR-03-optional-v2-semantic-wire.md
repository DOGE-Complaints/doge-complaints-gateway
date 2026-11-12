# STORY-GW-SSR-03 — Optional `schema_binding` on m2.story_intake_envelope.v2

## Meta
- **Key:** `STORY-GW-SSR-03-optional-v2-semantic-wire`
- **Пакет:** [`semantic-schema-runtime/`](./INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — T-wave wire (sequence **3**)
- **Тип:** implement (parser once)
- **Parent REQ:** 51 §2 FLOW-003, §4.3, §5 AC-10/15
- **Decision:** INDEX **D-SSR-1**
- **Siblings:** GPT [`REQ-45-…`](../../../../GPT%20UI/docs/requirements/REQ-45-semantic-schema-intake-envelope-compatibility.md) MAY emit; this story parses
- **Skill declared:** python-pro
- **Git:** только `semantic-schema-runtime` — [runbook Шаг 0](./orchestrator-t-wave-runbook.md)
- **Зависит от:** SSR-01, SSR-02

## Зачем простыми словами

Один optional sidecar на существующем v2 — как `gpt_signals`. Внутри binding + payload. Нет блока — civic intake как сейчас. Блок есть — не silent-drop.

## Scope / Out of scope

**In:** parser extended **once**. Required root `schema_version` = `m2.story_intake_envelope.v2`. Optional object **`schema_binding`** with **only** parent persist tokens:

```text
schema_id
schema_version          # semantic model (не envelope)
profile_id              # optional
profile_version         # optional
structured_payload
```

`envelope_version` persist ← корневой envelope id (не дублировать во внутреннем объекте — иначе коллизия с семантическим `schema_version`). `payload_hash` не на проводе. Absence of `schema_binding` = LegacyM2 success. Class of change = [`gpt_signals` sidecar](../../../../src/core/intake/contracts.py).

**Out:** new envelope enum; new HTTP intake path; extra OpenAPI names beyond `schema_binding` + parent token list; identity (**D-SSR-3**); GPT instruction files.

### Почему один объект (D-SSR-1)

Корневой `schema_version` уже занят envelope id. Плоские persist-токены на корне дали бы второе `schema_version`. Один sidecar: один `if key in payload` (как `gpt_signals`), внутренний `schema_version` = модель, рантаймы (local/remote) видят тот же binding record.

## Verified current state

### As-of-Done (SSR-03 pkg-000063)

| Fact | Ref |
|------|-----|
| Required envelope | [`contracts.py:19`](../../../../src/core/intake/contracts.py) `INTAKE_SCHEMA_VERSION` |
| Parser | [`_parse_schema_binding_block`](../../../../src/core/intake/contracts.py) [`:227–265`](../../../../src/core/intake/contracts.py); `SCHEMA_BINDING_ALLOWED_KEYS` [`:92–100`](../../../../src/core/intake/contracts.py) |
| Fields | `StoryDraftStashRequest.schema_binding` [`:122`](../../../../src/core/intake/contracts.py); `StoryIntakeRequest.schema_binding` [`:137`](../../../../src/core/intake/contracts.py) |
| Envelope body 7-tuple | [`_parse_story_envelope_body`](../../../../src/core/intake/contracts.py) return [`:484–492`](../../../../src/core/intake/contracts.py) includes `schema_binding`; sidecar parse [`:480–482`](../../../../src/core/intake/contracts.py) |
| Submit + stash | [`parse_story_intake_request`](../../../../src/core/intake/contracts.py) [`:495`](../../../../src/core/intake/contracts.py); [`parse_story_draft_stash_request`](../../../../src/core/intake/contracts.py) [`:529`](../../../../src/core/intake/contracts.py); stash→submit copies binding [`:571–585`](../../../../src/core/intake/contracts.py) |
| Optional sidecar `gpt_signals` | [`contracts.py:474–478`](../../../../src/core/intake/contracts.py) |
| Civic narrative still required | `narrative.original_text` [`:328–330`](../../../../src/core/intake/contracts.py); i18n title+description [`:343–353`](../../../../src/core/intake/contracts.py); `canonical_type` optional [`:371–376`](../../../../src/core/intake/contracts.py) |
| Runtime before save | [`services.py:246–262`](../../../../src/core/application/services.py) `LocalSchemaRuntime.validate`; `SchemaRuntimeError` → `IntakeValidationError` |
| Intake persist map | envelope → `StoryRecord.schema_version` [`services.py:271`](../../../../src/core/application/services.py); inner → `schema_id` / `bound_schema_version` / profiles / payload + hash [`:315–320`](../../../../src/core/application/services.py) |
| DI | [`service_factory.py:85`](../../../../src/core/infrastructure/service_factory.py) `schema_runtime=LocalSchemaRuntime()` |

### Historical (pre-P3)

| Fact | Ref |
|------|-----|
| `schema_binding` parsed | **Not found** |
| Envelope body 6-tuple | [`_parse_story_envelope_body`](../../../../src/core/intake/contracts.py) (pre-7th `SchemaBinding` return) |
| Intake persist | `schema_version=request.schema_version` only (no inner binding map) |
| DI | [`service_factory.py`](../../../../src/core/infrastructure/service_factory.py) / [`dependencies.py`](../../../../src/core/api/dependencies.py) — SchemaRuntime ещё нет |

## Стыковка с кодом

Parser **обязан** остаться civic-envelope: отсутствие `schema_binding` = текущий путь (`gpt_signals` pattern [`:397–401`](../../../../src/core/intake/contracts.py)).

При наличии блока: validate через SSR-01 **до** `save_story`; заполнить SSR-02 поля; `payload_hash` посчитать на сервере. Невалидный payload → `IntakeValidationError` (как остальные intake errors), не silent drop.

**Не** ослаблять обязательный `narrative` (AC «otherwise valid v2»). Pack domain живёт в `structured_payload`, не вместо title/description.

Stash: тот же envelope body — иначе GPT stash потеряет binding до submit.

OpenAPI/API_REFERENCE — optional T после path; не invent новых HTTP path.

Identity handlers ([`handlers.py:221`](../../../../src/core/api/handlers.py)) не менять.

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T01** | Parse | Optional `schema_binding` object; неизвестные inner keys → error; inner `schema_version` ≠ envelope. | [`contracts.py`](../../../../src/core/intake/contracts.py) `_parse_story_envelope_body` | Плоские root `schema_id` |
| **T02** | Dataclass | Поле на `StoryIntakeRequest` ([`:106`](../../../../src/core/intake/contracts.py)) + `StoryDraftStashRequest` ([`:93`](../../../../src/core/intake/contracts.py)). | same | |
| **T03** | Runtime hook | Если binding: `LocalSchemaRuntime.validate`; ошибки RUNTIME-005 → 4xx envelope. | [`services.py`](../../../../src/core/application/services.py) intake; factory wire | Identity policy_context |
| **T04** | Persist map | envelope → `StoryRecord.schema_version`; inner → `schema_id` / `bound_schema_version` / profiles / payload + hash. | [`services.py:236`](../../../../src/core/application/services.py) | Client `payload_hash` |
| **T05** | Absent path | Нет ключа / пустой объект: civic save как сейчас; regression intake tests. | tests | |
| **T06** | Docs | Optional object на **существующем** intake/stash schema. | [`openapi.yaml`](../../../../docs/runtime-docs/api-reference/openapi.yaml), [`API_REFERENCE.md`](../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) | Новый GET filter / новый HTTP path |
| **T07** | Tests | present→persist; absent→legacy; invalid payload rejected; stash round-trip. Civic suite green. | `tests/test_gw_ssr_03_*` | |
| **T08** | Gate | AC-015/COMPAT-001. | | |

## Target / AC

- [x] AC-GW-REQ3-15 / AC-015: `schema_binding` present → bind + validate `structured_payload`; absent → civic intake succeeds.
- [x] AC-GW-REQ3-10 / COMPAT-001: do not remove `m2.story_intake_envelope.v2`.
- [x] FLOW-003: named tokens persisted; silently ignoring = non-compliant.
- [x] Tests §29: optional parse vs ignore-absent; civic intake green.

## Точки в коде

- `parse_story_intake_request` / `_parse_story_envelope_body` ([`contracts.py:413`](../../../../src/core/intake/contracts.py), [`:397`](../../../../src/core/intake/contracts.py))
- Pattern: `gpt_signals` — **не** копировать GPT field names в schema tokens.

## Dependencies

- SSR-01 validate; SSR-02 persist targets.
- GPT MAY emit after this named contract — не блокер parser.
