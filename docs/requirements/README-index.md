# Module 2 Requirements Pack (Product + CTO)

Этот каталог содержит детализированную декомпозицию PDF `DOGEstonia — Module 2 Canvas: Web2 Core / Story Intelligence Layer`.

Дополнительно добавлены контрактные спецификации, выходящие за рамки нумерации PDF (например inbound API для GPT).

Каждый файл, привязанный к PDF, соответствует отдельному пункту исходного документа (разделы 1-18) и включает:
- продуктовую цель и ценность;
- операционную и техническую модель реализации;
- NFR/риски/метрики;
- решения и открытые вопросы.

## Файлы

- `01-module-mission.md`
- `02-business-problem-and-target-outcome.md`
- `03-scope-and-boundaries.md`
- `04-business-entities-model.md`
- `05-module-philosophy-and-principles.md`
- `06-lifecycle-business-logic.md`
- `07-dynamic-clusters-product-model.md`
- `08-distinct-issue-product-logic.md`
- `09-spa-issue-projection.md`
- `10-functional-requirements-system-spec.md`
- `11-working-content-model.md`
- `12-delivery-specs-package.md`
- `13-anti-patterns-and-prevention.md`
- `14-quality-criteria-framework.md`
- `15-acceptance-criteria-operationalization.md`
- `16-working-assumptions-v1.md`
- `17-open-decisions-and-decision-log.md`
- `18-module-formula-and-strategy.md`

### Контракты интеграции (GPT / API)

- `19-inbound-api-gpt-preprocessing-and-spa-issue-contracts.md` — inbound JSON для Story Intake, препроцессинг GPT, «живая» история, черновик SPA-issue (i18n), задел gov-interop.
- `22-m2-demo-story-intake-interview-ssot-v1.md` — **SSOT решений** по story intake для **demo M2** после интервью 2026-04-26: обязательные поля, async extraction, deprecated `/issues`, маппинг GPT → intake; раздел «as-is» синхронизирован с фактическим кодом `src/core/intake/contracts.py` и `src/core/application/services.py`.
- `23-m2-demo-story-clustering-interview-ssot-v1.md` — **SSOT решений** по кластеризации stories и выпуску issue из кластера (demo): пороги через `.env`, линзы, geo/tie-breaker/type-resolution, primary GPT canonical type/labels, N:M story–issue, контракт выхода кластера; раздел «as-is» сверен с `src/core/cluster/engine.py`, `src/core/application/issue_create.py`, `src/core/promotion/gates.py`.
- `24-tallinn-issues-read-api.md` — **требования и task-sequence** для read API кластеризованных issues: rename таблицы `spa_issue_projections` → `tallinn_issues_projections` (view не нужен — gateway читает через service_role), Protocol `IssueProjectionReadStore`, три реализации store (InMemory/SQLite/Supabase), endpoints `GET /tallinn/issues` и `GET /tallinn/issues/{issue_id}`, CORS; 10 упорядоченных шагов с критериями приёмки.
- `25-clustering-engine-target-state-spec.md` — **эталонные технические требования** к механике кластеризации: инварианты (детерминизм ID через SHA-256, idempotency, языковая нейтральность), полные словари SignalDimension/ClusterLens, иерархия источников сигналов (GPT canonical → keyword fallback), формула readiness score с исправлением hardcode=100, идемпотентность через lifecycle CLUSTERED, схема таблиц `story_signals`/`cluster_memberships`, расширенный реестр env vars (`CLUSTER_SIGNAL_SOURCE`, `CLUSTER_PRIMARY_LENS`, `CLUSTER_ID_ALGORITHM`), целевой orchestrator с 11-шаговой последовательностью, observability.
- `26-clustering-signal-axes-from-gpt-taxonomy.md` — **бизнес-анализ и проектирование осей кластеризации**: сопоставление GPT taxonomy (REQ-20) с текущей реализацией; модель трёх аудиторий (жители, государство, бизнес); принципы выбора осей (actionability, разделительная сила); 6 новых SmartSignalDimension (`civic_domain`×12 значений, `failure_pattern`×9, `civic_weight`×8, `desired_outcome`×8, `affected_group`×9, `geographic_district`); label vocabulary registries (code-ready frozensets, верифицированы по taxonomy §4); алгоритм `infer_signals_from_canonical()`; новые ClusterLens enum values; дефолтный конфиг публичного узла (`civic_domain_micro,failure_pattern_micro,civic_weight_systemic`); примеры cluster-card для каждой аудитории.

**Порядок исполнения gateway (Python) после SSOT 22/23:** operative очередь — YAML [`gateway-active-packages/pkg-*.yaml`](../tasks/gateway-active-packages/) + указатель [`gateway-active-package.current.yaml`](../tasks/gateway-active-package.current.yaml); процесс и Build — [`.cursor/plans/Gateway_builder.plan.md`](../../../.cursor/plans/Gateway_builder.plan.md); не путать с [`.cursor/plans/GPT_builder.plan.md`](../../../.cursor/plans/GPT_builder.plan.md) (репозиторий GPT UI).

### Обрамляющий контекст

- `30-clustering-concepts-and-lens-model.md` — **самодостаточный вводный документ**: теория кластеризации и концепции линз через пример DOGEstonia; читать перед `25` и `26`; содержит полный pipeline story→signal→cluster→issue, анатомию линзы, legacy vs civic поколения, таблицу config defaults vs target.

### Архитектурные решения 2026-05-05 (стратегия v2)

- `27-doge-issue-domain-rename.md` — **DOGEIssue**: переименование `SpaIssueProjection` → `DOGEIssue`, таблицы `spa_issue_projections` → `doge_issues`; supersedes раздел 2.1 из `24`. Полный инвентарь изменений + migration SQL + AC.
- `28-clustering-cron-scheduler.md` — **Cron-планировщик**: отвязка кластеризации от intake; новый метод `process_all_pending()`, `ClusterCronJob` на stdlib threading, lifespan-хук в ASGI, новые env vars `CLUSTER_CRON_INTERVAL_S` / `CLUSTER_CRON_ENABLED`.
- `29-living-issues-cluster-growth-model.md` — **Living Issues**: один `cluster_id` → один активный `DOGEIssue`; новый `extend_candidate()` на `IssuePromotionService`; extend path в `IssueCreateService`; задействует существующий `find_promoted_by_cluster_id` из всех трёх backends.

### Гражданский запуск: Таллинн MVP (civic launch blockers)

- `31-citizen-data-rights-deletion-and-pii.md` — **Права гражданина**: `DELETE /intake/stories/{id}`, soft delete (`WITHDRAWN` статус), `data_notice` в intake response, эвристическая PII-детекция. Закрывает P0-T3, P0-T4 из MVP-аудита и req22 §D-10 ("позже").
- `32-api-security-and-intake-protection.md` — **API Security**: production-grade token (замена demo-токена), `APP_PROFILE=pilot`, rate limiting на `POST /intake/stories` (slowapi), structured security event logging. Закрывает P0-T5, P0-T6 из MVP-аудита.

### Gap-интервью 2026-05-13 — новые требования (пакет REQ-33…39)

Сформированы по результатам gap-анализа и product-интервью. Источник: `docs/analysis/gap-interview-decisions-2026-05-13.md`.

- `33-multilingual-story-intake-contract-v2.md` — **P0 demo**: breaking change контракта v1→v2; dict-формат `{et,ru,en}` для title/description/summary; новое обязательное поле `session_language`; eID gate (`identity_issuer` required); SHA-256 idempotency fallback. Cascade: `intake/contracts.py`, `domain/contracts.py`, DB migrations.
- `34-civic-clustering-canonical-signal-pipeline.md` — **P1**: удаление legacy lenses и `infer_signals_from_narrative()`; civic-only signal extraction; исправление BUG с `_ = canonical_type`; `issue_type` из dominant story canonical, `labels` = union кластера. Cascade: `cluster/engine.py`, `profile/enrichment.py`, `projection/extraction_policy.py`. **Task pipeline:** [`STORY-M2-04-05`](../tasks/epics/EPIC-M2-04-dynamic-cluster-views/stories/STORY-M2-04-05-civic-canonical-signal-pipeline/STORY-M2-04-05-civic-canonical-signal-pipeline.md), operative queue [`pkg-000013`](../tasks/gateway-active-packages/pkg-000013-20260515-req34-civic-canonical-signal.yaml).
- `35-geo-scope-node-architecture-and-filtering.md` — **P1**: реализация `CLUSTER_GEO_FILTER`; новый `CLUSTER_GEO_SCOPE` env var; `StoryGeoSnapshot` admin-уровни (district/settlement/region/country); rejection на intake для out-of-scope историй. Cascade: `domain/contracts.py`, `cluster/engine.py`, `geo/providers.py`.
- `36-alpha-scoring-and-story-quality-gate.md` — **P1**: алгоритм `alpha_score()` (100 pts: classification 30 + narrative richness 40 + geo accuracy 30); `canonical_type` readiness gate в `promotion/gates.py`; eID как intake gate (не scoring). Новый модуль `cluster/alpha.py`.
- `37-pipeline-observability-and-pii-safety.md` — **P2**: `StoryDebugLogger` с per-story JSON Lines файлами; `LOG_DEBUG_DIR` env var; `redact_pii(text, contains_pii)` функция; покрытие всех 5 этапов pipeline. Cascade: `logging_setup.py`, `api/logging.py`.
- `38-data-integrity-issue-links-tests-validation.md` — **P2/P3**: `issue_story_links` N:M таблица (Supabase migration); e2e тесты `extend_candidate()` flow; Arweave txid regex validation. Cascade: bootstrap SQL, `db_supabase.py`, `projection/validation.py`.
- `39-cross-layer-contract-testing.md` — **P2**: offline contract suite zones A–N (bootstrap↔Python, PostgREST coercion, intake mapping, repository parity, API facade, logging, store parity, factory wiring). EPIC-M2-18; complements REQ-24/40 acceptance tests.
- `41-testing-production-coverage-target-state.md` — **P0–P2**: целевое покрытие 25 продакшн-сценариев (PS-01..PS-25): Layer 6 smoke (`LOCAL_SERVER_URL`), cron timing, concurrent intake, env-only config, CI `integration-live` + матрица в [`13-testing-and-quality-architecture.md`](../solution%20architecture/13-testing-and-quality-architecture.md) §6. Исполнение: EPIC-M2-18 stories M2-18-03..05, [`pkg-000021`](../tasks/gateway-active-packages/pkg-000021-20260518-req41-production-test-coverage.yaml).

### Early Signal / Pre-Cluster (parent product REQ)

- `48-early-signal-pre-cluster-data-readiness.md` — **Draft awaiting PA.2**: inventory существующих stores vs Level 1/2 metrics parent Early Signal Dashboard; privacy / Topic≠Issue; **без** invented public API path; sibling spa `15-early-signal-pre-cluster-public-dashboard.md`. Parent: `docs/requirements backlog/DOGEstonia-Early-Signal-Dashboard-Pre-Cluster-Product-Requirements.md`.
- `49-early-signal-network-pulse-l1-api.md` — **Accepted 2026-08-10**: public `GET /tallinn/network-pulse` path + payload schema (GW-ES-02 T00 / pkg-000059); predecessor REQ-48.
- `50-early-signal-emerging-l2-api.md` — **Accepted 2026-08-10**: public `GET /tallinn/emerging-signals` path + payload + MVP L2 rule closing REQ-48 open Q2 for MVP (GW-ES-03 T00 / pkg-000060).

### Post-demo (вне обязательного MVP, сроки не зафиксированы)

- `20-post-demo-orchestration-and-scheduled-jobs.md` — оркестрация, cron/queue, единый use-case слой.
- `21-post-demo-story-tokenization-and-contributor-notifications.md` — токенизация на уровне историй и уведомления авторам; **дисклеймер post-demo**.
