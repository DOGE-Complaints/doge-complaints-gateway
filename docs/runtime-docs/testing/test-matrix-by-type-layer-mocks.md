# Тестовая матрица: типы, слои, scope, моки

## Контекст и управленческий вопрос

Ключевой вопрос для CTO-уровня:  
**какую степень уверенности дает текущий тестовый портфель по архитектурным слоям и критическим runtime сценариям, и где расположены зоны остаточного риска?**

Последнее обновление: 2026-05-07 (211 passed, 9 skipped)

---

## Current state

### 1) Профиль стратегии тестирования

Текущий набор тестов строится вокруг четырёх целей:

1. Зафиксировать архитектурные инварианты (layer boundaries, DI wiring).
2. Подтвердить контрактность ключевых payload/error моделей.
3. Проверить in-process поведение сервисов на happy-path и важных негативных ветках.
4. Валидировать story-first cluster pipeline (cron, living issues, signal extraction, civic lenses).

Сильная сторона: высокая дисциплина contract/unit/integration; civic taxonomy (req26) и living issues (req29) покрыты отдельными тест-сьютами.  
Ограничение: Supabase live bucket остаётся opt-in (env-dependent); нет remote API тестирования против задеплоенного приложения.

---

### 2) Matrix by type and scope

#### Unit / Contract

| Test file | Type | Layer / scope | Что проверяет |
|-----------|------|---------------|---------------|
| `test_config_loading.py` | unit | config | Env contract, defaults (включая civic lenses, MIN_SIZE=5) |
| `test_layer_guardrails.py` | unit/guardrail | architecture | Контроль дрейфа зависимостей между слоями |
| `test_story_intake_contract.py` | contract | intake schema | Валидность intake parser/response |
| `test_error_envelope_contract.py` | contract | API envelope | Стабильность error envelope taxonomy |
| `test_signal_profile_schema.py` | unit | profile schema | Signal dimension contract |
| `test_signal_profile_quality_validation.py` | unit | profile quality | Validation rule correctness |
| `test_signal_vocabulary.py` | unit | cluster vocabulary | CIVIC_DOMAIN, FAILURE_PATTERN, CIVIC_SIGNAL completeness |
| `test_clustering_engine.py` | unit | cluster engine | SHA-256 детерминизм, readiness formula, AC-02/03/05/06 |
| `test_gw_ssr_18_cluster_active_schema.py` | unit | cluster orchestrator | pack iff persist == `NODE_SCHEMA_*`; mismatch skip; unbound civic |
| `test_doge_issue_projection.py` | unit/contract | issue projection | Projection happy-path, locale fallback, unknown label rejection |
| `test_translation_locale_differentiation.py` | unit | projection locale | Locale field preservation (title/description) |
| `test_unit_branch_closure_by_layer.py` | unit | API + application | trace_id generation, empty cluster_id/story_ids rejection |
| `test_unit_domain_flows_supabase_wave.py` | unit | domain | whitespace story_ids, label derivation determinism, issue_type default |
| `test_supabase_bootstrap_schema.py` | unit/contract | Supabase schema | cluster_memberships, story_signals tables + RLS policies in bootstrap SQL |

#### Integration (in-process)

| Test file | Type | Layer / scope | Что проверяет |
|-----------|------|---------------|---------------|
| `test_bootstrap_smoke.py` | smoke | bootstrap + API wiring | Базовый runtime поднимается |
| `test_di_service_factory.py` | integration | infrastructure → application | Service wiring completeness |
| `test_api_security_and_ops.py` | integration | API security + metrics | Service auth и ops counters |
| `test_api_route_edges.py` | integration | API route edges | Degraded readiness path, demo auth routes, config error 500 |
| `test_http_transport_smoke.py` | integration (transport) | FastAPI routes | HTTP 401/200, content-type, envelope shape |
| `test_http_intake_endpoint.py` | integration (transport) | Intake HTTP | `POST /intake/stories` 200/400, trace behavior |
| `test_http_issue_create_endpoint.py` | integration (transport) | story-first cleanup | `POST /issues` → 404 (endpoint removed) |
| `test_openapi_runtime_compliance.py` | integration | OpenAPI spec | Required paths present, response contract matches envelope |
| `test_story_intake_idempotency.py` | integration | application + repository | Идемпотентность intake |
| `test_story_repository_lifecycle.py` | integration | lifecycle | Переходы story статусов |
| `test_signal_profile_enrichment_and_versioning.py` | integration | profile service | Enrichment versioning |
| `test_signal_extraction_canonical.py` | integration | canonical extraction | Language neutrality, civic_weight priority, hybrid fallback |
| `test_story_cluster_orchestrator.py` | integration | cluster orchestrator | Signal caching, no-duplicate issue, primary lens from config, lifecycle advance |
| `test_issue_create_service.py` | integration | issue create | create→extend reuse, idempotent extend |
| `test_issue_promotion_service.py` | integration | promotion | Gate logic, state transitions, extend_candidate dedup |
| `test_story_promotion_projection_bridge.py` | integration + contract | Story/Promotion → Projection | Deterministic mapping, edge-case errors |
| `test_story_signal_store.py` | integration | signal persistence | InMemory read-after-write, SQLite persistence, policy isolation |
| `test_embedding_policy_versioning.py` | unit/integration | embedding | Canonical source + policy version |
| `test_geo_intelligence.py` | integration | geo pipeline | Cache/fallback/retry behavior |
| `test_geo_candidate_persistence_roundtrip.py` | integration | geo + persistence | GeoSnapshot roundtrip on StoryRecord, IssueCandidateStore SQLite roundtrip |
| `test_evidence_pack.py` | integration + contract | evidence/lineage | Lineage integrity, redaction tiers |
| `test_adapters_demo_pilot.py` | integration | adapters | Stub adapter determinism by profile |
| `test_trace_propagation.py` | integration | observability | Trace continuity success/error |
| `test_intake_observability.py` | unit/integration | intake telemetry | Error classification + telemetry |
| `test_asgi_lifespan_cron.py` | integration | cron lifecycle | Cron не стартует при `CLUSTER_CRON_ENABLED=false` |
| `test_cluster_cron_job.py` | integration | cron job | Start/stop loop, min_size guard, idempotent start |
| `test_cluster_active_lenses_runtime_effect.py` | integration | cluster config | `node_clustering.civic.active_lenses` активного pack меняет prefix `cluster_id` (не env `CLUSTER_ACTIVE_LENSES`) |
| `test_db_backend_switching.py` | integration | infra/config | Корректный switch in_memory/sqlite/supabase |
| `test_process_linkage_sqlite.py` | integration | persistence | SQL persistence issue_candidates/review_audit_log/issue_story_links |
| `test_integration_cross_layer_api_app_infra.py` | integration | cross-layer | Side-effects roundtrip через все три слоя |

#### E2E (in-process, full pipeline)

| Test file | Type | Layer / scope | Что проверяет |
|-----------|------|---------------|---------------|
| `test_e2e_create_story_fullpath.py` | e2e | intake → story create | Full path с idempotency и materialization, invalid payload rejection |
| `test_e2e_intake_create_doge_issue_contract.py` | e2e/contract | intake → cluster → issue | Сквозной contract gate story-first pipeline |
| `test_e2e_story_cluster_issue_pipeline.py` | e2e | story-cluster → issue | Happy-path + living issues two-batch reuse |
| `test_e2e_story_package_cluster_deterministic.py` | e2e | story package → cluster | Детерминизм кластеризации для одинаковых пакетов |
| `test_e2e_story_package_issue_tracking.py` | e2e | story package → audit | Materialization + audit trail |
| `test_db_backed_pipeline_e2e.py` | e2e/integration | DB backend parity | Story-first pipeline на SQLite (living issue, extend, audit) |

#### Live / Supabase (skip-safe, env-dependent)

| Test file | Type | Layer / scope | Что проверяет |
|-----------|------|---------------|---------------|
| `integration/supabase/test_supabase_live_smoke.py` | live/smoke | Supabase connectivity | Live путь при наличии env + миграций |
| `integration/supabase/test_spa_projection_supabase_roundtrip.py` | live | projection roundtrip | Сохранение/чтение projection в live Supabase |
| `integration/supabase/test_supabase_live_story_roundtrip.py` | live | story roundtrip | Story CRUD в live Supabase |
| `integration/supabase/test_supabase_live_story_embedding_roundtrip.py` | live | story embedding | StoryEmbedding persistence в live Supabase |
| `integration/supabase/test_supabase_live_full_pipeline_roundtrip.py` | live | full pipeline | Сквозной live pipeline через Supabase |
| `integration/supabase/test_supabase_live_missing_adapters_roundtrip.py` | live | missing adapters | Graceful degradation без адаптеров |
| `integration/supabase/test_rls_policy_validation.py` | live | RLS policies | Row-level security enforcement |
| `integration/supabase/test_supabase_ready_endpoint_shape.py` | live | readiness endpoint | /ready response shape при Supabase backend |
| `integration/supabase/test_supabase_required_columns_ready_live.py` | live | schema columns | Required columns present в live DB |

---

### 3) Coverage by layer and business capability

| Слой | Тесты | Confidence |
|------|-------|-----------|
| Bootstrap / composition | `test_bootstrap_smoke`, `test_di_service_factory` | ✅ Высокий |
| Config / env contract | `test_config_loading` | ✅ Высокий |
| API boundary (routes, auth, envelope) | `test_api_security_and_ops`, `test_http_transport_smoke`, `test_http_intake_endpoint`, `test_http_issue_create_endpoint`, `test_api_route_edges`, `test_openapi_runtime_compliance`, `test_error_envelope_contract`, `test_trace_propagation` | ✅ Высокий |
| Architecture guardrails | `test_layer_guardrails`, `test_unit_branch_closure_by_layer` | ✅ Высокий |
| Intake / lifecycle / idempotency | `test_story_intake_*`, `test_story_repository_lifecycle`, `test_e2e_create_story_fullpath` | ✅ Высокий |
| Cluster engine (civic taxonomy) | `test_clustering_engine`, `test_signal_vocabulary`, `test_signal_extraction_canonical`, `test_story_cluster_orchestrator`, `test_cluster_active_lenses_runtime_effect` | ✅ Высокий |
| Cron / background processing | `test_cluster_cron_job`, `test_asgi_lifespan_cron` | ✅ Высокий |
| Living issues / extend | `test_issue_create_service`, `test_e2e_story_cluster_issue_pipeline`, `test_db_backed_pipeline_e2e` | ✅ Высокий |
| Signal persistence | `test_story_signal_store`, `test_supabase_bootstrap_schema` | ✅ Высокий |
| Projection / locale | `test_doge_issue_projection`, `test_translation_locale_differentiation`, `test_story_promotion_projection_bridge`, `test_embedding_policy_versioning` | ✅ Высокий |
| DB persistence (SQLite) | `test_db_backend_switching`, `test_db_backed_pipeline_e2e`, `test_process_linkage_sqlite`, `test_geo_candidate_persistence_roundtrip` | ✅ Высокий |
| DB persistence (Supabase live) | `integration/supabase/*` | ⚠️ Env-dependent |
| Geo pipeline | `test_geo_intelligence`, `test_geo_candidate_persistence_roundtrip` | ✅ Средний |
| Remote API (задеплоенное приложение) | — | ❌ Отсутствует |

---

### 4) Mocks / stubs / in-memory doubles

#### In-memory repositories

- `src/core/infrastructure/repositories.py` — `InMemoryHealthRepository`, `InMemoryStoryRepository`, `InMemoryIdempotencyRepository`, `InMemorySignalProfileRepository`
- `src/core/evidence/repositories.py` — `InMemoryEvidencePackRepository`
- `src/core/promotion/repositories.py` — `InMemoryIssueCandidateStore`, `InMemoryReviewAuditLogRepository`
- `src/core/geo/repositories.py` — `InMemoryGeoCacheRepository`

Роль: тестировать бизнес-логику без I/O и flaky внешних систем.

#### Provider / adapter stubs

- `src/core/geo/providers.py` — `_TallinnOpenCageStub`, `_NarvaNominatimStub`
- `src/core/adapters/demo.py` — `DemoWalletPushAdapter`, `DemoSignRequestAdapter`, `DemoTxBroadcastAdapter`

Роль: детерминированный baseline для geo/chain сценариев.

#### Test-local doubles

- `_OkService` в `test_api_security_and_ops.py`
- `_FlakyProvider` в `test_geo_intelligence.py`

---

## Risk zones

- **Remote API тестирование** — полностью отсутствует. Нет способа прогнать симуляционные сценарии против задеплоенного приложения. See: `docs/analysis/remote-api-simulation-gap-2026-05-07.md`
- Live Supabase тесты зависят от внешнего окружения — skip в локальном прогоне без `.env`.
- Нет browser-level e2e (покрыт только API transport через `TestClient`).
- Нет chaos/failure-injection тестов для rollback runbook.

---

## Контрольные команды

```bash
# Полный локальный прогон
.venv/bin/python -m pytest tests/ -q  # 211 passed, 9 skipped

# Core regression (быстрый gate)
.venv/bin/python -m pytest tests/test_layer_guardrails.py tests/test_di_service_factory.py \
  tests/test_api_security_and_ops.py tests/test_story_repository_lifecycle.py \
  tests/test_clustering_engine.py -q

# DB-backed pipeline quality gate
.venv/bin/python -m pytest tests/test_db_backend_switching.py tests/test_db_backed_pipeline_e2e.py \
  tests/test_process_linkage_sqlite.py tests/test_story_signal_store.py -q

# Live Supabase (requires .env with SUPABASE_URL + SUPABASE_SERVICE_ROLE)
.venv/bin/python -m pytest tests/integration/supabase -q

# Канонический оффлайн-гейт (без живого Supabase/сети)
.venv/bin/python -m pytest -m "not live_integration" -q
```

---

## Local real-HTTP smoke tests (`tests/smoke/*`) и канонический оффлайн-гейт

> Verified по [`tests/smoke/conftest.py`](../../../tests/smoke/conftest.py). Публичные пути — `/node/…` (не `/tallinn/…`).

### Как выбирается цель

- Conftest читает `.env.test` (**overwrite=True**), затем `.env` без overwrite.
- Цель = `GATEWAY_URL`. Пусто → `pytest.fail` («must be set»).
- Host не localhost / `127.0.0.1` / `::1` → **skip** (не hosted Railway).
- До suite: `GET {GATEWAY_URL}/health`. Нет 200 или сеть недоступна → skip.

Service-токен (`GATEWAY_API_TOKEN` или `SERVICE_API_TOKEN`) нужен только intake/stash-кейсам. User-токен (email/password + Supabase anon) — только submit. Public GET (`/health`, `/ready`, `/node/issues`, Pulse, Emerging) токен не требуют.

### Что покрывает `test_local_server_smoke.py`

| Тест | Запрос | Ожидание |
|------|--------|----------|
| ls01 | `GET /health` | 200 |
| ls01b | `GET /ready` | 200, `data.status` = `ready` или `degraded` |
| ls04 | `GET /node/issues` | 200, `data.issues` — список |
| ls04b | `GET /node/issues/{id}` | нет id → 404; если list непустой — 200 и `data.issue` |
| ls04c | `GET /node/network-pulse` | 200, не карточки issues |
| ls04d | `GET /node/emerging-signals` | 200, `data.signals` |
| ls04e | `GET /tallinn/issues` | 404 |

Intake-кейсы ls02/ls03/ls05/ls06 — живой stash+submit; без токенов skip. Canvas / smoke payload **`schema_binding` = env сервера** (`NODE_SCHEMA_ID` + `NODE_SCHEMA_VERSION` процесса). Чужой pack или отсутствие binding → 4xx (SSR-17), не civic.

### Как прогнать

1. Поднять сервер: [`server-env-quickstart.md`](../manuals/server-env-quickstart.md) (`make serve`).
2. В `.env.test`: `GATEWAY_URL=http://127.0.0.1:8000` (тот же порт, что у uvicorn).
3. Для intake-smoke — тот же `SERVICE_API_TOKEN`, что у сервера; для submit ещё user+Supabase.

```bash
cd doge-complaints-gateway
make serve
# другой терминал:
.venv/bin/python -m pytest tests/smoke/test_local_server_smoke.py -q
.venv/bin/python -m pytest tests/smoke -q
```

Только health + public `/node` без intake: те же ls01/ls01b/ls04*.

### Оффлайн-гейт (`pytest -m "not live_integration"`)

Сетевые smoke **не** помечены `live_integration`. Если в `.env.test` висит `GATEWAY_URL`, suite может skip/fail по сети. Обход: `GATEWAY_URL= .venv/bin/python -m pytest -m "not live_integration" -q`.
