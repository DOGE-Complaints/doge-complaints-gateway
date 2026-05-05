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

### Архитектурные решения 2026-05-05 (стратегия v2)

- `27-doge-issue-domain-rename.md` — **DOGEIssue**: переименование `SpaIssueProjection` → `DOGEIssue`, таблицы `spa_issue_projections` → `doge_issues`; supersedes раздел 2.1 из `24`. Полный инвентарь изменений + migration SQL + AC.
- `28-clustering-cron-scheduler.md` — **Cron-планировщик**: отвязка кластеризации от intake; новый метод `process_all_pending()`, `ClusterCronJob` на stdlib threading, lifespan-хук в ASGI, новые env vars `CLUSTER_CRON_INTERVAL_S` / `CLUSTER_CRON_ENABLED`.
- `29-living-issues-cluster-growth-model.md` — **Living Issues**: один `cluster_id` → один активный `DOGEIssue`; новый `extend_candidate()` на `IssuePromotionService`; extend path в `IssueCreateService`; задействует существующий `find_promoted_by_cluster_id` из всех трёх backends.

### Post-demo (вне обязательного MVP, сроки не зафиксированы)

- `20-post-demo-orchestration-and-scheduled-jobs.md` — оркестрация, cron/queue, единый use-case слой.
- `21-post-demo-story-tokenization-and-contributor-notifications.md` — токенизация на уровне историй и уведомления авторам; **дисклеймер post-demo**.
