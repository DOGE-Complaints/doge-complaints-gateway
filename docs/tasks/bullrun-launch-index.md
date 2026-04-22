# DOGE Complaints Gateway — Bullrun launch index (Module 2)

**Зона:** `doge-complaints-gateway/docs/tasks/`  
**Команда:** [`.cursor/commands/bullrun-start.md`](../../../.cursor/commands/bullrun-start.md)  
**Коды статусов (S):** ⚪ Todo, 🟡 In Progress, 🔵 Implemented (Waiting Acceptance), 🟢 Done (Committed).

**Pipeline (SSOT):** [`docs/tasks/m2-epic-story-execution-pipeline.md`](./m2-epic-story-execution-pipeline.md)  
**User Manual (Cursor):** [`docs/tasks/m2-pipeline-user-manual-cursor.md`](./m2-pipeline-user-manual-cursor.md)  
**Git / коммиты (методика репозитория, в т.ч. task-доки):** [`docs/methodology/git-commit.md`](../../../docs/methodology/git-commit.md) · [`docs/methodology/git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md)
**Run source rule:** сначала `ACTIVE_TASK_PATH` (если задан), иначе fallback на первую `⚪` сущность по приоритету из этого индекса.

## Актуальная точка (сводка для запуска)

- **Закрыты по индексу:** EPIC-M2-01 … EPIC-M2-10 (все stories в таблицах ниже — `🟢 Done (Committed)`).
- **Приёмка / коммиты:** EPIC-M2-13 — все перечисленные stories в `🔵 Implemented (Waiting Acceptance/Commits)`; строка эпика `M2-13` остаётся **In Progress** до перевода stories в `🟢` после acceptance/commits.
- **Fallback без `ACTIVE_TASK_PATH`:** в `Cross-Epic Task Backlog` нет строк со статусом `⚪`; следующие кандидаты с `⚪` — эпики **M2-11** и **M2-12** (оба Draft).
- **HTTP runtime (факт):** локальный сервер — `python3 -m core.api.asgi_app` (см. [`../runtime-docs/server-env-quickstart.md`](../runtime-docs/server-env-quickstart.md)); legacy `dev_server` удалён — см. [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md).

## EPIC-M2-01 — Core Foundation and Governance

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-01-01 | [Layered module bootstrap](./epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-01-layered-module-bootstrap.md) | implement | Done (Committed) | `src/core` layered skeleton + smoke/guardrails tests + task artifacts. |
| 🟢 | M2-01-02 | [DI providers and service factory baseline](./epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-02-di-providers-and-service-factory-baseline.md) | implement | Done (Committed) | `ServiceFactory` contract + providers + API wiring via DI bridge + tests. |
| 🟢 | M2-01-03 | [Config schema and feature flags baseline](./epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-03-config-schema-and-feature-flags-baseline.md) | implement | Done (Committed) | `core.config` schema + demo/pilot profiles + feature flags + config loading tests. |
| 🟢 | M2-01-04 | [Unified error envelope and trace propagation](./epics/EPIC-M2-01-core-foundation-and-governance/stories/STORY-M2-01-04-unified-error-envelope-and-trace-propagation.md) | implement | Done (Committed) | Unified `ErrorEnvelope`, trace propagation in payload/logs, contract tests. |

## EPIC-M2-02 — Story Intake and Story Store

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-02-01 | [Story intake request/response contract](./epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-01-story-intake-request-response-contract.md) | implement | Done (Committed) | Versioned intake contract and response envelope baseline. |
| 🟢 | M2-02-02 | [Story repository lifecycle and authorship linkage](./epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-02-story-repository-lifecycle-and-authorship-linkage.md) | implement | Done (Committed) | Immutable narrative store + lifecycle and external submitter linkage. |
| 🟢 | M2-02-03 | [Intake idempotency key handling](./epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-03-intake-idempotency-key-handling.md) | implement | Done (Committed) | Deterministic deduplication for repeated intake commands. |
| 🟢 | M2-02-04 | [Intake observability and error taxonomy](./epics/EPIC-M2-02-story-intake-and-store/stories/STORY-M2-02-04-intake-observability-and-error-taxonomy.md) | implement | Done (Committed) | Structured intake telemetry and classified error categories. |

## EPIC-M2-03 — Story Intelligence Profile

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-03-01 | [Signal profile schema and contract baseline](./epics/EPIC-M2-03-story-intelligence-profile/stories/STORY-M2-03-01-signal-profile-schema-and-contract-baseline.md) | implement | Done (Committed) | Profile schema for user-asserted vs system-inferred signal layers. |
| 🟢 | M2-03-02 | [Profile enrichment service baseline](./epics/EPIC-M2-03-story-intelligence-profile/stories/STORY-M2-03-02-profile-enrichment-service-baseline.md) | implement | Done (Committed) | Baseline enrichment service to derive profile signals from story narrative. |
| 🟢 | M2-03-03 | [Profile versioning and audit trail repository](./epics/EPIC-M2-03-story-intelligence-profile/stories/STORY-M2-03-03-profile-versioning-and-audit-trail-repository.md) | implement | Done (Committed) | Version history per story profile and audit-friendly retrieval. |
| 🟢 | M2-03-04 | [Profile quality validation and consistency tests](./epics/EPIC-M2-03-story-intelligence-profile/stories/STORY-M2-03-04-profile-quality-validation-and-consistency-tests.md) | implement | Done (Committed) | Validation rules and test suite for minimum profile consistency. |

## EPIC-M2-04 — Dynamic Cluster Views

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-04-01 | [Cluster lens framework and deterministic clustering](./epics/EPIC-M2-04-dynamic-cluster-views/stories/STORY-M2-04-01-cluster-lens-framework-and-deterministic-clustering.md) | implement | Done (Committed) | Six canonical lenses + deterministic clustering engine baseline. |
| 🟢 | M2-04-02 | [Multi-membership story-to-cluster mapping](./epics/EPIC-M2-04-dynamic-cluster-views/stories/STORY-M2-04-02-multi-membership-story-to-cluster-mapping.md) | implement | Done (Committed) | Story membership across multiple cluster views and lenses. |
| 🟢 | M2-04-03 | [Cluster narrative generator baseline](./epics/EPIC-M2-04-dynamic-cluster-views/stories/STORY-M2-04-03-cluster-narrative-generator-baseline.md) | implement | Done (Committed) | Explainable cluster narrative summaries from dominant patterns. |
| 🟢 | M2-04-04 | [Cluster readiness scoring baseline](./epics/EPIC-M2-04-dynamic-cluster-views/stories/STORY-M2-04-04-cluster-readiness-scoring-baseline.md) | implement | Done (Committed) | Issue-readiness scoring for clusters with explainable factors. |

## EPIC-M2-05 — Distinct Issue Promotion and Reviewability

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-05-01 | [Issue candidate state machine and lifecycle](./epics/EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-01-issue-candidate-state-machine-and-lifecycle.md) | implement | Done (Committed) | `core.promotion` lifecycle orchestration + transition validation + tests. |
| 🟢 | M2-05-02 | [Promotion gate evaluator baseline](./epics/EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-02-promotion-gate-evaluator-baseline.md) | implement | Done (Committed) | Explainable gate evaluation integrated into submit step + tests. |
| 🟢 | M2-05-03 | [Split merge reframe command handlers](./epics/EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-03-split-merge-reframe-command-handlers.md) | implement | Done (Committed) | Draft-only split/merge/reframe with audit trail provenance + tests. |
| 🟢 | M2-05-04 | [Review audit log repository](./epics/EPIC-M2-05-distinct-issue-promotion-review/stories/STORY-M2-05-04-review-audit-log-repository.md) | implement | Done (Committed) | In-memory audit repository + deterministic ordered reads + DI wiring. |

## EPIC-M2-06 — SPA Projection and i18n Contract

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-06-01 | [SPA projection DTO and mapper](./epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-01-spa-projection-dto-and-mapper.md) | implement | Done (Committed) | `core.projection` DTO, input, mapper, `IssueProjectionService`. |
| 🟢 | M2-06-02 | [i18n projection policy](./epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-02-i18n-projection-policy.md) | implement | Done (Committed) | `I18nText`, summary fallback, `PROJECTION_POLICY_VERSION`. |
| 🟢 | M2-06-03 | [SPA projection contract test suite](./epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-03-spa-projection-contract-tests.md) | implement | Done (Committed) | Required keys + DI `get_issue_projection_service`. |
| 🟢 | M2-06-04 | [SPA enum governance checks](./epics/EPIC-M2-06-spa-projection-and-i18n/stories/STORY-M2-06-04-spa-enum-governance.md) | implement | Done (Committed) | Governed status/type/labels; placeholder tx rejection. |

## EPIC-M2-07 — Evidence Pack and Lineage

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-07-01 | [Evidence pack schema](./epics/EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-01-evidence-pack-schema.md) | implement | Done (Committed) | `core.evidence.types`, EvidencePackRecord, snapshot refs. |
| 🟢 | M2-07-02 | [Lineage graph persistence](./epics/EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-02-lineage-graph-persistence.md) | implement | Done (Committed) | In-memory repo, reverse lineage по story_id, reindex на upsert. |
| 🟢 | M2-07-03 | [Visibility tiers and redaction](./epics/EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-03-visibility-tiers-and-redaction.md) | implement | Done (Committed) | `VisibilityTier`, `redact_evidence_pack`, public без artifact refs. |
| 🟢 | M2-07-04 | [Evidence export metadata](./epics/EPIC-M2-07-evidence-pack-and-lineage/stories/STORY-M2-07-04-evidence-export-metadata.md) | implement | Done (Committed) | `EvidenceExportMetadata`, `BUNDLE_FORMAT`, `export_metadata` на сервисе. |

## EPIC-M2-08 — Geo Intelligence

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-08-01 | [Canonical geo cache schema](./epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-01-canonical-geo-cache-schema.md) | implement | Done (Committed) | `normalize_location_query`, `InMemoryGeoCacheRepository`, `StoryGeoSnapshot`. |
| 🟢 | M2-08-02 | [GeoResolver adapter chain](./epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-02-geo-resolver-adapter-chain.md) | implement | Done (Committed) | `GeoResolverChain`, стабы OpenCage/Nominatim, fallback Narva. |
| 🟢 | M2-08-03 | [GeoService in intake](./epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-03-geo-service-intake-integration.md) | implement | Done (Committed) | `narrative.location_query`, `StoryRecord.geo`, DI `get_geo_service`. |
| 🟢 | M2-08-04 | [Geo resilience and metrics](./epics/EPIC-M2-08-geo-intelligence-module/stories/STORY-M2-08-04-geo-resilience-and-metrics-tests.md) | implement | Done (Committed) | `InMemoryGeoMetrics`, degraded intake при unknown place. |

## EPIC-M2-09 — Security, Config, Observability

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-09-01 | [Centralized config and env validation](./epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-01-centralized-config-and-env-validation.md) | implement | Done (Committed) | `ENV_SCHEMA` + `LOG_LEVEL`, валидация `API_BASE_URL` (http/https), тесты. |
| 🟢 | M2-09-02 | [Security middleware baseline](./epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-02-security-middleware-baseline.md) | implement | Done (Committed) | `ServiceTokenAuth`, `SERVICE_API_TOKEN`, `handle_protected_status`, UNAUTHORIZED envelope. |
| 🟢 | M2-09-03 | [Structured logging and tracing](./epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-03-structured-logging-and-tracing.md) | implement | Done (Committed) | `log_api_event`, `trace_id` в extra логов handlers. |
| 🟢 | M2-09-04 | [Health checks and metrics](./epics/EPIC-M2-09-security-config-observability/stories/STORY-M2-09-04-health-checks-and-metrics.md) | implement | Done (Committed) | `handle_readiness`, `handle_metrics`, `ApiMetrics`. |

## EPIC-M2-10 — Demo-to-Pilot Adapters

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🟢 | M2-10-01 | [Adapter interfaces (wallet push / sign / tx)](./epics/EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-01-define-adapter-interfaces-wallet-push-sign-tx.md) | implement | Done (Committed) | `core.adapters` protocols + `TxReceipt`. |
| 🟢 | M2-10-02 | [Demo stub adapters](./epics/EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-02-demo-stub-adapters.md) | implement | Done (Committed) | `Demo*` in-memory, детерминированные id. |
| 🟢 | M2-10-03 | [Feature-flag snapshot and adapter bundle](./epics/EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-03-feature-flag-registry-and-bundle.md) | implement | Done (Committed) | `build_adapter_bundle`, `adapter_runtime_flags`. |
| 🟢 | M2-10-04 | [Pilot activation playbook](./epics/EPIC-M2-10-demo-to-pilot-adapters/stories/STORY-M2-10-04-pilot-activation-playbook.md) | doc | Done (Committed) | [`pilot-activation-playbook.md`](./task-m2-10-04-pilot-activation-playbook/pilot-activation-playbook.md). |
| 🟢 | M2-10 | [EPIC-M2-10 Demo-to-Pilot Adapters](./epics/EPIC-M2-10-demo-to-pilot-adapters.md) | epic | Done (Committed) | Story-level токенизация — EPIC-M2-12. |

## EPIC-M2-13 — Demo Polishing (Gap Closure)

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| 🔵 | M2-13-01 | [Story lifecycle readiness transitions](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-01-story-lifecycle-readiness-transitions.md) | implement | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-001`. |
| 🔵 | M2-13-02 | [Intake envelope parity with requirements 19](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-02-intake-envelope-parity-requirements-19.md) | implement | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-002`. |
| 🔵 | M2-13-03 | [Author lineage proof tests](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-03-author-lineage-proof-tests.md) | test | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-003`. |
| 🔵 | M2-13-04 | [Centralized config injection consistency](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-04-centralized-config-injection-consistency.md) | implement | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-004`. |
| 🔵 | M2-13-05 | [Geo timeout/retry policy hardening](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-05-geo-timeout-retry-policy-hardening.md) | implement | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-005`. |
| 🔵 | M2-13-06 | [Ops alert metrics contract](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-06-ops-alert-metrics-contract.md) | doc+test | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-006`. |
| 🔵 | M2-13-07 | [Privacy minimization runtime enforcement](./epics/EPIC-M2-13-demo-polishing/stories/STORY-M2-13-07-privacy-minimization-runtime-enforcement.md) | implement | Implemented (Waiting Acceptance/Commits) | Закрытие `GAP-007`. |
| 🔵 | M2-13 | [EPIC-M2-13 Demo Polishing](./epics/EPIC-M2-13-demo-polishing.md) | epic | In Progress | Consolidated gap-closure wave по non-post-demo scope. |

## EPIC-M2-11 — Post-demo: Orchestration and Scheduled Automation

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-11 | [EPIC-M2-11 Post-demo orchestration](./epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md) | epic | Draft | `solution architecture/16`, `requirements/20`; не блокирует demo. |

## EPIC-M2-12 — Post-demo: Story Tokenization and Contributor Notifications

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-12 | [EPIC-M2-12 Post-demo tokenization](./epics/EPIC-M2-12-post-demo-story-tokenization-and-contributor-notifications.md) | epic | Draft | `requirements/21` (дисклеймер); срок не зафиксирован. |

## Cross-Epic Task Backlog

| S | Key | Task | Type | Status | Scope / Notes |
|---|-----|------|------|--------|---------------|
| 🟢 | TASK-AUTH-01 | [Full Bearer auth enforcement across API boundary](./task-implement-full-bearer-api-enforcement/README.md) | implement | Done (Committed) | Универсальный server-side auth enforcement + fail-fast policy + test matrix. |
| 🔵 | TASK-DEMO-UI-01 | [Demo static auth mock page (fixed user)](./task-implement-demo-static-auth-mock-page/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Отдельный static `html/css` auth-entry экран для demo narrative и onboarding. |
| 🔵 | TASK-BP-API-01 | [FastAPI ASGI entrypoint for runtime API](./task-implement-fastapi-asgi-entrypoint/README.md) | implement | Implemented (Waiting Acceptance) | ASGI/uvicorn entrypoint; фактическая верификация + удаление legacy `dev_server`: [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-02 | [Auth middleware and protected route policy](./task-implement-auth-middleware-and-route-policy/README.md) | implement | Implemented (Waiting Acceptance) | Route-level auth policy; та же runtime-verification сессия: [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-03 | [HTTP transport smoke and contract checks](./task-tests-http-transport-e2e-smoke/README.md) | test | Implemented (Waiting Acceptance) | `TestClient` smoke; полный pytest `104 passed` — [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-04 | [Demo auth page delivery boundary](./task-refactor-demo-auth-delivery-boundary/README.md) | refactor | Implemented (Waiting Acceptance) | Combined ASGI delivery + docs; Puppeteer mock-auth smoke — [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |

## Run Reports Registry

| Timestamp | Mode | Scope | Report | Outcome |
|---|---|---|---|---|
| 2026-04-22 20:38 | explicit | Runtime verification + remove legacy `dev_server` | [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md) | Live HTTP smoke OK, Puppeteer mock auth OK, `dev_server.py` removed, full pytest `104 passed`, pilot adapter test env aligned with strict token. |
| 2026-04-22 17:30 | explicit | TASK_BATCH (`TASK-BP-API-01`, `TASK-BP-API-02`, `TASK-BP-API-03`, `TASK-BP-API-04`) | [run-summary-20260422-1730](./run-reports/run-summary-20260422-1730.md) | FastAPI/ASGI runtime added, route auth policy enforced, HTTP transport smoke tests added, demo static/API boundary documented. |
| 2026-04-22 14:29 | explicit | TASK_BATCH (`TASK-DEMO-UI-01`) | [run-summary-20260422-1429](./run-reports/run-summary-20260422-1429.md) | Static demo auth page implemented with loading/success states and runbook. |
| 2026-04-22 14:16 | explicit | TASK_BATCH (`TASK-AUTH-01`) | [run-summary-20260422-1416](./run-reports/run-summary-20260422-1416.md) | Auth gate expanded to metrics, pilot fail-fast policy added, tests green (31 passed). |

Правило синхронизации:
- после каждого запуска (`EPIC_BATCH`/`STORY_BATCH`/`TASK_BATCH`) создать `run-summary-YYYYMMDD-HHMM.md` в `docs/tasks/run-reports/`;
- в той же итерации добавить строку в эту таблицу (newest-first).

