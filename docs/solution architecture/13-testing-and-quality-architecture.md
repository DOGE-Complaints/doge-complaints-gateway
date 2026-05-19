# 13. Testing & Quality Architecture

Дата последнего обновления: 2026-05-18  
Счётчик тестов: **431** collected · **410** pass offline (`pytest -m "not live_integration"`) · **11** smoke skip без `LOCAL_SERVER_URL` · **10** live (`pytest -m live_integration`, требуют Supabase secrets)  
Связанные требования: REQ-39 (cross-layer contracts), REQ-41 (production coverage target state)  
Исполнение REQ-41: EPIC-M2-18 stories 03–05, operative queue [`pkg-000021`](../tasks/gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml)

---

## 1. Архитектура тест-слоёв

```
┌─────────────────────────────────────────────────────────────────────┐
│  LAYER 6 — Real HTTP / Local Server (opt-in, ручной запуск)         │
│  tests/smoke/                                                       │
│  Транспорт: httpx.Client / httpx.AsyncClient → TCP-сокет            │
│  Требует: LOCAL_SERVER_URL (uvicorn запускается пользователем)       │
│  Без переменной: pytest.skip — offline suite не ломается            │
│  Покрывает: реальный HTTP-стек, uvicorn middleware, response headers │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 5 — Live Supabase Integration (opt-in, requires secrets)     │
│  tests/integration/supabase/                                        │
│  10 файлов · пропускаются без SUPABASE_TEST_URL                     │
│  Marker: `live_integration` · CI: `.github/workflows/integration-live.yml` (main) │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 4 — HTTP E2E / SQLite Backend                                │
│  test_db_backed_pipeline_e2e.py                                     │
│  test_integration_cross_layer_api_app_infra.py                      │
│  Транспорт: TestClient · БД: SQLite (реальная) · Cron: disabled     │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 3 — HTTP E2E / In-Memory Backend                             │
│  ~50+ файлов — основная масса (см. §3)                              │
│  Транспорт: FastAPI TestClient · БД: InMemory · Cron: disabled      │
│  Включает: REQ-24, REQ-33–40, sandbox, simulation canvas            │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 2 — Domain Integration (offline, no HTTP)                    │
│  test_e2e_story_cluster_issue_pipeline.py                           │
│  test_e2e_story_package_cluster_deterministic.py                    │
│  test_stories_schema_cross_layer_invariant.py                       │
│  test_process_linkage_sqlite.py                                     │
│  Прямые вызовы application-слоя · нет TestClient                    │
├─────────────────────────────────────────────────────────────────────┤
│  LAYER 1 — Unit / Smoke                                             │
│  test_bootstrap_smoke.py · test_asgi_lifespan_cron.py               │
│  test_openapi_runtime_compliance.py · test_api_security_and_ops.py  │
│  Изоляция: нет БД, нет HTTP, нет внешних I/O                       │
└─────────────────────────────────────────────────────────────────────┘
```

**Команда запуска offline suite (как CI, без Layer 5 live marker):**
```bash
python3 -m pytest -q -m "not live_integration"
```

**Полный локальный прогон (Layer 5 skip без secrets, Layer 6 skip без LOCAL_SERVER_URL):**
```bash
python3 -m pytest tests/ -q
```

**Команда запуска local server suite (Layer 6, после ручного старта uvicorn):**
```bash
# Шаг 1 — запустить сервер в отдельном терминале:
APP_PROFILE=demo DB_BACKEND=in_memory CLUSTER_CRON_ENABLED=false \
  .venv/bin/python -m uvicorn core.api.asgi_app:app --host 127.0.0.1 --port 8000

# Шаг 2 — запустить smoke suite:
LOCAL_SERVER_URL=http://127.0.0.1:8000 .venv/bin/python -m pytest tests/smoke/ -v
```

---

## 2. Конфигурация среды — conftest.py

**`_block_dotenv_leakage`** (autouse, session-scope): принудительно устанавливает:
- `DB_BACKEND=in_memory` — предотвращает случайный доступ к prod/staging БД
- `SUPABASE_URL=""`, `SUPABASE_SERVICE_ROLE=""` — блокирует Supabase HTTP
- `CLUSTER_CRON_ENABLED=false` — отключает фоновый поток в тестах
- `CLUSTER_MIN_SIZE=2`, `CLUSTER_READINESS_THRESHOLD=60` — стабильные дефолты

**`_pytest_session_logging`** (autouse): настраивает root logger из `LOG_LEVEL` env (default: WARNING).

**`configured_logging`** (opt-in fixture): DEBUG log capture для тестов observability.

Live-тесты переопределяют эти дефолты через `monkeypatch.setenv()` в своих fixture.

---

## 3. Полный реестр тест-файлов по слоям

### Layer 1 — Unit / Smoke

| Файл | Что тестирует | REQ |
|------|---------------|-----|
| `test_bootstrap_smoke.py` | Импорт модулей, нет circular deps | — |
| `test_asgi_lifespan_cron.py` | ASGI startup/shutdown, cron lifecycle | REQ-28 |
| `test_openapi_runtime_compliance.py` | OpenAPI schema генерируется без ошибок | REQ-32 |
| `test_api_security_and_ops.py` | API key, rate limit headers, health endpoint | REQ-32 |
| `test_layer_guardrails.py` | Инфра не импортирует domain напрямую | — |
| `test_config_loading.py` | `load_app_config()` из env | — |
| `test_logging_setup.py` | Logger factory, structured log shape | REQ-37 |

### Layer 2 — Domain Integration (offline, no HTTP)

| Файл | Что тестирует | REQ |
|------|---------------|-----|
| `test_e2e_story_cluster_issue_pipeline.py` | Orchestrator → IssueCreateService → Issue | REQ-34 |
| `test_e2e_story_package_cluster_deterministic.py` | Детерминированность кластеризации | REQ-25 |
| `test_stories_schema_cross_layer_invariant.py` | `StoryRecord` поля инвариантны | REQ-33 |
| `test_process_linkage_sqlite.py` | SQLite issue_story_links persistence | REQ-38 |
| `test_issue_create_service.py` | `IssueCreateService` unit | — |
| `test_issue_promotion_service.py` | `IssuePromotionService` promotion gates | — |
| `test_story_cluster_orchestrator.py` | `StoryClusterOrchestrator` unit | REQ-34 |
| `test_clustering_engine.py` | `ClusteringEngine` lens selection | REQ-25/34 |
| `test_cluster_active_lenses_runtime_effect.py` | Lens env config → кластерный результат | REQ-34 |
| `test_cluster_cron_job.py` | `ClusterCronJob` start/stop/timing (stub) | REQ-28 |
| `test_signal_extraction_canonical.py` | Signal extraction pipeline | REQ-34 |
| `test_signal_profile_enrichment_and_versioning.py` | Signal profile enrichment | REQ-34 |
| `test_signal_profile_quality_validation.py` | Signal quality gates | REQ-34 |
| `test_signal_profile_schema.py` | Signal schema validation | REQ-34 |
| `test_signal_vocabulary.py` | Canonical vocabulary terms | REQ-34 |
| `test_geo_intelligence.py` | Geo resolver, cache, fallback | REQ-35 |
| `test_alpha_score.py` | Alpha scoring function | REQ-36 |
| `test_evidence_pack.py` | Evidence pack assembly | — |
| `test_doge_issue_projection.py` | `IssueProjectionService` derivation | REQ-27 |
| `test_projection_canonical_derivation.py` | Canonical type/labels derivation | REQ-34 |
| `test_promotion_canonical_type_gate.py` | Type gate in promotion | — |
| `test_story_promotion_projection_bridge.py` | `StoryPromotionProjectionBridge` | REQ-40 |
| `test_geo_propagation_contract.py` | Geo cascade: StoryRecord → DOGEIssue | REQ-40 |
| `test_story_repository_contract.py` | `StoryRepository` Protocol contract | — |
| `test_story_repository_lifecycle.py` | Story lifecycle state machine | — |
| `test_issue_projection_store_contract.py` | `IssueProjectionReadStore` × 2 impls | REQ-39-L |
| `test_store_contract_parity.py` | In-memory/SQLite parity | REQ-39-H |

### Layer 3 — HTTP E2E / In-Memory Backend

| Файл | Что тестирует | REQ |
|------|---------------|-----|
| `test_http_intake_endpoint.py` | `POST /intake/stories` HTTP contract | REQ-33 |
| `test_http_issue_create_endpoint.py` | Issue create HTTP | — |
| `test_http_transport_smoke.py` | Transport smoke | — |
| `test_e2e_create_story_fullpath.py` | Intake fullpath E2E | — |
| `test_e2e_intake_create_doge_issue_contract.py` | Intake → issue contract | REQ-27 |
| `test_e2e_sandbox_full_pipeline.py` | Sandbox 130 canvas scenarios E2E | REQ-39-N |
| `test_e2e_simulation_canvas_intake.py` | Canvas simulation intake | — |
| `test_e2e_story_package_issue_tracking.py` | Story package tracking | — |
| `test_req24_tallinn_issues_read_api.py` | `GET /tallinn/issues` 23 tests | REQ-24 |
| `test_req35_geo_scope_and_filter.py` | Geo filter (district/bbox/country) | REQ-35 |
| `test_req37_pipeline_observability_pii.py` | PII scrubbing, trace propagation | REQ-37 |
| `test_req38_data_integrity.py` | Issue-story links integrity | REQ-38 |
| `test_req40_geo_propagation.py` | Geo propagation to issue (HTTP path) | REQ-40 |
| `test_story_intake_contract.py` | Intake contract (schema, fields) | REQ-33 |
| `test_story_intake_field_persistence.py` | Field persistence roundtrip | REQ-33 |
| `test_story_intake_idempotency.py` | Idempotency-key deduplication | REQ-33 |
| `test_story_intake_live_context_not_on_record.py` | Live context not persisted | REQ-33 |
| `test_clustering_pipeline_contract.py` | Clustering pipeline stitch J-01..J-04 | REQ-39-J |
| `test_filter_projection_rows_contract.py` | Filter engine M-01..M-12 | REQ-39-M |
| `test_supabase_issue_projection_store_contract.py` | Supabase store HTTP mock (offline) | REQ-39-L |
| `test_api_route_edges.py` | API edge cases (404, 422, etc.) | — |
| `test_api_service_contract.py` | API ↔ service contract | — |
| `test_error_envelope_contract.py` | Error envelope shape | — |
| `test_adapters_demo_pilot.py` | Demo/pilot profile switching | — |
| `test_di_service_factory.py` | DI factory correctness | — |
| `test_db_backend_switching.py` | `DB_BACKEND` env switch | — |
| `test_db_supabase_jsonb_reads.py` | Supabase JSONB deserialization | — |
| `test_geo_candidate_persistence_roundtrip.py` | Geo candidate store roundtrip | REQ-35 |
| `test_embedding_policy_versioning.py` | Embedding version tagging | — |
| `test_intake_observability.py` | Intake structured logs | REQ-37 |
| `test_trace_propagation.py` | Trace-ID header propagation | REQ-37 |
| `test_translation_locale_differentiation.py` | EN/ET locale handling | REQ-33 |
| `test_story_signal_store.py` | Signal store persistence | REQ-34 |
| `test_supabase_bootstrap_schema.py` | DDL/bootstrap SQL offline | — |
| `test_supabase_deserialization_contracts.py` | Supabase deserialization | — |
| `test_supabase_observability.py` | Supabase HTTP observability | REQ-37 |
| `test_unit_branch_closure_by_layer.py` | Branch closure unit | — |
| `test_unit_domain_flows_supabase_wave.py` | Domain flows (Supabase wave) | — |

### Layer 6 — Real HTTP / Local Server (opt-in)

Требует локально запущенного `uvicorn` (пользователь запускает вручную). Guard: `pytest.skip("LOCAL_SERVER_URL not set")`.

**Источник тестовых данных**: `tests/sandbox/dogestonia_simulation_canvas_v0_1.json` (130 сценариев, 4 группы).  
Тесты используют `_scenario_to_payload()` из `tests/simulation_runner.py` для конвертации canvas-сценариев в intake payloads — те же реальные Таллиннские civic-истории что и в E2E sandbox suite (Layer 3 Zone N).

| Файл | Что тестирует | GAP |
|------|---------------|-----|
| `tests/smoke/test_local_server_smoke.py` | intake с canvas-сценариями по группам, `/health`, headers, error envelope через реальный HTTP | GAP-41-01 |
| `tests/smoke/test_local_server_async_read.py` | `GET /tallinn/issues` через `httpx.AsyncClient` после sandbox intake, параллельные запросы | GAP-41-06 |

Дополнительно offline (REQ-41, Layer 3):

| Файл | Что тестирует | GAP |
|------|---------------|-----|
| `test_cron_clustering_timing_contract.py` | Cron timing CT-01..03, real orchestrator + lifespan | GAP-41-02 |
| `test_concurrent_intake_contract.py` | Concurrent intake CC-01..02 | GAP-41-03 |
| `test_config_env_only_contract.py` | Env-only config CE-01..03 (subprocess) | GAP-41-04 |

---

### Layer 4 — HTTP E2E / SQLite Backend

| Файл | Что тестирует | REQ |
|------|---------------|-----|
| `test_db_backed_pipeline_e2e.py` | Full pipeline с SQLite БД | — |
| `test_integration_cross_layer_api_app_infra.py` | Cross-layer API + infra (SQLite) | REQ-39 |

### Layer 5 — Live Supabase Integration (opt-in)

Все файлы помечены `live_integration` (см. `tests/conftest.py` → `pytest_collection_modifyitems`). Пропускаются (`pytest.skip`) если `SUPABASE_TEST_URL` / `SUPABASE_TEST_SERVICE_ROLE` не установлены.

| Файл | Что тестирует |
|------|---------------|
| `test_supabase_live_full_pipeline_roundtrip.py` | Полный pipeline: intake → cluster → issue → GET (Supabase) |
| `test_supabase_live_story_roundtrip.py` | Story CRUD через Supabase |
| `test_supabase_live_missing_adapters_roundtrip.py` | Partial adapter roundtrip |
| `test_supabase_live_story_embedding_roundtrip.py` | Embedding persistence в Supabase |
| `test_rls_policy_validation.py` | RLS-политики для всех таблиц |
| `test_supabase_required_columns_ready_live.py` | `required_columns_ready()` live check |
| `test_supabase_ready_endpoint_shape.py` | `/ready` endpoint против Supabase |
| `test_supabase_dotenv_connectivity.py` | Connectivity smoke (dotenv-based) |
| `test_spa_projection_supabase_roundtrip.py` | SPA projection Supabase roundtrip |

---

## 4. SEAM-зоны и тест-контракты (REQ-39)

REQ-39 определяет 14 SEAM-зон (A–N) для contract-тестирования между слоями:

| SEAM | Граница | Ключевой тест-файл |
|------|---------|--------------------|
| A | HTTP ↔ SupabaseDatabase | `test_supabase_bootstrap_schema.py` |
| B | SupabaseDatabase ↔ StoryRepository | `test_supabase_deserialization_contracts.py` |
| C–I | Intake pipeline zones | `test_story_intake_contract.py` и др. |
| J | StoryClusterOrchestrator → IssueCreateService → Store | `test_clustering_pipeline_contract.py` |
| K | StoryRecord.geo → DOGEIssue.geo | `test_geo_propagation_contract.py` |
| L | IssueProjectionReadStore Protocol ↔ 3 реализации | `test_issue_projection_store_contract.py` + `test_supabase_issue_projection_store_contract.py` |
| M | `filter_projection_rows()` engine | `test_filter_projection_rows_contract.py` |
| N | E2E sandbox (130 scenarios) | `test_e2e_sandbox_full_pipeline.py` |

Полная спецификация: `docs/requirements/39-cross-layer-contract-testing.md`

---

## 5. Quality gates (текущие)

- **Type checking**: `pyright` (strict mode) — все модули `src/core/`
- **Linting**: `ruff` — pre-commit hook
- **Test suite**: 410 offline pass (`-m "not live_integration"`), opt-in live (10) + smoke (11 skip)
- **CI offline**: `.github/workflows/test-offline.yml` — `pytest -m "not live_integration"`
- **CI live**: `.github/workflows/integration-live.yml` — `pytest -m live_integration` on `main` (secrets `SUPABASE_TEST_URL`, `SUPABASE_TEST_SERVICE_ROLE_KEY`)
- **No dotenv leakage**: `_block_dotenv_leakage` autouse блокирует prod credentials
- **Policy version**: `m3.doge_issue_derivation.v1` — верифицирован тестом J-03
- **OpenAPI compliance**: runtime schema validation в каждом PR
- **PII safety**: structured log scrubbing верифицирован REQ-37 тестами

---

## 6. Матрица продакшн-сценариев PS-01..PS-25 (REQ-41, AC-41-8)

Источник сценариев: [`41-testing-production-coverage-target-state.md`](../requirements/41-testing-production-coverage-target-state.md) §2.  
Статус **covered** = есть автоматизированный тест; **CI** = обязателен в `integration-live` workflow при настроенных secrets.

| PS | Сценарий (кратко) | Layer | Тест-файл(ы) | Статус |
|----|-------------------|-------|--------------|--------|
| PS-01 | Canvas intake на реальный HTTP | 6 | `tests/smoke/test_local_server_smoke.py` (LS-02..03) | covered (opt-in `LOCAL_SERVER_URL`) |
| PS-02 | Intake + geo persistence | 3 | `test_http_intake_endpoint.py`, `test_story_intake_field_persistence.py` | covered |
| PS-03 | Stories накапливаются за интервал | 3 | `test_cron_clustering_timing_contract.py` (CT-02) | covered |
| PS-04 | Cron interval → кластеризация | 3 | `test_cron_clustering_timing_contract.py` (CT-01, CT-03) | covered |
| PS-05 | CLUSTER_MIN_SIZE threshold | 3 | `test_clustering_pipeline_contract.py` (J-01) | covered |
| PS-06 | Issue в `doge_issues` после порога | 3 | `test_clustering_pipeline_contract.py` (J-02) | covered |
| PS-07 | GET /tallinn/issues | 3 | `test_req24_tallinn_issues_read_api.py` | covered |
| PS-08 | status=PUBLISHED filter | 3 | `test_req24_tallinn_issues_read_api.py` | covered |
| PS-09 | geo_district filter | 3 | `test_req35_geo_scope_and_filter.py`, `test_filter_projection_rows_contract.py` | covered |
| PS-10 | bbox filter null-safety | 3 | `test_filter_projection_rows_contract.py` (M-06) | covered |
| PS-11 | Параллельный intake | 3 | `test_concurrent_intake_contract.py` (CC-01..02) | covered |
| PS-12 | Idempotency-key dedup | 3 | `test_story_intake_idempotency.py`, `test_api_service_contract.py` | covered |
| PS-13 | RLS live | 5 | `test_rls_policy_validation.py` | covered + **CI** |
| PS-14 | Supabase full roundtrip | 5 | `test_supabase_live_full_pipeline_roundtrip.py` | covered + **CI** |
| PS-15 | policy_version в issue | 3/4 | `test_clustering_pipeline_contract.py` (J-03, SQLite) | covered |
| PS-16 | geo → issue payload | 3 | `test_geo_propagation_contract.py`, `test_req40_geo_propagation.py` | covered |
| PS-17 | CLUSTER_READINESS_THRESHOLD | 3 | `test_clustering_pipeline_contract.py` (J-01) | covered |
| PS-18 | Railway env-only config | 3 | `test_config_env_only_contract.py` (CE-01..03) | covered |
| PS-19 | Реальный HTTP-стек (uvicorn) | 6 | `tests/smoke/test_local_server_smoke.py` (LS-01, LS-04..06) | covered (opt-in) |
| PS-20 | OpenAPI runtime compliance | 1 | `test_openapi_runtime_compliance.py` | covered |
| PS-21 | Trace / request correlation | 3/6 | `test_trace_propagation.py`, smoke LS-06 | covered |
| PS-22 | PII scrubbing в логах | 3 | `test_req37_pipeline_observability_pii.py` | covered |
| PS-23 | Sandbox 130 scenarios E2E | 3 | `test_e2e_sandbox_full_pipeline.py` (N-01..06) | covered |
| PS-24 | Embedding policy version | 3 | `test_embedding_policy_versioning.py` | covered |
| PS-25 | required_columns_ready live | 5 | `test_supabase_required_columns_ready_live.py` | covered + **CI** |

**Итог REQ-41:** 25/25 сценариев имеют автоматизированное покрытие; Layer 5 и Layer 6 — opt-in (secrets / `LOCAL_SERVER_URL`).  
**Оператор Layer 6:** см. §1 — uvicorn вручную, затем `LOCAL_SERVER_URL=http://127.0.0.1:8000 pytest tests/smoke/`.

---

## 7. История расширений (Pilot → REQ-41)

REQ-41 реализован в EPIC-M2-18 (stories M2-18-03..05, `pkg-000021`). Прежний план расширения (Layer 6, offline gaps, CI) перенесён в матрицу §6 и закрыт кодом.
