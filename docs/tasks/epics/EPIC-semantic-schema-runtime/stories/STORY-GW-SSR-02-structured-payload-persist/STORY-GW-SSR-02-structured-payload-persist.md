# STORY-GW-SSR-02 — Schema/profile binding + structured_payload persist

## Meta
- **Key:** `STORY-GW-SSR-02-structured-payload-persist`
- **Parent Epic:** [`../../../EPIC-semantic-schema-runtime.md`](../../../EPIC-semantic-schema-runtime.md)
- **Пакет:** [`semantic-schema-runtime/`](../../../../backlog-stories/semantic-schema-runtime/INDEX.md)
- **Status:** 🔵 Done (Awaiting Commits)
- **Приоритет:** 🟠 MED — T-wave persist (sequence **2**)
- **Тип:** implement (domain + SQL/sqlite persist)
- **source:** [`../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md`](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-02-structured-payload-persist.md)
- **Parent REQ:** [`51-semantic-schema-runtime.md`](../../../../../requirements/51-semantic-schema-runtime.md) §2 persist, §4.3–4.4, §5 AC-02/03
- **Siblings in package:** [SSR-01](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-01-schema-runtime-pack-load.md) Done pkg-000061; [SSR-03](../../../../backlog-stories/semantic-schema-runtime/STORY-GW-SSR-03-optional-v2-semantic-wire.md) wire (backlog; not this pkg)
- **Skill declared:** python-pro
- **Etalon структуры:** [STORY-GW-SSR-01](../STORY-GW-SSR-01-schema-runtime-pack-load/STORY-GW-SSR-01-schema-runtime-pack-load.md)
- **Operative queue:** [`../../../../gateway-active-packages/pkg-000062-20260828-gw-ssr-02-structured-payload-persist.yaml`](../../../../gateway-active-packages/pkg-000062-20260828-gw-ssr-02-structured-payload-persist.yaml)
- **Git:** исполнять только на `semantic-schema-runtime` — [runbook Шаг 0](../../../../backlog-stories/semantic-schema-runtime/orchestrator-t-wave-runbook.md)
- **decision_ref:** backlog SSR-02 + INDEX **D-SSR-5** / **D-SSR-3** + persist map `bound_schema_version`
- **Scaffolded:** 2026-08-28T13:38:52Z

### Трассировка
| Слой | Документ | §§ |
|------|----------|-----|
| Child REQ | 51 §2 persist, §4.3–4.4, §5 AC-02/03 | |
| Parent | DATA-001…004; PR-002; AC-002/003; COMPAT-002 | |
| Decision | INDEX **D-SSR-5** payload_hash; persist map `bound_schema_version` | |

- **Зависит от:** SSR-01 (Done pkg-000061)
- **Разблокирует:** SSR-03, SSR-04
- **Не reopen:** civic `ClusterLens` enum; вторая колонка `schema_version`; `schema_binding` parser
- **Не трогаем:** identity-service / claim keys (**D-SSR-3**)

## Nested tasks (pkg-000062)

| ID | Folder |
|----|--------|
| T00 | [`task-gw-ssr-02-t00-parent-persist-field-map`](./task-gw-ssr-02-t00-parent-persist-field-map/README.md) |
| T01 | [`task-gw-ssr-02-t01-story-record-optional-fields`](./task-gw-ssr-02-t01-story-record-optional-fields/README.md) |
| T02 | [`task-gw-ssr-02-t02-payload-hash`](./task-gw-ssr-02-t02-payload-hash/README.md) |
| T03 | [`task-gw-ssr-02-t03-sqlite-alter-upsert`](./task-gw-ssr-02-t03-sqlite-alter-upsert/README.md) |
| T04 | [`task-gw-ssr-02-t04-lifecycle-copy-replace`](./task-gw-ssr-02-t04-lifecycle-copy-replace/README.md) |
| T05 | [`task-gw-ssr-02-t05-supabase-row-select`](./task-gw-ssr-02-t05-supabase-row-select/README.md) |
| T06 | [`task-gw-ssr-02-t06-migration-bootstrap-alter`](./task-gw-ssr-02-t06-migration-bootstrap-alter/README.md) |
| T07 | [`task-gw-ssr-02-t07-unit-tests`](./task-gw-ssr-02-t07-unit-tests/README.md) |
| T08 | [`task-gw-ssr-02-t08-story-acceptance-gate`](./task-gw-ssr-02-t08-story-acceptance-gate/README.md) |
| T09 | [`task-gw-ssr-02-t09-audit-g1-as-of-done-ssot`](./task-gw-ssr-02-t09-audit-g1-as-of-done-ssot/README.md) — P6 `run_mode=gw_ssr_02_audit_followup` |
| T10 | [`task-gw-ssr-02-t10-audit-g2-sqlite-save-return-hash`](./task-gw-ssr-02-t10-audit-g2-sqlite-save-return-hash/README.md) — P6 `run_mode=gw_ssr_02_audit_followup` |

## Зачем простыми словами

Две node-модели на одной core DB: binding-поля + JSON `structured_payload`, плюс хеш канонического payload. Без колонок `stories` под domain fields.

## Scope / Out of scope

**In:** persist tokens parent PR-002 / DATA-003 / DATA-002: `envelope_version`, `schema_id`, `schema_version` (semantic), `profile_id`, `profile_version` (nullable), `structured_payload`, **`payload_hash` (D-SSR-5, DATA-004 — делаем)**. Same logical core DB (DATA-001, AC-002). Exact version traceability (AC-003). JSONB round-trip (§29 Repository). Civic текущий `StoryRecord.schema_version` (envelope) не сломать (COMPAT-002 order 3–4).

**Out:** invent names beyond that list; `story_dimensions` (→ SSR-06 Draft); node-specific `stories` domain columns; `schema_binding` wire (→ SSR-03); QRY HTTP; identity (**D-SSR-3**). Client-supplied `payload_hash` на intake — **не** принимать как авторитет (считает runtime после validate).

## Verified current state

| Fact | Ref |
|------|-----|
| `StoryRecord.schema_version` single field | [`contracts.py:46`](../../../../../../src/core/domain/contracts.py) |
| Opaque author keys | [`contracts.py:48–49`](../../../../../../src/core/domain/contracts.py) |
| `stories.schema_version` | [`20260423_1500_init_db_wave.sql:8`](../../../../../../supabase/migrations/20260423_1500_init_db_wave.sql) |
| `structured_payload` / `payload_hash` / `schema_id` in src+sql | **P3:** domain + sqlite ALTER/upsert + supabase SELECT/row + migration `20260828_1400_*` + bootstrap ALTER |
| `envelope_version` column | **Not found** (envelope stays `schema_version`) |
| Lifecycle reconstruct | **P3:** `dataclasses.replace` in `advance_story_readiness` (`services.py`) |
| sqlite INSERT column list | [`db_sqlite.py:537–548`](../../../../../../src/core/infrastructure/db_sqlite.py) |
| supabase save row dict | [`db_supabase.py:439–462`](../../../../../../src/core/infrastructure/db_supabase.py) |
| sqlite ALTER pattern (existing DBs) | [`db_sqlite.py:306–335`](../../../../../../src/core/infrastructure/db_sqlite.py) |
| In-memory | [`repositories.py:56–70`](../../../../../../src/core/infrastructure/repositories.py) stores whole dataclass |

## Стыковка с кодом

**Коллизия имён (решаемая, не стоп):** parent DATA-003 `schema_version` = semantic model; существующий `StoryRecord.schema_version` / колонка `stories.schema_version` = envelope ([`contracts.py:46`](../../../../../../src/core/domain/contracts.py), intake [`services.py:238`](../../../../../../src/core/application/services.py)). **Не** переименовывать колонку envelope. Semantic version → новое поле/колонка `bound_schema_version` (Python+SQL). Persist map:

| Parent token | Код / SQL |
|--------------|-----------|
| envelope_version | существующий `schema_version` |
| schema_id | new `schema_id` nullable |
| schema_version (semantic) | new `bound_schema_version` nullable |
| profile_id / profile_version | new nullable |
| structured_payload | new JSON/JSONB nullable |
| payload_hash | new nullable TEXT |

`envelope_version` отдельной колонкой **не** плодить (дубль envelope).

**Silent-wipe риск (закрыт P3):** `advance_story_readiness` теперь `dataclasses.replace(current, lifecycle_status=…, updated_at=…)`.

Три адаптера: in-memory (авто, если dataclass + constructors ок), sqlite (ALTER + SELECT + INSERT **и** `ON CONFLICT DO UPDATE SET` [`db_sqlite.py:549+`](../../../../../../src/core/infrastructure/db_sqlite.py)), supabase (migration + row + `_story_record_from_supabase_row` [`db_supabase.py:154`](../../../../../../src/core/infrastructure/db_supabase.py) + `_STORY_SELECT_FIELDS` [`:66`](../../../../../../src/core/infrastructure/db_supabase.py)).

`CREATE TABLE IF NOT EXISTS stories` ([`db_sqlite.py:177`](../../../../../../src/core/infrastructure/db_sqlite.py)) **не** переписывать ради новых колонок — существующие DB не подхватят; только `_ensure_sqlite_schema_migrations` ALTER (как geo).

`REQUIRED_READINESS_TABLES` не менять. `required_columns_ready` ([`db_supabase.py:336`](../../../../../../src/core/infrastructure/db_supabase.py)) **не** расширять binding-колонками (503 `/ready` до hosted apply). Cross-layer invariant: каждое имя в `_STORY_SELECT_FIELDS` должно быть в [`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql) — иначе [`test_stories_schema_cross_layer_invariant.py`](../../../../../../tests/test_stories_schema_cross_layer_invariant.py) красный.

Hosted SELECT без миграции падает на unknown column. Допустимый паттерн: omit-probe как `_story_select_fields_for_db` / geo_admin ([`:418`](../../../../../../src/core/infrastructure/db_supabase.py)), не silent drop payload на write если колонки есть.

`update_lifecycle_status` (sqlite UPDATE только статуса) extra columns не трогает — не путать с `advance_story_readiness` reconstruct.

Intake **ещё не** пишет binding (SSR-03). Эта стори может закрыть round-trip тестом через `save_story` напрямую (как TAX persist), без parser.

## Подзадачи

| ID | Слой | Задача | Где | Не делать |
|----|------|--------|-----|-----------|
| **T00** | Naming | Зафиксировать map parent→`StoryRecord`/SQL в этой стори (таблица выше). | this file + domain comments | Вторая колонка `schema_version` |
| **T01** | Domain | Optional fields на `StoryRecord` с default `None`. | [`contracts.py:44`](../../../../../../src/core/domain/contracts.py) | Domain columns (`institution_type`, …) |
| **T02** | Hash | Canonical JSON of validated payload → `payload_hash`. Не принимать client hash. | `src/core/schema/` helper, зов из persist/intake позже | |
| **T03** | sqlite | ALTER в `_ensure_sqlite_schema_migrations`; `_STORY_SELECT_COLUMNS`; `_story_record_from_sqlite_row`; INSERT **и** `ON CONFLICT DO UPDATE SET` для каждого нового поля. | [`db_sqlite.py`](../../../../../../src/core/infrastructure/db_sqlite.py) | Новая таблица в REQUIRED; только INSERT без UPDATE SET |
| **T04** | Application | `StoryRecord(` intake create [`services.py:236`](../../../../../../src/core/application/services.py) defaults None; **lifecycle copy** [`:461`](../../../../../../src/core/application/services.py) — все новые поля. Предпочтительно `dataclasses.replace(current, lifecycle_status=…, updated_at=…)`. | [`services.py`](../../../../../../src/core/application/services.py) | Забыть copy |
| **T05** | supabase row | save row dict + from_row + `_STORY_SELECT_FIELDS`. Omit-probe если unmigrated host (как geo_admin), иначе SELECT civic сломается. | [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) | Класть поля в `required_columns_ready`; ломать geo-split |
| **T06** | SQL + bootstrap | `supabase/migrations/` ADD COLUMN nullable; **тот же** `ALTER … ADD COLUMN IF NOT EXISTS` в [`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql). Не schema-specific DDL. | migration + bootstrap | Node-specific columns; SELECT без bootstrap |
| **T07** | Tests | Two payloads same table; round-trip sqlite+memory; civic save без binding (все None) зелёный; lifecycle advance **сохраняет** binding. | `tests/test_gw_ssr_02_*` | Live hosted как единственный proof |
| **T08** | Gate | AC-002/003; envelope `schema_version` civic rows unchanged. | | |

## Target / AC

- [x] AC-GW-REQ3-02 / AC-002: two unrelated payloads persist on same core model; no schema-specific DDL between them.
- [x] AC-GW-REQ3-03 / AC-003: stored structured Story identifies envelope version, schema ID/version, profile ID/version, payload.
- [x] DATA-001: no node-specific `stories` columns for domain fields.
- [x] DATA-004: deterministic hash of canonical validated payload persisted as `payload_hash`.
- [x] Existing M2 persist of current envelope `schema_version` remains operational.

## Точки в коде

- Domain: `StoryRecord` ([`contracts.py:44`](../../../../../../src/core/domain/contracts.py)).
- sqlite: [`db_sqlite.py`](../../../../../../src/core/infrastructure/db_sqlite.py) SELECT [`:72`](../../../../../../src/core/infrastructure/db_sqlite.py), INSERT [`:537`](../../../../../../src/core/infrastructure/db_sqlite.py), ON CONFLICT [`:549`](../../../../../../src/core/infrastructure/db_sqlite.py), ALTER [`:306`](../../../../../../src/core/infrastructure/db_sqlite.py).
- supabase: [`db_supabase.py`](../../../../../../src/core/infrastructure/db_supabase.py) from_row [`:154`](../../../../../../src/core/infrastructure/db_supabase.py), save [`:434`](../../../../../../src/core/infrastructure/db_supabase.py), `_STORY_SELECT_FIELDS` [`:66`](../../../../../../src/core/infrastructure/db_supabase.py).
- Bootstrap: [`000_full_init.sql`](../../../../../../supabase/bootstrap/000_full_init.sql).
- Lifecycle reconstruct: [`services.py:461`](../../../../../../src/core/application/services.py). Status-only: [`db_sqlite.py:670`](../../../../../../src/core/infrastructure/db_sqlite.py).
- Do not invent HTTP. Do not add tables to [`REQUIRED_READINESS_TABLES`](../../../../../../src/core/infrastructure/db_supabase.py). Do not add binding cols to `required_columns_ready`.

## Dependencies

- SSR-01 (validate before persist).
- Identity не зависит и не меняется.
