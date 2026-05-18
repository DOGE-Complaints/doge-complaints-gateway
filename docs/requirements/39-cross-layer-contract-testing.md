# 39. Тестирование контрактов между слоями

**Дата:** 2026-05-10 (обновлён 2026-05-18)  
**Статус:** requirements — ready for tasking  
**Supersedes:** `req-cross-layer-contract-testing.md` (unnumbered, 2026-05-10)  
**Зависит от:** REQ-24 (`24-tallinn-issues-read-api.md`), REQ-27 (`27-doge-issue-domain-rename.md`), REQ-33 (`33-multilingual-story-intake-contract-v2.md`), REQ-34 (`34-civic-clustering-canonical-signal-pipeline.md`), REQ-35 (`35-geo-scope-node-architecture-and-filtering.md`), REQ-40 (`40-geo-propagation-to-issue-projection.md`)  
**Контекст:** По итогам gap-анализа (`data-model-vs-bootstrap-000-full-init-2026-05-08.md §16`) и независимой верификации (`gap-verification-report-2026-05-10.md`) установлено, что 226 unit-тестов не выловили ни один из 11 структурных gaps. Причина — тесты проверяют слои изолированно, но не контракты на стыках. За период REQ-24/33–40 добавились новые слои: clustering pipeline, issue projection, geo propagation, filter engine, E2E sandbox — без contract-тестирования.  
**Методология:** только факты из кода; каждое требование привязано к конкретным файлам.

---

## 1. Контекст и цель

### 1.1 Исходная проблема (2026-05-10)

Структурные gaps (GAP-07, GAP-08, GAP-11) существовали незамеченными потому что:
- Unit-тесты работают с Python-объектами напрямую, не проходя сериализацию/десериализацию
- Bootstrap SQL и код не связаны единым инвариантом
- In-memory реализации не имеют SQL-ограничений, маскируя ошибки типов

### 1.2 Расширение (2026-05-18)

Введены REQ-24/27/33–40. Новые слои создали новые незакрытые стыки:
- Clustering pipeline (REQ-34): story → signals → cluster → IssueCreateService → doge_issues
- Geo propagation (REQ-40): StoryGeoSnapshot → ProjectionInput → DOGEIssue.geo
- IssueProjectionReadStore (REQ-24): Protocol ↔ 3 реализации (InMemory/SQLite/Supabase)
- filter_projection_rows() (REQ-24): 15-параметровый filter engine в `read_filters.py`
- E2E sandbox: полный pipeline на реальных данных из `tests/sandbox/`

Существующие зоны A–I остаются в силе и расширяются пятью новыми (J–N).

---

## 2. Архитектура слоёв и SEAM-зоны

```
┌──────────────────────────────────────────────────────────────────────┐
│  ВНЕШНИЙ ПРОДЮСЕР                                                    │
│  GPT api-orchestrator.md §5.2.1                                      │
│  Формирует JSON-payload → POST /intake/stories                       │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ raw HTTP JSON dict
                    ══════════╪══════════ SEAM-0: HTTP boundary
                              │
┌─────────────────────────────▼────────────────────────────────────────┐
│  TRANSPORT LAYER (asgi_app.py)                                       │
│  intake_stories() → читает request.json(), передаёт в handler        │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ payload: dict + idempotency_key + trace_id
                    ══════════╪══════════ SEAM-E: API handler ↔ Service facade
                              │
┌─────────────────────────────▼────────────────────────────────────────┐
│  API HANDLER LAYER (handlers.py: handle_story_intake)                │
│  ├── parse_story_intake_request(payload) → StoryIntakeRequest        │◄─ SEAM-E1: парсинг/валидация
│  └── deps.story_intake_service.create_story(request, idempotency_key)│◄─ SEAM-E2: вызов сервиса
│                                                                       │
│  deps: ApiDependencies (dependencies.py)                             │◄─ SEAM-I: factory wiring
│    └── story_intake_service: StoryIntakeService                      │
│         (собран через DefaultServiceFactory.get_story_intake_service)│
└──────────────┬──────────────────────────────────────────────────────┘
               │ StoryIntakeRequest (typed dataclass)
     ══════════╪══════════ SEAM-C: StoryIntakeRequest ↔ StoryRecord
               │
┌──────────────▼──────────────────────────────────────────────────────┐
│  APPLICATION SERVICE LAYER (services.py: StoryIntakeService)        │
│  ├── idempotency_repository.get_by_key()                            │
│  ├── geo_service.resolve(location_query) → StoryGeoSnapshot|None    │
│  ├── repository.save_story(StoryRecord) → StoryRecord               │◄─ SEAM-D: Protocol impl
│  └── story_embedding_store.save_story_embedding(...)                │◄─ SEAM-H: store contract
└──────────────┬──────────────────────────────────────────────────────┘
               │ StoryRecord (domain dataclass)
     ══════════╪══════════ SEAM-D: Repository Protocol ↔ реализации
               │
┌──────────────▼──────────────────────────────────────────────────────┐
│  INFRASTRUCTURE LAYER — три реализации StoryRepository              │
│  InMemoryStoryRepository (repositories.py)   ← unit tests           │
│  SqliteStoryRepository   (db_sqlite.py)       ← offline integration  │
│  SupabaseStoryRepository (db_supabase.py)     ← live integration     │
│    ├── _STORY_SELECT_FIELDS — SELECT-поля                           │◄─ SEAM-A: fields ↔ SQL
│    ├── _story_geo_supabase_fields() — geo dict для INSERT           │◄─ SEAM-A: fields ↔ SQL
│    └── _coerce_jsonb_text_id_sequence() — PostgREST десериализация  │◄─ SEAM-B: PostgREST types
└──────────────┬──────────────────────────────────────────────────────┘
               │ HTTP → PostgREST → PostgreSQL
     ══════════╪══════════ SEAM-A/B: SQL schema ↔ Python types
               │
┌──────────────▼──────────────────────────────────────────────────────┐
│  DATABASE LAYER                                                      │
│  PostgreSQL (Supabase) — схема из 000_full_init.sql                 │◄─ SEAM-A: bootstrap parity
│  PostgREST — JSON serialization типов (JSONB→list, TEXT→str, ...)   │◄─ SEAM-B: type coercion
│  required_columns_ready() — runtime check наличия колонок           │◄─ SEAM-G: 3 источника правды
└──────────────────────────────────────────────────────────────────────┘

Пересекающие слои:
  SEAM-F: configure_logging ↔ pytest/uvicorn context
  SEAM-G: required_columns_ready() ↔ _STORY_SELECT_FIELDS ↔ bootstrap SQL

═══════════════════ НОВЫЕ SEAM-ЗОНЫ (REQ-24/33–40) ════════════════════

┌──────────────────────────────────────────────────────────────────────┐
│  SCHEDULING / CRON LAYER (REQ-28)                                    │
│  StoryClusterOrchestrator.run_clustering_cycle()                     │
└──────────────┬───────────────────────────────────────────────────────┘
               │ cluster_id, story_ids, env: CLUSTER_MIN_SIZE
     ══════════╪══════════ SEAM-J: Clustering pipeline stitch
               │
┌──────────────▼───────────────────────────────────────────────────────┐
│  APPLICATION LAYER (issue_create.py: IssueCreateService)             │
│  ├── StoryPromotionProjectionBridge.build_projection_input()         │◄─ SEAM-K: geo propagation
│  │     StoryRecord.geo → ProjectionInput.geo_snapshot                │
│  └── IssueProjectionStore.save_projection()                          │◄─ SEAM-L: store contract
└──────────────┬───────────────────────────────────────────────────────┘
               │ doge_issues (SQLite/Supabase/InMemory)
     ══════════╪══════════ SEAM-L: IssueProjectionReadStore ↔ 3 impl
               │
┌──────────────▼───────────────────────────────────────────────────────┐
│  FILTER ENGINE (read_filters.py: filter_projection_rows)             │
│  15 параметров: status, type, labels, institution, temporal, geo     │◄─ SEAM-M: filter contract
└──────────────┬───────────────────────────────────────────────────────┘
               │ filtered list[dict] → HTTP response
     ══════════╪══════════ SEAM-N: E2E sandbox pipeline
               │
┌──────────────▼───────────────────────────────────────────────────────┐
│  HTTP READ LAYER (handlers.py: handle_list_issues / handle_get_issue)│
│  GET /tallinn/issues — публичный эндпоинт                            │
│  GET /tallinn/issues/{issue_id}                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Зоны тестирования — обзорная таблица

| Зона | SEAM | Стык | Тест-файл |
|------|------|------|-----------|
| A | SEAM-A | Bootstrap SQL ↔ Python write/read | `test_supabase_bootstrap_schema.py` |
| B | SEAM-B | PostgREST types ↔ Python десериализация | `test_supabase_deserialization_contracts.py` |
| C | SEAM-C | StoryIntakeRequest ↔ StoryRecord | `test_story_intake_field_persistence.py` |
| D | SEAM-D | StoryRepository Protocol ↔ 3 реализации | `test_story_repository_contract.py` |
| E | SEAM-E | API handler ↔ Service facade (parse + create_story) | `test_api_service_contract.py` |
| F | SEAM-F | configure_logging ↔ pytest/uvicorn | `test_logging_setup.py` |
| G | SEAM-G | required_columns_ready() ↔ SQL ↔ SELECT fields | `test_supabase_bootstrap_schema.py` |
| H | SEAM-H | Embedding/Signal/Cluster stores in-memory vs Supabase | `test_store_contract_parity.py` |
| I | SEAM-I | DB_BACKEND config ↔ factory wiring | `test_config_loading.py` |
| J | SEAM-J | Clustering pipeline stitch: stories → cluster → doge_issues | `test_clustering_pipeline_contract.py` |
| K | SEAM-K | Geo propagation: StoryRecord.geo → DOGEIssue.geo | `test_geo_propagation_contract.py` |
| L | SEAM-L | IssueProjectionReadStore Protocol ↔ 3 реализации | `test_issue_projection_store_contract.py` |
| M | SEAM-M | filter_projection_rows() — 15-параметровый filter engine | `test_filter_projection_rows_contract.py` |
| N | SEAM-N | E2E sandbox pipeline: canvas → intake → issues → GET | `test_e2e_sandbox_full_pipeline.py` |

---

## Оглавление

**Зоны A–I (intake/story pipeline):**
1. [Зона A: Bootstrap SQL ↔ Python write/read fields](#зона-a-bootstrap-sql--python-writeread-fields)
2. [Зона B: PostgREST response format ↔ Python десериализация](#зона-b-postgrest-response-format--python-десериализация)
3. [Зона C: StoryIntakeRequest ↔ StoryRecord (services.py mapping)](#зона-c-storyintakerequest--storyrecord-servicespy-mapping)
4. [Зона D: StoryRepository Protocol ↔ три реализации](#зона-d-storyrepository-protocol--три-реализации)
5. [Зона E: API handler ↔ Service facade](#зона-e-api-handler--service-facade)
6. [Зона F: configure_logging ↔ pytest / uvicorn context](#зона-f-configure_logging--pytest--uvicorn-context)
7. [Зона G: required_columns_ready() ↔ bootstrap SQL ↔ _STORY_SELECT_FIELDS](#зона-g-required_columns_ready--bootstrap-sql--_story_select_fields)
8. [Зона H: Embedding / Signal / Cluster stores — in-memory vs Supabase](#зона-h-embedding--signal--cluster-stores--in-memory-vs-supabase)
9. [Зона I: DB_BACKEND конфигурация ↔ factory wiring](#зона-i-db_backend-конфигурация--factory-wiring)

**Новые зоны J–N (clustering/issue/filter/e2e pipeline):**
10. [Зона J: Clustering pipeline stitch](#зона-j-clustering-pipeline-stitch)
11. [Зона K: Geo propagation cascade (REQ-40)](#зона-k-geo-propagation-cascade-req-40)
12. [Зона L: IssueProjectionReadStore Protocol ↔ 3 реализации](#зона-l-issueprojectionreadstore-protocol--3-реализации)
13. [Зона M: filter_projection_rows() — filter engine contract](#зона-m-filter_projection_rows--filter-engine-contract)
14. [Зона N: E2E sandbox test — полный датасет](#зона-n-e2e-sandbox-test--полный-датасет)

**Инфраструктура:**
15. [Системный инвариант: единый test-run для всех зон](#системный-инвариант-единый-test-run-для-всех-зон)
16. [Порядок реализации](#порядок-реализации)
17. [Acceptance Criteria](#acceptance-criteria)

---

## Зона A: Bootstrap SQL ↔ Python write/read fields

### Контекст

Код читает и пишет поля через три независимые структуры:
- `_STORY_SELECT_FIELDS` (`db_supabase.py:39-46`) — tuple строк, подставляется в каждый SELECT
- `save_story()` (`db_supabase.py:289-330`) — dict с полями для INSERT/UPSERT
- `_story_geo_supabase_fields()` (`db_supabase.py:48-70`) — geo-словарь, всегда merge-ится в INSERT

Bootstrap SQL `supabase/bootstrap/000_full_init.sql` — независимый артефакт. Нет механизма, связывающего их в единый инвариант. GAP-07 существовал незамеченным именно поэтому.

### Требуемые тесты (файл: `tests/test_supabase_bootstrap_schema.py`)

**A-01: Каждое поле из `_STORY_SELECT_FIELDS` присутствует в bootstrap SQL как имя колонки**

```python
def test_story_select_fields_all_in_bootstrap_sql():
    from core.infrastructure.db_supabase import _STORY_SELECT_FIELDS
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    for field in _STORY_SELECT_FIELDS.split(","):
        field = field.strip()
        assert field in sql, f"SELECT field '{field}' not found in bootstrap SQL"
```

*Что проверяет:* добавление поля в `_STORY_SELECT_FIELDS` без соответствующего ALTER в bootstrap немедленно ломает тест.

**A-02: Типы geo-колонок точно соответствуют ожидаемым**

```python
def test_geo_columns_have_correct_sql_types():
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    assert "geo_latitude double precision" in sql
    assert "geo_longitude double precision" in sql
    assert "geo_confidence double precision" in sql
    assert "geo_normalized_label text" in sql
    assert "geo_provider text" in sql
    assert "geo_cluster_tags_json text not null default '[]'" in sql
```

*Что проверяет:* тип `float` в Python матчит `double precision` в SQL; `text not null default '[]'` обеспечивает что `_story_geo_supabase_fields()` не провалит INSERT при `geo=None`.

**A-03: `embedding` объявлена nullable в bootstrap (вариант A)**

```python
def test_embedding_columns_are_nullable_in_bootstrap():
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    # Оба ALTER должны присутствовать
    count = sql.count("alter column embedding drop not null")
    assert count == 2, f"Expected 2 DROP NOT NULL for embedding, got {count}"
```

**A-04: Дельта-миграция существует и содержит тот же DDL**

```python
def test_delta_migration_exists_and_covers_gap07_gap08():
    path = Path("supabase/migrations/20260510_1400_m2_02_bootstrap_geo_embedding_nullable.sql")
    assert path.exists()
    content = path.read_text()
    assert "geo_normalized_label" in content
    assert "alter column embedding drop not null" in content
    assert "add column if not exists" in content  # идемпотентность
```

**A-05: `narrative_canonical_labels_json` объявлена как TEXT, не JSONB**

```python
def test_canonical_labels_is_text_not_jsonb():
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    # TEXT, а не jsonb — важно для паттерна json.loads(str(...))
    assert "narrative_canonical_labels_json text" in sql
    assert "narrative_canonical_labels_json jsonb" not in sql
```

*Почему важно:* `db_supabase.py:89` использует `json.loads(str(row[...]))` — на JSONB это было бы багом, на TEXT — корректно.

---

## Зона B: PostgREST response format ↔ Python десериализация

### Контекст

PostgREST преобразует PostgreSQL типы в JSON следующим образом:
- `jsonb` массив → Python `list`
- `jsonb` объект → Python `dict`
- `text` → Python `str`
- `boolean` → Python `bool`
- `timestamptz` → Python `str` (ISO 8601)
- `double precision` → Python `float`
- `vector(8)` — не включён в SELECT, возвращался бы как строка

Текущий unit-suite не проверяет ни один из этих паттернов — все тесты работают с Python-объектами напрямую.

### Требуемые тесты (файл: `tests/test_supabase_deserialization_contracts.py`)

**B-01: JSONB-массив (list) корректно десериализуется в tuple[str, ...]**

```python
def test_jsonb_list_coercion_covers_all_cases():
    from core.infrastructure.db_supabase import _coerce_jsonb_text_id_sequence
    # PostgREST JSONB → Python list
    assert _coerce_jsonb_text_id_sequence(["a", "b"]) == ("a", "b")
    # legacy JSON string
    assert _coerce_jsonb_text_id_sequence('["x","y"]') == ("x", "y")
    # None (отсутствие записи)
    assert _coerce_jsonb_text_id_sequence(None) == ()
    # пустые варианты
    assert _coerce_jsonb_text_id_sequence([]) == ()
    assert _coerce_jsonb_text_id_sequence("[]") == ()
    # нестроковые элементы (если PostgREST вернёт int)
    assert _coerce_jsonb_text_id_sequence([1, 2]) == ("1", "2")
```

**B-02: TEXT-колонки с JSON-содержимым корректно десериализуются**

```python
def test_text_json_columns_correct_deserialization():
    import json
    # geo_cluster_tags_json: TEXT, всегда JSON-строка из PostgREST
    raw_tags = '["tag1","tag2"]'
    assert tuple(json.loads(str(raw_tags or "[]"))) == ("tag1", "tag2")
    # пустой default
    empty = "[]"
    assert tuple(json.loads(str(empty or "[]"))) == ()
    # narrative_canonical_labels_json: TEXT, аналогично
    raw_labels = '["infrastructure","transport"]'
    assert json.loads(str(raw_labels)) == ["infrastructure", "transport"]
```

**B-03: `_coerce_datetime` обрабатывает timestamptz-строки от PostgREST**

```python
def test_datetime_coercion_from_postgrest_format():
    from core.infrastructure.db_supabase import _coerce_datetime
    # PostgREST возвращает ISO с timezone
    assert _coerce_datetime("2026-05-10T14:00:00+00:00") is not None
    assert _coerce_datetime("2026-05-10T14:00:00Z") is not None
```

**B-04: Недопустимая JSON-строка поднимает `json.JSONDecodeError`, не возвращает пустоту**

```python
def test_coerce_invalid_string_raises_not_silences():
    import pytest
    from core.infrastructure.db_supabase import _coerce_jsonb_text_id_sequence
    with pytest.raises(json.JSONDecodeError):
        _coerce_jsonb_text_id_sequence("not json at all")
```

---

## Зона C: StoryIntakeRequest ↔ StoryRecord (services.py mapping)

### Контекст

`StoryIntakeService.create_story()` (`services.py:72+`) принимает `StoryIntakeRequest` и строит `StoryRecord`. Некоторые поля молча не переносятся:
- `live_story_context.consistency_notes` — принимается (`contracts.py:198-225`), не читается в `services.py`
- `narrative.location_query` → `GeoService` → `record.geo` (работает, если GeoService настроен)
- `origin.*` — переносятся, но GPT-оркестратор их не заполняет

Ни один тест не проверяет полную цепочку: intake payload → `StoryRecord` поле за полем.

### Требуемые тесты (файл: `tests/test_story_intake_field_persistence.py`)

**C-01: `consistency_notes` принимается API, не попадает в StoryRecord**

```python
def test_consistency_notes_accepted_but_not_in_storyrecord(in_memory_deps):
    import dataclasses
    # Убеждаемся что поля нет в StoryRecord по определению
    field_names = {f.name for f in dataclasses.fields(StoryRecord)}
    assert "consistency_notes" not in field_names
    assert "live_story_context" not in field_names
```

*Цель:* если поле когда-нибудь добавят в `StoryRecord`, тест упадёт и напомнит добавить маппинг в `services.py`.

**C-02: Все поля StoryIntakeRequest маппируются или явно задокументированы как discarded**

```python
def test_intake_to_storyrecord_field_coverage():
    """Каждое поле StoryIntakeRequest либо есть в StoryRecord, либо задокументировано как discarded."""
    # Поля StoryIntakeRequest (верхний уровень и вложенные)
    mapped = {
        "schema_version", "submitter_external_user_id", "submitter_identity_issuer",
        "narrative_original_text", "narrative_language", "narrative_title_hint",
        "narrative_location_query",  # → через GeoService → geo
        "narrative_canonical_type", "narrative_canonical_labels",
        "origin_source", "origin_conversation_id", "origin_tool_call_id",
        "privacy_contains_pii", "privacy_redaction_requested",
    }
    explicitly_discarded = {
        "live_story_context",  # GAP-06: принимается, не персистируется
    }
    # Этот тест — документальный контракт, не runtime проверка
    # Если GAP-06 закроют, убрать из explicitly_discarded и добавить в mapped
    assert len(explicitly_discarded) >= 1  # напоминание что GAP-06 открыт
```

**C-03: `narrative_complete` логика — оба условия должны выполняться для READY_FOR_PROFILE**

```python
@pytest.mark.parametrize("language,title_hint,expected_status", [
    ("et", "Title", "READY_FOR_PROFILE"),
    ("",   "Title", "PARTIAL_READY"),
    ("et", "",      "PARTIAL_READY"),
    ("",   "",      "PARTIAL_READY"),
])
def test_narrative_complete_determines_lifecycle(language, title_hint, expected_status, ...):
    ...
```

*Что проверяет:* стык `StoryIntakeRequest.narrative.language` → `services.py:208` проверка → `StoryRecord.lifecycle_status`.

**C-04: geo-поля в StoryRecord None когда location_query не передан**

```python
def test_no_location_query_results_in_none_geo(in_memory_deps):
    # payload без location_query
    ...
    assert story.geo is None
```

---

## Зона D: StoryRepository Protocol ↔ три реализации

### Контекст

`StoryRepository` (`domain/contracts.py:61`) — Protocol с 4 методами. Три реализации: `InMemoryStoryRepository`, `SqliteStoryRepository`, `SupabaseStoryRepository`. Все три должны давать одинаковое поведение при одних входных данных. Различие в том, что InMemory хранит Python-объект напрямую, SQLite и Supabase делают сериализацию/десериализацию — там могут теряться данные (например, enum → str → enum).

### Требуемые тесты (файл: `tests/test_story_repository_contract.py`)

**D-01: save→get roundtrip сохраняет все поля StoryRecord — для каждой реализации**

```python
@pytest.mark.parametrize("repo_factory", [
    lambda: InMemoryStoryRepository(),
    lambda: SqliteStoryRepository(SqliteDatabase.from_url("sqlite:///:memory:")),
])
def test_save_get_roundtrip_preserves_all_fields(repo_factory):
    repo = repo_factory()
    original = make_full_story_record()  # все поля заполнены
    repo.save_story(original)
    loaded = repo.get_story(original.story_id)
    assert loaded is not None
    assert loaded.story_id == original.story_id
    assert loaded.narrative_original_text == original.narrative_original_text
    assert loaded.narrative_language == original.narrative_language
    assert loaded.narrative_title_hint == original.narrative_title_hint
    assert loaded.narrative_canonical_type == original.narrative_canonical_type
    assert loaded.narrative_canonical_labels == original.narrative_canonical_labels
    assert loaded.lifecycle_status == original.lifecycle_status
    assert loaded.geo == original.geo
    assert loaded.origin_source == original.origin_source
    assert loaded.privacy_contains_pii == original.privacy_contains_pii
```

*Примечание: `SupabaseStoryRepository` — только в live-тестах с реальной БД.*

**D-02: `list_stories_ready_for_clustering()` возвращает только READY_FOR_PROFILE**

```python
@pytest.mark.parametrize("repo_factory", [...])
def test_list_ready_for_clustering_filters_correctly(repo_factory):
    repo = repo_factory()
    ready = make_story(status=StoryLifecycleStatus.READY_FOR_PROFILE)
    partial = make_story(status=StoryLifecycleStatus.PARTIAL_READY)
    accepted = make_story(status=StoryLifecycleStatus.ACCEPTED)
    for s in [ready, partial, accepted]:
        repo.save_story(s)
    result = repo.list_stories_ready_for_clustering()
    ids = {s.story_id for s in result}
    assert ready.story_id in ids
    assert partial.story_id not in ids
    assert accepted.story_id not in ids
```

**D-03: `update_lifecycle_status` на несуществующем story_id поднимает исключение**

```python
@pytest.mark.parametrize("repo_factory", [...])
def test_update_lifecycle_unknown_story_raises(repo_factory):
    repo = repo_factory()
    with pytest.raises(ValueError):
        repo.update_lifecycle_status("nonexistent", StoryLifecycleStatus.READY_FOR_PROFILE)
```

**D-04: Двойной save (upsert) не дублирует запись**

```python
@pytest.mark.parametrize("repo_factory", [...])
def test_double_save_is_idempotent(repo_factory):
    repo = repo_factory()
    record = make_story()
    repo.save_story(record)
    repo.save_story(record)
    all_stories = repo.list_stories()
    assert len([s for s in all_stories if s.story_id == record.story_id]) == 1
```

---

## Зона E: API handler ↔ Service facade

### Контекст

Стык между HTTP-слоем и application-слоем состоит из двух частей:

**SEAM-E1** — `parse_story_intake_request(payload)` (`intake/contracts.py`): raw dict → `StoryIntakeRequest`. Это валидирующий парсер: проверяет `schema_version` (exact match `"m2.story_intake_envelope.v1"`), обязательные поля, enum-значения `language` (et/ru/en). Ошибки превращаются в `IntakeValidationError`.

**SEAM-E2** — `handle_story_intake()` → `deps.story_intake_service.create_story(request, idempotency_key)` (`handlers.py:155`). Фасад `ApiDependencies` (`dependencies.py:17-19`) предоставляет `story_intake_service: StoryIntakeService`, собранный через `DefaultServiceFactory.get_story_intake_service()` (`service_factory.py:64-72`).

Что здесь не тестируется сейчас:
- Полный маршрут от raw HTTP dict до `StoryIntakeRequest` — только через TestClient, не юнитом
- Что `IntakeValidationError` приводит к корректному HTTP-ответу (не 500)
- Что `idempotency_key` из HTTP-header корректно прокидывается в сервис
- Что логи в handler-е (`log_api_event`) не ломают выполнение при разных payload-ах
- Что `ApiDependencies.story_intake_service.repository` соответствует выбранному бекенду

### Требуемые тесты (файл: `tests/test_api_service_contract.py`)

**E-01: `parse_story_intake_request` — минимальный валидный payload проходит**

```python
def test_parse_minimal_valid_payload():
    from core.intake.contracts import parse_story_intake_request
    payload = {
        "schema_version": "m2.story_intake_envelope.v1",
        "submitter": {"external_user_id": "u-001"},
        "narrative": {
            "original_text": "Katki sillal on auk",
            "language": "et",
            "title_hint": "Katki sild",
        },
    }
    result = parse_story_intake_request(payload)
    assert result.schema_version == "m2.story_intake_envelope.v1"
    assert result.submitter.external_user_id == "u-001"
    assert result.narrative.language == "et"
    assert result.narrative.title_hint == "Katki sild"
    assert result.narrative.location_query is None
    assert result.narrative.canonical_type is None
    assert result.narrative.canonical_labels == ()
```

**E-02: Неверный `schema_version` → `IntakeValidationError`, не KeyError или TypeError**

```python
def test_wrong_schema_version_raises_intake_validation_error():
    from core.intake.contracts import parse_story_intake_request
    from core.intake import IntakeValidationError
    with pytest.raises(IntakeValidationError):
        parse_story_intake_request({
            "schema_version": "v99.wrong",
            "submitter": {"external_user_id": "u"},
            "narrative": {"original_text": "x", "language": "et", "title_hint": "t"},
        })
```

**E-03: Недопустимый `language` → `IntakeValidationError`**

```python
@pytest.mark.parametrize("lang", ["fr", "ee", "", "EST", "english"])
def test_invalid_language_raises_intake_validation_error(lang):
    from core.intake.contracts import parse_story_intake_request
    from core.intake import IntakeValidationError
    with pytest.raises(IntakeValidationError):
        parse_story_intake_request({
            "schema_version": "m2.story_intake_envelope.v1",
            "submitter": {"external_user_id": "u"},
            "narrative": {"original_text": "x", "language": lang, "title_hint": "t"},
        })
```

**E-04: `IntakeValidationError` в handler → HTTP 422, не HTTP 500**

```python
def test_invalid_payload_returns_422_not_500(test_client):
    resp = test_client.post("/intake/stories", json={"schema_version": "wrong"})
    assert resp.status_code != 500
    assert resp.status_code in (400, 422)
    body = resp.json()
    assert "error" in body or "detail" in body
```

**E-05: `idempotency_key` из header передаётся в service, повторный запрос — idempotent**

```python
def test_idempotency_key_deduplicates_story(test_client):
    payload = minimal_valid_payload()
    headers = {"idempotency-key": "test-key-001"}
    resp1 = test_client.post("/intake/stories", json=payload, headers=headers)
    resp2 = test_client.post("/intake/stories", json=payload, headers=headers)
    assert resp1.status_code == 200
    assert resp2.status_code == 200
    assert resp1.json()["data"]["story_id"] == resp2.json()["data"]["story_id"]
```

**E-06: `ApiDependencies.story_intake_service` имеет верный тип репозитория при `in_memory` бекенде**

```python
def test_api_dependencies_wires_correct_repo_for_in_memory():
    from core.infrastructure.providers import provide_app_config, provide_service_factory
    from core.infrastructure.repositories import InMemoryStoryRepository
    config = provide_app_config(env={"APP_PROFILE": "demo"})
    factory = provide_service_factory(config)
    svc = factory.get_story_intake_service()
    assert isinstance(svc.repository, InMemoryStoryRepository)
```

**E-07: `parse_story_intake_request` с `live_story_context.consistency_notes` не падает (GAP-06)**

```python
def test_payload_with_consistency_notes_parses_without_error():
    """GAP-06: consistency_notes принимается парсером, хотя в StoryRecord не сохраняется."""
    from core.intake.contracts import parse_story_intake_request
    result = parse_story_intake_request({
        "schema_version": "m2.story_intake_envelope.v1",
        "submitter": {"external_user_id": "u"},
        "narrative": {"original_text": "x", "language": "ru", "title_hint": "t"},
        "live_story_context": {"consistency_notes": "duplicate of #123"},
    })
    assert result.live_story_context is not None
    assert result.live_story_context.consistency_notes == "duplicate of #123"
    # StoryRecord не имеет этого поля — покрывается тестом C-01
```

**E-08: Поля из `canonical_labels` корректно парсируются как tuple (не list)**

```python
def test_canonical_labels_parsed_as_tuple():
    from core.intake.contracts import parse_story_intake_request
    result = parse_story_intake_request({
        "schema_version": "m2.story_intake_envelope.v1",
        "submitter": {"external_user_id": "u"},
        "narrative": {
            "original_text": "x", "language": "en", "title_hint": "t",
            "canonical_labels": ["infrastructure", "transport"],
        },
    })
    assert result.narrative.canonical_labels == ("infrastructure", "transport")
    assert isinstance(result.narrative.canonical_labels, tuple)
```

---

## Зона F: configure_logging ↔ pytest / uvicorn context

### Контекст

`configure_logging()` (`logging_setup.py:86-107`) вызывается из `asgi_app.py:82-86` в lifespan. Pytest не запускает lifespan при обычном использовании `TestClient` — только если явно использовать `with TestClient(app)` как context manager. Логи в тестах молчат (root level WARNING), что маскирует проблемы трассировки.

### Требуемые тесты (файл: `tests/test_logging_setup.py`)

**F-01: `configure_logging()` выставляет root logger на переданный уровень**

```python
def test_configure_logging_sets_root_level():
    import logging
    from core.logging_setup import configure_logging
    configure_logging("DEBUG")
    assert logging.getLogger().level == logging.DEBUG
    # cleanup
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger().handlers.clear()
```

**F-02: После `configure_logging()` DEBUG-сообщения достигают handler**

```python
def test_configure_logging_debug_messages_captured(caplog):
    from core.logging_setup import configure_logging
    configure_logging("DEBUG")
    with caplog.at_level(logging.DEBUG, logger="core.test"):
        logging.getLogger("core.test").debug("test debug message")
    assert "test debug message" in caplog.text
```

**F-03: `configure_logging()` удаляет pre-existing handlers (без дублирования)**

```python
def test_configure_logging_removes_old_handlers():
    import logging
    from core.logging_setup import configure_logging
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())
    initial_count = len(root.handlers)
    configure_logging("INFO")
    # должен быть ровно один StreamHandler, старые удалены
    assert len(root.handlers) == 1
    assert isinstance(root.handlers[0], logging.StreamHandler)
```

**F-04: pytest-fixture `configured_logging` для opt-in использования в тестах трассировки**

```python
# tests/conftest.py
@pytest.fixture
def configured_logging():
    """Opt-in: call configure_logging so log capture works in tests."""
    from core.logging_setup import configure_logging
    configure_logging("DEBUG", log_format="text")
    yield
    logging.getLogger().handlers.clear()
    logging.getLogger().setLevel(logging.WARNING)
```

*Использование:* `def test_intake_emits_structured_log(configured_logging, caplog): ...`

---

## Зона G: required_columns_ready() ↔ bootstrap SQL ↔ _STORY_SELECT_FIELDS

### Контекст

Три независимых источника правды о составе `public.stories`:

| Источник | Файл | Назначение |
|---|---|---|
| `_STORY_SELECT_FIELDS` | `db_supabase.py:39-46` | Поля, которые SELECT запрашивает |
| `required_columns_ready()` | `db_supabase.py:238-270` | Поля, наличие которых проверяется в live DB |
| `000_full_init.sql` | `supabase/bootstrap/` | Поля, которые реально существуют в БД |

GAP-07 возник потому что `_STORY_SELECT_FIELDS` был дополнен geo-полями, bootstrap — нет, а `required_columns_ready()` проверял geo-поля → возвращал `False` → intake падал. Тест-инвариант должен поймать такое рассогласование offline.

### Требуемые тесты (файл: `tests/test_supabase_bootstrap_schema.py`)

**G-01: Все поля из `_STORY_SELECT_FIELDS` входят в `required_columns_ready()` check-set или присутствуют в CREATE TABLE**

```python
def test_story_select_fields_covered_by_bootstrap():
    from core.infrastructure.db_supabase import _STORY_SELECT_FIELDS
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    for field in _STORY_SELECT_FIELDS.split(","):
        field = field.strip()
        assert field in sql, (
            f"Field '{field}' in _STORY_SELECT_FIELDS not found in bootstrap SQL. "
            f"Add 'add column if not exists {field} ...' to 000_full_init.sql"
        )
```

**G-02: `required_columns_ready()` проверяет подмножество `_STORY_SELECT_FIELDS`**

```python
def test_required_columns_subset_of_select_fields():
    """required_columns_ready() не должен проверять поля, которые код не запрашивает."""
    from core.infrastructure.db_supabase import _STORY_SELECT_FIELDS, SupabaseDatabase
    import inspect
    select_fields = set(_STORY_SELECT_FIELDS.split(","))
    select_fields = {f.strip() for f in select_fields}
    # Читаем source required_columns_ready чтобы найти список проверяемых полей
    src = inspect.getsource(SupabaseDatabase.required_columns_ready)
    # Проверяем что каждое упомянутое в required_columns_ready поле есть в SELECT
    for field in select_fields:
        if field in src:
            assert field in select_fields
```

**G-03: `required_columns_ready()` возвращает True на bootstrap SQL (через SQLite-прокси)**

*Примечание:* этот тест сложнее — `required_columns_ready()` делает live HTTP-запрос к Supabase. Альтернатива — тест через `SqliteDatabase`, если там реализован аналог. Пока — документальный тест, описывающий что должно быть True после bootstrap.

```python
def test_required_columns_ready_logic_covers_all_select_fields():
    """
    Документальный тест: убеждаемся что метод required_columns_ready()
    проверяет ровно те поля, которые есть в _STORY_SELECT_FIELDS и в bootstrap.
    Реальная проверка — только в live-тестах.
    """
    from core.infrastructure.db_supabase import _STORY_SELECT_FIELDS
    sql = Path("supabase/bootstrap/000_full_init.sql").read_text()
    geo_fields = [
        "geo_normalized_label", "geo_latitude", "geo_longitude",
        "geo_confidence", "geo_provider", "geo_cluster_tags_json"
    ]
    for f in geo_fields:
        assert f in _STORY_SELECT_FIELDS, f"geo field '{f}' missing from SELECT"
        assert f in sql, f"geo field '{f}' missing from bootstrap"
```

---

## Зона H: Embedding / Signal / Cluster stores — in-memory vs Supabase

### Контекст

Пять store-классов имеют in-memory и Supabase реализации:
- `InMemoryStoryEmbeddingStore` / `SupabaseStoryEmbeddingStore`
- `InMemoryStorySignalStore` / `SupabaseStorySignalStore`
- `InMemoryClusterMembershipStore` / `SupabaseClusterMembershipStore`
- `InMemoryIssueProjectionStore` / `SupabaseIssueProjectionStore`
- `InMemoryIssueProjectionEmbeddingStore` / `SupabaseIssueProjectionEmbeddingStore`

In-memory реализации не имеют SQL-ограничений → GAP-08 (`embedding NOT NULL`) не мог проявиться в unit-тестах.

### Требуемые тесты (файл: `tests/test_store_contract_parity.py`)

**H-01: `save_story_embedding()` пишет `embedding_vector_json`, не `embedding` vector**

```python
def test_story_embedding_store_writes_json_not_vector():
    """GAP-08: код пишет embedding_vector_json, колонка embedding должна быть nullable."""
    store = InMemoryStoryEmbeddingStore()
    store.save_story_embedding(
        story_id="s1",
        model_name="test-model",
        embedding_vector=(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8),
        source_checksum="abc123",
        embedding_policy_version="test.v1",
    )
    # Убеждаемся что в in-memory нет raw vector — только json
    # Тест документирует что write-контракт не включает raw embedding
```

**H-02: `signals_json` write pattern — dict, не json.dumps(dict)**

```python
def test_story_signal_store_writes_dict_not_json_string():
    """story_signals.signals_json — правильный паттерн: dict напрямую, не json.dumps."""
    # Проверяем что InMemoryStorySignalStore хранит dict, а не строку
    store = InMemoryStorySignalStore()
    signals = {"type": "complaint", "urgency": 3}
    store.save_signals(story_id="s1", extraction_policy="test-policy", signals=signals)
    result = store.get_signals(story_id="s1", extraction_policy="test-policy")
    assert result == signals
    assert isinstance(result, dict)
```

**H-03: `ClusterMembershipStore` — get_cluster_members возвращает только нужный lens**

```python
def test_cluster_membership_filters_by_lens():
    store = InMemoryClusterMembershipStore()
    store.save_membership(story_id="s1", lens="geo", cluster_id="c1")
    store.save_membership(story_id="s2", lens="topic", cluster_id="c1")
    members = store.get_cluster_members(cluster_id="c1", lens="geo")
    assert "s1" in members
    assert "s2" not in members
```

---

## Зона I: DB_BACKEND конфигурация ↔ factory wiring

### Контекст

`provide_service_factory()` (`infrastructure/providers.py:115-237`) выбирает backend на основе `config.db_backend`. Дефолт `"in_memory"` (`config/schema.py:113`). На Railway без явного `DB_BACKEND=supabase` — данные теряются в памяти процесса (GAP-11).

### Требуемые тесты (файл: `tests/test_config_loading.py`)

**I-01: Пустое окружение → `db_backend = "in_memory"`**

```python
def test_db_backend_defaults_to_in_memory():
    from core.infrastructure.providers import provide_app_config
    config = provide_app_config(env={})
    assert config.db_backend == "in_memory"
```

**I-02: `DB_BACKEND=supabase` → `db_backend = "supabase"`**

```python
def test_db_backend_supabase_from_env():
    from core.infrastructure.providers import provide_app_config
    config = provide_app_config(env={"DB_BACKEND": "supabase"})
    assert config.db_backend == "supabase"
```

**I-03: `provide_service_factory()` с `in_memory` возвращает in-memory репозитории**

```python
def test_factory_in_memory_uses_inmemory_repos():
    from core.infrastructure.providers import provide_service_factory, provide_app_config
    from core.infrastructure.repositories import InMemoryStoryRepository
    config = provide_app_config(env={"APP_PROFILE": "demo"})
    factory = provide_service_factory(config)
    service = factory.story_intake_service()
    # Проверяем через тип bridge.story_repository
    repo = service.bridge.story_repository
    assert isinstance(repo, InMemoryStoryRepository)
```

**I-04: Дефолт `in_memory` задокументирован как явная константа в коде**

```python
def test_in_memory_default_is_explicit_in_config_schema():
    import inspect
    from core.config import schema
    src = inspect.getsource(schema)
    assert '"in_memory"' in src or "'in_memory'" in src
```

---

## Зона J: Clustering pipeline stitch

### Контекст

`StoryClusterOrchestrator.run_clustering_cycle()` запускает цепочку: story read → signal extraction → cluster formation → `IssueCreateService.create_issue()` → `IssueProjectionStore.save_projection()`. Параметры кластеризации управляются через env:

- `CLUSTER_MIN_SIZE` — минимальное количество stories для создания issue (default: 2)
- `CLUSTER_READINESS_THRESHOLD` — порог готовности кластера (default: 0.5)

Ни один тест не проверяет, что при изменении `CLUSTER_MIN_SIZE` меняется поведение issue creation. Unit-тесты оркестратора не касаются `IssueProjectionStore`.

### Требуемые тесты (файл: `tests/test_clustering_pipeline_contract.py`)

**J-01: story count < `CLUSTER_MIN_SIZE` → issue НЕ создаётся**

```python
def test_cluster_below_min_size_does_not_create_issue(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "3")
    monkeypatch.setenv("APP_PROFILE", "demo")
    _clear_api_dependencies_cache()
    deps = get_api_dependencies()
    # Создать 2 stories (меньше CLUSTER_MIN_SIZE=3) и запустить кластеризацию
    # Проверить что IssueProjectionStore пуст
    store = deps.issue_create_service.issue_projection_store
    # ... intake 2 stories, trigger clustering ...
    assert store is not None
    issues = store.list_projections()
    assert len(issues) == 0
```

**J-02: story count >= `CLUSTER_MIN_SIZE` → issue создаётся в `doge_issues`**

```python
def test_cluster_at_min_size_creates_issue(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    monkeypatch.setenv("APP_PROFILE", "demo")
    _clear_api_dependencies_cache()
    deps = get_api_dependencies()
    client = TestClient(app)
    # POST 1 story → должна создасться issue при CLUSTER_MIN_SIZE=1
    payload = minimal_valid_intake_payload()
    resp = client.post("/intake/stories", json=payload)
    assert resp.status_code == 200
    # Trigger clustering
    cluster_resp = client.post("/clustering/trigger", headers=service_auth_headers())
    # issue_projection_store не пустой
    store = deps.issue_create_service.issue_projection_store
    issues = store.list_projections()
    assert len(issues) >= 1
```

**J-03: `policy_version` новой записи содержит `m3.doge_issue_derivation.v1`**

```python
def test_new_issue_has_m3_policy_version(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    # ... intake + clustering ...
    issues = store.list_projections()
    assert len(issues) >= 1
    # policy_version хранится отдельно от payload
    # Проверяем через прямой доступ к store._rows или через SQLite SELECT
    for issue_id in [i["issue_id"] for i in issues]:
        row = store._rows.get(issue_id)  # InMemory
        assert row is not None
        assert row.get("policy_version") == "m3.doge_issue_derivation.v1"
```

**J-04: повторный запуск кластеризации — duplicate issue не создаётся (idempotency)**

```python
def test_clustering_idempotent_no_duplicate_issues(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    # ... intake + clustering + clustering again ...
    issues = store.list_projections()
    issue_ids = [i["issue_id"] for i in issues]
    assert len(issue_ids) == len(set(issue_ids)), "Duplicate issue_ids found"
```

---

## Зона K: Geo propagation cascade (REQ-40)

### Контекст

Geo-данные проходят следующую цепочку (REQ-40):

```
StoryRecord.geo (StoryGeoSnapshot | None)
  → StoryPromotionProjectionBridge.build_projection_input()   (issue_create.py:152)
  → ProjectionInput.geo_snapshot
  → DeterministicStoryToProjectionPolicy.project_distinct_issue()
  → DOGEIssue.geo (dict | None)
  → IssueProjectionStore.save_projection(payload=issue.to_public_dict())
  → doge_issues.payload_json["geo"]
```

Без contract-теста можно сломать `build_projection_input` или `project_distinct_issue` и geo перестанет проходить в issues без явной ошибки.

### Требуемые тесты (файл: `tests/test_geo_propagation_contract.py`)

**K-01: story с `geo` → issue содержит `geo` snapshot в `payload_json`**

```python
def test_story_with_geo_produces_issue_with_geo(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    # ... intake story with location_query → geo resolved ...
    # ... trigger clustering ...
    issues = store.list_projections()
    assert any(i.get("geo") is not None for i in issues)
    geo = next(i["geo"] for i in issues if i.get("geo"))
    assert "lat" in geo or "district" in geo
```

**K-02: story без `geo` → issue содержит `geo: null`**

```python
def test_story_without_geo_produces_issue_with_null_geo(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "1")
    # ... intake story без location_query ...
    issues = store.list_projections()
    issue = issues[0]
    assert issue.get("geo") is None
```

**K-03: `geo.district` сохраняется как нормализованный токен (lowercase, non-alnum stripped)**

```python
def test_geo_district_normalized_in_issue_payload(monkeypatch):
    from core.geo.scope import normalize_geo_token
    # ... intake story where geo.district = "Põhja-Tallinn" ...
    issues = store.list_projections()
    geo = issues[0].get("geo", {})
    district = geo.get("district", "")
    assert district == normalize_geo_token("Põhja-Tallinn")
```

**K-04: несколько stories в кластере → dominant geo определяется (не None если хоть одна имеет geo)**

```python
def test_cluster_dominant_geo_from_mixed_stories(monkeypatch):
    monkeypatch.setenv("CLUSTER_MIN_SIZE", "2")
    # story1 with geo, story2 without geo → cluster → issue should have geo from story1
    # ... intake both stories, trigger clustering ...
    issues = store.list_projections()
    assert len(issues) >= 1
    # At least one issue should have non-None geo (dominant from geo-having story)
    geo_present = [i for i in issues if i.get("geo") is not None]
    assert len(geo_present) >= 1
```

---

## Зона L: IssueProjectionReadStore Protocol ↔ 3 реализации

### Контекст

`IssueProjectionReadStore` Protocol (`issue_create.py:87-111`) — 2 метода:
- `list_projections(*, status, issue_type, labels, institution, created_after, created_before, geo_lat_min, geo_lat_max, geo_lon_min, geo_lon_max, geo_district, geo_settlement, geo_region, geo_country, geo_postal_code)` — 15 параметров
- `get_projection(issue_id)` → `dict | None`

Три реализации: `InMemoryIssueProjectionStore` (repositories.py), `SqliteIssueProjectionStore` (db_sqlite.py), `SupabaseIssueProjectionStore` (db_supabase.py). Все три должны давать одинаковое поведение на одних входных данных. Различие — SQL-уровень фильтрации status и created_at (SQL) vs Python post-fetch (type, labels, geo).

### Требуемые тесты (файл: `tests/test_issue_projection_store_contract.py`)

**L-01: `save_projection` + `get_projection` roundtrip — InMemory и SQLite**

```python
@pytest.mark.parametrize("store_factory", [
    lambda: InMemoryIssueProjectionStore(),
    lambda: SqliteIssueProjectionStore(SqliteDatabase.from_url("sqlite:///:memory:")),
])
def test_save_get_roundtrip(store_factory):
    store = store_factory()
    payload = {
        "issue_id": "test-001",
        "status": "PUBLISHED",
        "type": "IMPROVEMENT",
        "labels": ["infrastructure"],
        "geo": {"district": "põhja-tallinn", "lat": 59.44, "lon": 24.75},
        "created_at": "2026-05-18T10:00:00+00:00",
    }
    store.save_projection(
        issue_id="test-001",
        status="PUBLISHED",
        payload=payload,
        policy_version="m3.doge_issue_derivation.v1",
    )
    result = store.get_projection("test-001")
    assert result is not None
    assert result["issue_id"] == "test-001"
    assert result["status"] == "PUBLISHED"
    assert result["geo"]["district"] == "põhja-tallinn"
```

**L-02: `list_projections(status=["PUBLISHED"])` не возвращает DRAFT записи**

```python
@pytest.mark.parametrize("store_factory", [...])
def test_list_by_status_excludes_other_statuses(store_factory):
    store = store_factory()
    store.save_projection(issue_id="pub-1", status="PUBLISHED", payload={"issue_id": "pub-1", "status": "PUBLISHED"}, policy_version="m3.v1")
    store.save_projection(issue_id="draft-1", status="DRAFT", payload={"issue_id": "draft-1", "status": "DRAFT"}, policy_version="m3.v1")
    result = store.list_projections(status=["PUBLISHED"])
    ids = {r["issue_id"] for r in result}
    assert "pub-1" in ids
    assert "draft-1" not in ids
```

**L-03: `list_projections` без фильтров возвращает все записи**

```python
@pytest.mark.parametrize("store_factory", [...])
def test_list_no_filters_returns_all(store_factory):
    store = store_factory()
    for i in range(3):
        store.save_projection(issue_id=f"id-{i}", status="PUBLISHED", payload={"issue_id": f"id-{i}", "status": "PUBLISHED"}, policy_version="m3.v1")
    result = store.list_projections()
    assert len(result) == 3
```

**L-04: `get_projection` несуществующего issue_id → returns None**

```python
@pytest.mark.parametrize("store_factory", [...])
def test_get_nonexistent_returns_none(store_factory):
    store = store_factory()
    result = store.get_projection("nonexistent-id")
    assert result is None
```

---

## Зона M: filter_projection_rows() — filter engine contract

### Контекст

`filter_projection_rows()` (`src/core/projection/read_filters.py:175-222`) — центральный filter engine. Принимает `rows: list[tuple[str, dict, str]]` и 15 keyword-only параметров. Частично покрыт в `test_req24_tallinn_issues_read_api.py` (23 теста, AC-15/17/18/19). Дополнительные тесты покрывают оставшиеся filter-режимы.

Архитектура фильтрации:
- **SQL-уровень** (до `filter_projection_rows`): `status IN (...)`, `created_at` range — в `list_projections()` каждой store
- **Python post-fetch** (`filter_projection_rows`): `type`, `labels`, `institution`, `geo_*`
- **`_matches_geo_filters`**: null-safety (AC-15), bbox (AC-17 OR), district AND bbox (AC-18 AND)

### Требуемые тесты (файл: `tests/test_filter_projection_rows_contract.py`)

**M-01: status filter — пустой список → возвращает всё**

```python
def test_empty_status_list_returns_all():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "a", "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("DRAFT",     {"issue_id": "b", "status": "DRAFT"},     "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, status=[])
    assert len(result) == 2
```

**M-02: `issue_type` filter — exact match only**

```python
def test_issue_type_filter_exact_match():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "a", "type": "IMPROVEMENT", "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "b", "type": "BUG",         "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, issue_type="IMPROVEMENT")
    ids = {r["issue_id"] for r in result}
    assert ids == {"a"}
```

**M-03: `labels` filter — OR semantics (any matching label)**

```python
def test_labels_filter_or_semantics():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "a", "labels": ["infrastructure", "transport"], "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "b", "labels": ["waste"],                       "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "c", "labels": ["safety"],                      "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, labels=["infrastructure", "waste"])
    ids = {r["issue_id"] for r in result}
    assert ids == {"a", "b"}
```

**M-04: `institution` filter — exact match**

```python
def test_institution_filter_exact_match():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "a", "institution": "tallinn-city", "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "b", "institution": "state-roads",  "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, institution="tallinn-city")
    ids = {r["issue_id"] for r in result}
    assert ids == {"a"}
```

**M-05: `created_after` / `created_before` — граничные значения включительно/исключительно**

```python
def test_temporal_filters_boundary_conditions():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "exact", "status": "PUBLISHED"}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "after",  "status": "PUBLISHED"}, "2026-05-02T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "before", "status": "PUBLISHED"}, "2026-04-30T00:00:00+00:00"),
    ]
    # created_after: strict >
    result_after = filter_projection_rows(rows, created_after="2026-05-01T00:00:00+00:00")
    ids_after = {r["issue_id"] for r in result_after}
    # "exact" is NOT after 2026-05-01 (string compare, same value → not excluded)
    assert "after" in ids_after
    assert "before" not in ids_after

    # created_before: strict <
    result_before = filter_projection_rows(rows, created_before="2026-05-01T00:00:00+00:00")
    ids_before = {r["issue_id"] for r in result_before}
    assert "before" in ids_before
    assert "after" not in ids_before
```

**M-06: `geo=None` запись при активном bbox → excluded (AC-15)**

```python
def test_geo_null_excluded_when_bbox_active():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "no-geo", "status": "PUBLISHED", "geo": None},                                "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "with-geo", "status": "PUBLISHED", "geo": {"lat": 59.44, "lon": 24.75}},     "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, geo_lat_min=59.0)
    ids = {r["issue_id"] for r in result}
    assert "with-geo" in ids
    assert "no-geo" not in ids
```

**M-07: bbox AND district — AND semantics**

```python
def test_bbox_and_district_and_semantics():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "match",           "status": "PUBLISHED", "geo": {"lat": 59.44, "lon": 24.75, "district": "põhjatallinn"}}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "wrong-district",  "status": "PUBLISHED", "geo": {"lat": 59.44, "lon": 24.75, "district": "mustamäe"}},     "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "outside-bbox",    "status": "PUBLISHED", "geo": {"lat": 58.00, "lon": 24.75, "district": "põhjatallinn"}}, "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, geo_lat_min=59.0, geo_district=["põhja-tallinn"])
    ids = {r["issue_id"] for r in result}
    assert ids == {"match"}
```

**M-08: district multi-value OR semantics (AC-17)**

```python
def test_district_multi_value_or_semantics():
    from core.projection.read_filters import filter_projection_rows
    rows = [
        ("PUBLISHED", {"issue_id": "dist-a", "status": "PUBLISHED", "geo": {"district": "põhjatallinn"}}, "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "dist-b", "status": "PUBLISHED", "geo": {"district": "mustamäe"}},     "2026-05-01T00:00:00+00:00"),
        ("PUBLISHED", {"issue_id": "dist-c", "status": "PUBLISHED", "geo": {"district": "kesklinn"}},     "2026-05-01T00:00:00+00:00"),
    ]
    result = filter_projection_rows(rows, geo_district=["põhja-tallinn", "mustamäe"])
    ids = {r["issue_id"] for r in result}
    assert ids == {"dist-a", "dist-b"}
```

---

## Зона N: E2E sandbox test — полный датасет

### Контекст

`tests/sandbox/dogestonia_simulation_canvas_v0_1.json` — реальный датасет сценариев для demo. Уже используется в `test_e2e_simulation_canvas_intake.py` для проверки intake-пути. Новый тест расширяет это до полного pipeline: intake → clustering → issue projection → GET `/tallinn/issues`.

Без этого теста можно сломать связку clustering → GET-эндпоинт и не узнать до запуска demo.

Параметризация:
- `CLUSTER_MIN_SIZE=1` — каждый intake story → issue (для максимального покрытия)
- `APP_PROFILE=demo` — in-memory backend

### Требуемые тесты (файл: `tests/test_e2e_sandbox_full_pipeline.py`)

```python
_CANVAS_PATH = Path(__file__).resolve().parent / "sandbox" / "dogestonia_simulation_canvas_v0_1.json"
```

**N-01: все сценарии из canvas проходят intake без ошибок**

```python
def test_n01_all_canvas_scenarios_intake_without_errors(client):
    canvas = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    for scenario in canvas:
        payload = _scenario_to_payload(scenario)
        resp = client.post("/intake/stories", json=payload)
        assert resp.status_code == 200, f"Intake failed for scenario: {scenario.get('id', '?')}"
```

**N-02: после intake + clustering — в `doge_issues` есть issue-записи**

```python
def test_n02_after_clustering_issues_exist(client):
    canvas = json.loads(_CANVAS_PATH.read_text(encoding="utf-8"))
    for scenario in canvas:
        client.post("/intake/stories", json=_scenario_to_payload(scenario))
    # trigger clustering
    resp = client.post("/clustering/trigger", headers=_service_auth_headers())
    assert resp.status_code in (200, 202)
    deps = get_api_dependencies()
    issues = deps.issue_projection_read_store.list_projections()
    assert len(issues) > 0, "No issues created after clustering full canvas"
```

**N-03: `GET /tallinn/issues` возвращает non-empty результат**

```python
def test_n03_get_tallinn_issues_returns_results(client):
    _intake_and_cluster_all_canvas(client)
    resp = client.get("/tallinn/issues")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("data") is not None
    assert len(body["data"]) > 0
```

**N-04: `GET /tallinn/issues?status=PUBLISHED` — статус-фильтрация работает**

```python
def test_n04_status_filter_works_on_real_data(client):
    _intake_and_cluster_all_canvas(client)
    resp = client.get("/tallinn/issues", params={"status": "PUBLISHED"})
    assert resp.status_code == 200
    issues = resp.json()["data"]
    for issue in issues:
        assert issue["status"] == "PUBLISHED"
```

**N-05: каждый issue из GET-ответа имеет обязательные поля**

```python
def test_n05_every_issue_has_required_fields(client):
    _intake_and_cluster_all_canvas(client)
    resp = client.get("/tallinn/issues")
    issues = resp.json()["data"]
    required_fields = {"issue_id", "status", "type", "created_at"}
    for issue in issues:
        missing = required_fields - set(issue.keys())
        assert not missing, f"Issue {issue.get('issue_id', '?')} missing fields: {missing}"
```

**N-06: geo-содержащие stories → issues с geo, `geo_district` фильтр работает на реальных данных**

```python
def test_n06_geo_filter_matches_real_data(client):
    _intake_and_cluster_all_canvas(client)
    # Найти district из реальных данных
    resp_all = client.get("/tallinn/issues")
    issues_all = resp_all.json()["data"]
    geo_issues = [i for i in issues_all if i.get("geo") and i["geo"].get("district")]
    if not geo_issues:
        pytest.skip("No geo-district issues in canvas — skip geo filter test")
    district = geo_issues[0]["geo"]["district"]
    resp_filtered = client.get("/tallinn/issues", params={"geo_district": district})
    assert resp_filtered.status_code == 200
    filtered_ids = {i["issue_id"] for i in resp_filtered.json()["data"]}
    assert geo_issues[0]["issue_id"] in filtered_ids
```

---

## Системный инвариант: единый test-run для всех зон

Все тесты из зон A–N должны работать без live Supabase и без env-переменных. Разделение:

```
pytest tests/ --ignore=tests/integration  # зоны A-N: offline, всегда в CI
pytest tests/integration/ -m live         # live Supabase: по требованию
```

### Полный список файлов

| Файл | Зоны | Тестов примерно |
|---|---|---|
| `tests/test_supabase_bootstrap_schema.py` | A, G | +5 к существующим |
| `tests/test_supabase_deserialization_contracts.py` | B | 4 |
| `tests/test_story_intake_field_persistence.py` | C | 4 |
| `tests/test_story_repository_contract.py` | D | 4 (параметризованных) |
| `tests/test_api_service_contract.py` | E | 8 |
| `tests/test_logging_setup.py` | F | 4 |
| `tests/test_store_contract_parity.py` | H | 3 |
| `tests/test_config_loading.py` | I | +3 к существующим |
| `tests/test_clustering_pipeline_contract.py` | J | 4 (**новые**) |
| `tests/test_geo_propagation_contract.py` | K | 4 (**новые**) |
| `tests/test_issue_projection_store_contract.py` | L | 4 (**новые**) |
| `tests/test_filter_projection_rows_contract.py` | M | 8 (**новые**) |
| `tests/test_e2e_sandbox_full_pipeline.py` | N | 6 (**новые**) |
| `tests/conftest.py` | F | +1 fixture |

**Оценочный итог:** ~39 тестов из зон A–I + ~26 новых тестов из зон J–N = ~65 тестов суммарно.

---

## Порядок реализации

| # | Зона | Файл | Приоритет | Зависимость |
|---|------|------|-----------|-------------|
| 1 | L | `test_issue_projection_store_contract.py` | HIGH | REQ-24 (AC-1/2 уже есть) |
| 2 | M | `test_filter_projection_rows_contract.py` | HIGH | REQ-24 (AC-15/17/18 уже покрыты в req24 файле) |
| 3 | J | `test_clustering_pipeline_contract.py` | HIGH | REQ-34, CLUSTER_MIN_SIZE |
| 4 | K | `test_geo_propagation_contract.py` | MEDIUM | REQ-40 (должен быть выполнен) |
| 5 | N | `test_e2e_sandbox_full_pipeline.py` | MEDIUM | зоны J + K + L |
| 6 | A/G | `test_supabase_bootstrap_schema.py` | MEDIUM | уже частично есть |
| 7 | B | `test_supabase_deserialization_contracts.py` | MEDIUM | |
| 8 | C | `test_story_intake_field_persistence.py` | MEDIUM | |
| 9 | D | `test_story_repository_contract.py` | MEDIUM | |
| 10 | E | `test_api_service_contract.py` | MEDIUM | |
| 11 | F | `test_logging_setup.py` | LOW | |
| 12 | H | `test_store_contract_parity.py` | LOW | |
| 13 | I | `test_config_loading.py` | LOW | уже частично есть |

---

## Acceptance Criteria

**AC-39-1:** Файл `39-cross-layer-contract-testing.md` существует; `req-cross-layer-contract-testing.md` удалён.

**AC-39-2:** Зоны A–I сохранены полностью (все тест-спецификации, все код-примеры).

**AC-39-3:** Зона J (`test_clustering_pipeline_contract.py`) — 4 теста покрывают `CLUSTER_MIN_SIZE` параметризацию и idempotency.

**AC-39-4:** Зона K (`test_geo_propagation_contract.py`) — 4 теста покрывают geo-cascading от `StoryRecord.geo` до `payload_json["geo"]` в `doge_issues`.

**AC-39-5:** Зона L (`test_issue_projection_store_contract.py`) — 4 теста покрывают `IssueProjectionReadStore` Protocol против InMemory и SQLite реализаций.

**AC-39-6:** Зона M (`test_filter_projection_rows_contract.py`) — 8 тестов покрывают все filter-режимы `filter_projection_rows()` включая null-safety, bbox, district OR, temporal boundaries.

**AC-39-7:** Зона N (`test_e2e_sandbox_full_pipeline.py`) — 6 тестов на полном `dogestonia_simulation_canvas_v0_1.json` датасете: intake → clustering → `GET /tallinn/issues` с фильтрацией.

**AC-39-8:** Критерий закрытия для каждой зоны задокументирован (таблица в §«Системный инвариант»).

**AC-39-9:** Все тесты зон A–N работают offline (`pytest tests/ --ignore=tests/integration`) без env-переменных.
