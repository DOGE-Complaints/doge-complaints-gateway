# DOGE Complaints Gateway — Bullrun launch index (Module 2)

**Зона:** `doge-complaints-gateway/docs/tasks/`  
**Команда:** [`.cursor/commands/bullrun-start.md`](../../../.cursor/commands/bullrun-start.md)  
**Коды статусов (S):** ⚪ Todo, 🟡 In Progress, 🔵 Implemented (Waiting Acceptance), 🟢 Done (Committed).

**Pipeline (SSOT):** [`docs/tasks/m2-epic-story-execution-pipeline.md`](./m2-epic-story-execution-pipeline.md)  
**User Manual (Cursor):** [`docs/tasks/m2-pipeline-user-manual-cursor.md`](./m2-pipeline-user-manual-cursor.md)  
**Gap rollout plan (Intake/Projection):** [`docs/tasks/intake-projection-task-batch-plan.md`](./intake-projection-task-batch-plan.md)  
**Gap traceability matrix (Intake/Projection):** [`docs/tasks/intake-projection-gap-traceability-matrix.md`](./intake-projection-gap-traceability-matrix.md)  
**Gap rollout plan (DB/Supabase):** [`docs/tasks/db-task-batch-plan.md`](./db-task-batch-plan.md)  
**Gap traceability matrix (DB/Supabase):** [`docs/tasks/db-gap-traceability-matrix.md`](./db-gap-traceability-matrix.md)  
**Git / коммиты (методика репозитория, в т.ч. task-доки):** [`docs/methodology/git-commit.md`](../../../docs/methodology/git-commit.md) · [`docs/methodology/git-commit-prompt.md`](../../../docs/methodology/git-commit-prompt.md)
**Run source rule:** сначала `ACTIVE_TASK_PATH` (если задан), иначе fallback на первую `⚪` сущность по приоритету из этого индекса.

## Актуальная точка (сводка для запуска)

- **Закрыты по индексу:** EPIC-M2-01 … EPIC-M2-10 (все stories в таблицах ниже — `🟢 Done (Committed)`).
- **Приёмка / коммиты:** EPIC-M2-13 — все перечисленные stories в `🔵 Implemented (Waiting Acceptance/Commits)`; строка эпика `M2-13` остаётся **In Progress** до перевода stories в `🟢` после acceptance/commits.
- **Fallback без `ACTIVE_TASK_PATH`:** приоритетно первая `⚪` в `Cross-Epic Task Backlog` сверху вниз; текущий story-first старт — `TASK-SF-P0-01` (см. новый SF pack и operative `TASK_BATCH` в `Gateway_builder.plan.md`).
- **Продуктовый SSOT story-first (после интервью):** [`docs/requirements/22-m2-demo-story-intake-interview-ssot-v1.md`](../requirements/22-m2-demo-story-intake-interview-ssot-v1.md), [`docs/requirements/23-m2-demo-story-clustering-interview-ssot-v1.md`](../requirements/23-m2-demo-story-clustering-interview-ssot-v1.md).
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
| 🔵 | TASK-SH-P0-01 | [SH pack: Supabase HTTP client bootstrap and transport abstraction](./task-sh-p0-01-http-client-bootstrap/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: SH-ARCH-HTTP-01; единый PostgREST transport/client boundary для всех supabase repositories. |
| 🔵 | TASK-SH-P0-02 | [SH pack: Config cutover to Supabase HTTP without DSN](./task-sh-p0-02-config-cutover-no-dsn/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: SH-CONFIG-HTTP-01; Supersedes: `TASK-DB-CONFIG-SUPABASE-02`; `DB_BACKEND=supabase` требует `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE`, без обязательного `DATABASE_URL`. |
| 🔵 | TASK-SH-P0-03 | [SH pack: Stories and idempotency repositories via HTTP](./task-sh-p0-03-story-idempotency-http-repos/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: SH-REPO-HTTP-01; Supersedes: `TASK-DB-SUPABASE-REPOS-02` (часть stories/idempotency). |
| 🔵 | TASK-SH-P1-01 | [SH pack: Projection and embeddings repositories via HTTP](./task-sh-p1-01-projection-embeddings-http-repos/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: SH-REPO-HTTP-02; Supersedes: `TASK-DB-SUPABASE-REPOS-02` (часть projections/embeddings). |
| 🔵 | TASK-SH-P1-02 | [SH pack: Promotion and linkage repositories via HTTP](./task-sh-p1-02-promotion-linkage-http-repos/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: SH-REPO-HTTP-03; Supersedes: `TASK-DB-SUPABASE-REPOS-02` (часть issue candidates/review/log/linkage). |
| 🔵 | TASK-SH-P1-03 | [SH pack: Readiness and preflight via HTTP probes](./task-sh-p1-03-readiness-http-preflight/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: SH-READINESS-HTTP-01; Supersedes: `TASK-DB-READINESS-SUPABASE-02`; `db.not_ready` diagnostics via HTTP checks. |
| 🔵 | TASK-SH-P2-01 | [SH pack: Unit/mock coverage for HTTP adapters](./task-sh-p2-01-unit-http-adapter-tests/README.md) | test | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: SH-TEST-HTTP-UNIT-01; transport/auth/timeout/retry/error mapping coverage. |
| 🔵 | TASK-SH-P2-02 | [SH pack: Live Supabase HTTP integration gates](./task-sh-p2-02-live-http-integration/README.md) | test | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: SH-TEST-HTTP-INT-01; live roundtrip + skip-safe integration bucket for HTTP mode. |
| 🔵 | TASK-SH-P2-03 | [SH pack: Runtime docs, runbook and DSN supersede map](./task-sh-p2-03-docs-runbook-supersede/README.md) | docs | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: SH-DOCS-HTTP-01; Supersedes: `TASK-DB-CONFIG-SUPABASE-02`, `TASK-DB-SUPABASE-REPOS-02`, `TASK-DB-READINESS-SUPABASE-02`. |
| 🔵 | TASK-SF-P0-01 | [SF pack: Supabase schema parity for story-first fields and embeddings](./task-sf-p0-01-supabase-schema-parity/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: Q6.1 stories/story_embeddings/issue_embeddings, Q6.2; added migration `20260427_1600_story_first_schema_parity.sql`, required column probe in supabase live smoke. |
| 🔵 | TASK-SF-P0-02 | [SF pack: Cluster config/env wiring and PromotionGate de-hardcode](./task-sf-p0-02-cluster-config-and-gates/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: Q3.1, Q3.3, Q4.2; `CLUSTER_*` added to AppConfig/ENV_SCHEMA, `PromotionGatePolicy` wired from config thresholds, clustering lenses configurable. |
| 🔵 | TASK-SF-P0-03 | [SF pack: Story->cluster->issue orchestrator as single production path](./task-sf-p0-03-story-cluster-issue-orchestrator/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: Q3.4, Q4.1, Q4.2, Q4.3; new `StoryClusterOrchestrator` added and wired into intake handler for automatic cluster->issue attempt. |
| 🔵 | TASK-SF-P0-04 | [SF pack: Supabase SPA compatibility out-of-the-box](./task-sf-p0-04-supabase-spa-compatibility/README.md) | implement | Implemented (Waiting Acceptance/Commits) | **P0**; Closes: Q5.3, Q5.4, Q6.6; added `issues_dashboard` Supabase view migration + live roundtrip integration test (skip-safe without env). |
| 🔵 | TASK-SF-P1-01 | [SF pack: Intake/test fixtures alignment with required narrative fields](./task-sf-p1-01-intake-fixtures-alignment/README.md) | fix | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: Q1.3(part), Q2.1.3, Q2.1.4, Section 8.2; intake test payloads aligned to required `narrative.language` and `narrative.title_hint`. |
| 🔵 | TASK-SF-P1-02 | [SF pack: E2E regression rewrite to story-first pipeline](./task-sf-p1-02-e2e-story-first-regression/README.md) | test | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: Q1.3, Q4.4, Q5.4, Section 8.2; legacy `/issues` e2e paths replaced by story-first checks and dedicated pipeline e2e. |
| 🔵 | TASK-SF-P1-03 | [SF pack: Live Supabase integration gates (required columns + roundtrip)](./task-sf-p1-03-live-supabase-gates/README.md) | test | Implemented (Waiting Acceptance/Commits) | **P1**; Closes: Q6.6, Q5.4; required column probe + SPA roundtrip integration tests are present and skip-safe for missing live env. |
| 🔵 | TASK-SF-P2-01 | [SF pack: Remove deprecated manual issue-create runtime chain](./task-sf-p2-01-remove-manual-issue-chain/README.md) | refactor | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: Q1.5, Q7.2, Section 8.1; removed `/issues` route and `handle_issue_create` API boundary wiring, dropped `issue_create_service` from API dependencies. |
| 🔵 | TASK-SF-P2-02 | [SF pack: Runtime docs cleanup to story-first-only terminology](./task-sf-p2-02-runtime-docs-cleanup/README.md) | docs | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: Q7.1, Q7.3, Section 8.3; story-first docs synced, `/issues` described only as removed boundary (404) not active endpoint. |
| 🔵 | TASK-SF-P2-03 | [SF pack: OpenAPI + contract docs reconciliation for intake narrative](./task-sf-p2-03-openapi-contract-reconciliation/README.md) | docs | Implemented (Waiting Acceptance/Commits) | **P2**; Closes: Q2.1.9, Q2.3.11, A4; `/issues` removed from OpenAPI, intake narrative required/canonical fields synchronized with runtime parser. |
| 🔵 | TASK-INTAKE-HTTP-01 | [Expose story intake contract via HTTP runtime endpoint](./task-intake-http-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-IP-001; `POST /intake/stories` runtime binding implemented, parser/service/envelope wiring, HTTP 200/400 tests green. |
| 🔵 | TASK-ISSUE-CREATE-HTTP-01 | [Expose create issue orchestration via HTTP API](./task-issue-create-http-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-IP-002; `POST /issues` added, orchestration delegated to `IssueCreateService`, HTTP positive/negative tests green. |
| 🔵 | TASK-STORY-TO-PROJECTION-01 | [Bridge story and promotion data into ProjectionInput](./task-story-to-projection-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-IP-003; `StoryPromotionProjectionBridge` added and wired in application layer, bridge tests cover mapping + edge cases. |
| 🔵 | TASK-SPA-PROJECTION-DATA-01 | [Define and enforce SPA projection derivation policy](./task-spa-projection-data-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-IP-004; deterministic derivation rules + `policy_version` marker implemented and validated via tests. |
| 🔵 | TASK-E2E-CONTRACT-01 | [Add end-to-end contract suite for intake-to-spa pipeline](./task-e2e-contract-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | GAP-IP-005; e2e contract suite `intake -> create -> SPA` added with happy-path + negative cases, linked into verification commands. |
| 🔵 | TASK-DB-SCHEMA-01 | [Supabase schema bootstrap and migrations baseline](./task-db-schema-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-002; DB-wave #1; supabase migrations baseline + vector tables created. |
| 🔵 | TASK-DB-CONFIG-01 | [Runtime DB/Supabase config contract and readiness checks](./task-db-config-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-003; DB-wave #2; AppConfig DB contract and readiness db backend signal added. |
| 🔵 | TASK-DB-STORIES-01 | [Persistent storage for incoming stories](./task-db-stories-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-001 + GAP-DB-006(part); DB-wave #3; sqlite-backed stories/idempotency repositories wired. |
| 🔵 | TASK-DB-STORY-EMBEDDINGS-01 | [Persistence for incoming story embeddings](./task-db-story-embeddings-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-005(part); DB-wave #4; deterministic story embedding store persists to SQL layer. |
| 🔵 | TASK-DB-SPA-PROJECTIONS-01 | [Persistence for SPA projections](./task-db-spa-projections-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-004 + GAP-DB-006(part); DB-wave #5; issue projection read-model persistence added. |
| 🔵 | TASK-DB-SPA-EMBEDDINGS-01 | [Persistence for SPA projection embeddings](./task-db-spa-embeddings-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-005(part); DB-wave #6; projection embedding persistence added. |
| 🔵 | TASK-DB-RLS-01 | [RLS and policy baseline for exposed DB access patterns](./task-db-rls-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | GAP-DB-007; DB-wave #7; baseline RLS policies added in supabase migration. |
| 🔵 | TASK-DB-E2E-01 | [E2E DB contract checks for intake/create/projection pipeline](./task-db-e2e-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | DB-wave #8; final gate; DB-backed e2e pipeline suite added and passing. |
| 🔵 | TASK-DB-CONFIG-SUPABASE-02 | [Strict DB/Supabase config contract and fail-fast modes](./task-db-config-supabase-02/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 1 (первый в паре); deterministic backend selection; verified by `tests/test_config_loading.py` + `tests/test_db_backend_switching.py`. |
| 🔵 | TASK-DB-SUPABASE-REPOS-02 | [Supabase-native repositories and stores](./task-db-supabase-repos-02/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 1 (второй в паре); runtime repositories при `DB_BACKEND=supabase`; verified by DI/backend/e2e DB-backed suite. |
| 🔵 | TASK-DB-READINESS-SUPABASE-02 | [Supabase readiness preflight and diagnostics](./task-db-readiness-supabase-02/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 2; readiness probes for connectivity/schema/policy baseline; verified by API ops tests. |
| 🔵 | TASK-DB-RLS-VALIDATION-02 | [Automated RLS validation scenarios for live Supabase](./task-db-rls-validation-02/README.md) | test | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 2; deny-by-default + service role allow policy validation suite; live bucket remains skip-safe without env. |
| 🔵 | TASK-TEST-UNIT-API-APP-01 | [Unit/mock coverage for API and application orchestration](./task-test-unit-api-app-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 3; API/app branches verified in unit bucket (`tests/test_api_security_and_ops.py`, `tests/test_trace_propagation.py`). |
| 🔵 | TASK-TEST-UNIT-INFRA-CONFIG-01 | [Unit coverage for infrastructure adapters and config switching](./task-test-unit-infra-config-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 3; providers/factory/config parsing and backend-switch deterministic tests passed. |
| 🔵 | TASK-TEST-UNIT-DOMAIN-FLOWS-01 | [Unit coverage for intake/promotion/projection domain flows](./task-test-unit-domain-flows-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 3; domain invariants and edge cases verified (`tests/test_unit_domain_flows_supabase_wave.py`). |
| 🔵 | TASK-TEST-INTEGRATION-SUPABASE-LIVE-01 | [Live Supabase integration test bucket](./task-test-integration-supabase-live-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 4; integration bucket in place; skip-safe without env, green with live credentials. |
| 🔵 | TASK-TEST-COVERAGE-GATE-01 | [Formal test coverage gates and verification buckets](./task-test-coverage-gate-01/README.md) | docs+qa | Implemented (Waiting Acceptance/Commits) | Supabase-native wave Batch 5; mandatory buckets + verification commands and gate docs synchronized. |
| 🟢 | TASK-DOMAIN-STORY-CONTRACT-INTERVIEW-01 | [Interview: target story intake contract SSOT](./task-domain-story-contract-interview-01/README.md) | analyze | Done (Committed) | Артефакт: `interview-report-domain-story-contract-01.md`; продуктовый SSOT: `docs/requirements/22-m2-demo-story-intake-interview-ssot-v1.md`. |
| 🟢 | TASK-CLUSTER-CRITERIA-INTERVIEW-01 | [Interview: clustering criteria for demo](./task-cluster-criteria-interview-01/README.md) | analyze | Done (Committed) | Артефакт: `interview-report-cluster-criteria-01.md`; продуктовый SSOT: `docs/requirements/23-m2-demo-story-clustering-interview-ssot-v1.md`. |
| 🔵 | TASK-INTAKE-STORY-CONTRACT-EXPANSION-02 | [Expand story intake contract for deterministic extraction](./task-intake-story-contract-expansion-02/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Story-first P0 по SSOT 22: mandatory `language`/`title_hint` (400), allowlist `et|ru|en`, `canonical_type` / `canonical_labels[]` в intake/domain, тесты `test_story_intake_contract` + `test_http_intake_endpoint` green. |
| 🔵 | TASK-DB-STORY-FIELD-COVERAGE-01 | [Persist rule-relevant story fields end-to-end](./task-db-story-field-coverage-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Story-first: поля language/title_hint/canonical* persisted в sqlite/supabase adapters; roundtrip covered by DB-backed regressions. |
| 🔵 | TASK-API-STORY-FIRST-BOUNDARY-01 | [Shift API boundary to story-first orchestration](./task-api-story-first-boundary-01/README.md) | refactor | Implemented (Waiting Acceptance/Commits) | Story-first: `POST /issues` переведен в deprecated boundary (HTTP 410), primary path `POST /intake/stories`; OpenAPI synced. |
| 🔵 | TASK-PROJECTION-MODULE-BOUNDARY-01 | [Modular projection policy boundary in monolith](./task-projection-module-boundary-01/README.md) | refactor | Implemented (Waiting Acceptance/Commits) | Story-first: policy boundary вынесен в `core/projection/extraction_policy.py`, bridge переведен на pluggable `StoryToProjectionPolicy`, DI wiring + contract tests обновлены. |
| 🔵 | TASK-CLUSTER-STORY-FIRST-PIPELINE-01 | [Build story-first clustering runtime pipeline](./task-cluster-story-first-pipeline-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Story-first runtime stage active: intake triggers `StoryClusterOrchestrator.process_story()`, clustering/promotion thresholds wired via `CLUSTER_*` config and validated by clustering + e2e pipeline tests. |
| 🔵 | TASK-DB-SOURCE-PROCESS-LINKAGE-01 | [Persist SQL source/process linkage entities](./task-db-source-process-linkage-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Story-first: SQL stores added for `issue_candidates` and `review_audit_log`; explicit N:M `issue_story_links` persisted via `IssueCreateService` linkage store and covered by sqlite process-linkage tests. |
| 🔵 | TASK-EMBEDDING-CANONICALIZATION-01 | [Canonicalize story/issue embeddings with policy versioning](./task-embedding-canonicalization-01/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Canonical source blocks introduced for story/issue embeddings; `embedding_policy_version` persisted across in-memory/sqlite/supabase stores and migration contracts updated. |
| 🔵 | TASK-TEST-E2E-STORY-TO-ISSUE-CLUSTER-01 | [E2E for full story->cluster->issue demo path](./task-test-e2e-story-to-issue-cluster-01/README.md) | test | Implemented (Waiting Acceptance/Commits) | Story-first e2e bucket validates cluster->issue materialization, negative boundary on removed `/issues`, and linkage/embedding-policy markers in runtime stores. |
| 🔵 | TASK-CODEBASE-REFACTOR-CLEANUP-01 | [Cleanup legacy/duplicate/ad-hoc drift after waves](./task-codebase-refactor-cleanup-01/README.md) | refactor | Implemented (Waiting Acceptance/Commits) | Anti-drift cleanup applied across projection/embedding/linkage paths, stale task references reconciled to story-first boundary, full regression suite green (`137 passed, 3 skipped`). |
| 🟢 | TASK-AUTH-01 | [Full Bearer auth enforcement across API boundary](./task-implement-full-bearer-api-enforcement/README.md) | implement | Done (Committed) | Универсальный server-side auth enforcement + fail-fast policy + test matrix. |
| 🔵 | TASK-DEMO-UI-01 | [Demo static auth mock page (fixed user)](./task-implement-demo-static-auth-mock-page/README.md) | implement | Implemented (Waiting Acceptance/Commits) | Отдельный static `html/css` auth-entry экран для demo narrative и onboarding. |
| 🔵 | TASK-BP-API-01 | [FastAPI ASGI entrypoint for runtime API](./task-implement-fastapi-asgi-entrypoint/README.md) | implement | Implemented (Waiting Acceptance) | ASGI/uvicorn entrypoint; фактическая верификация + удаление legacy `dev_server`: [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-02 | [Auth middleware and protected route policy](./task-implement-auth-middleware-and-route-policy/README.md) | implement | Implemented (Waiting Acceptance) | Route-level auth policy; та же runtime-verification сессия: [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-03 | [HTTP transport smoke and contract checks](./task-tests-http-transport-e2e-smoke/README.md) | test | Implemented (Waiting Acceptance) | `TestClient` smoke; полный pytest `104 passed` — [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |
| 🔵 | TASK-BP-API-04 | [Demo auth page delivery boundary](./task-refactor-demo-auth-delivery-boundary/README.md) | refactor | Implemented (Waiting Acceptance) | Combined ASGI delivery + docs; Puppeteer mock-auth smoke — [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md). |

## Run Reports Registry

| Timestamp | Mode | Scope | Report | Outcome |
|---|---|---|---|---|
| 2026-04-27 16:37 | fallback | Post-SF backlog continuation (`TASK-PROJECTION-MODULE-BOUNDARY-01` … `TASK-CODEBASE-REFACTOR-CLEANUP-01`) | [run-summary-20260427-1637](./run-reports/run-summary-20260427-1637.md) | Remaining story-first backlog items implemented: modular projection policy boundary, clustering pipeline closure, SQL process/linkage persistence, canonical embedding policy versioning, expanded e2e cluster flow, and cleanup anti-drift pass. |
| 2026-04-27 16:35 | explicit | SF pack completion (P2 closure) | [run-summary-20260427-1635](./run-reports/run-summary-20260427-1635.md) | `TASK-SF-P2-01`, `TASK-SF-P2-02`, `TASK-SF-P2-03` finalized as implemented (waiting acceptance/commits); story-first boundary cleanup + runtime docs/OpenAPI reconciliation completed. |
| 2026-04-27 16:30 | explicit | SF pack continuation (P1 completion) | [run-summary-20260427-1630](./run-reports/run-summary-20260427-1630.md) | `TASK-SF-P1-01`, `TASK-SF-P1-02`, `TASK-SF-P1-03` implemented (waiting acceptance): fixture alignment, story-first e2e rewrite, and live Supabase gate coverage completed. |
| 2026-04-27 16:18 | explicit | SF pack P0 execution (`TASK-SF-P0-03`, `TASK-SF-P0-04`) | [run-summary-20260427-1618](./run-reports/run-summary-20260427-1618.md) | `TASK-SF-P0-03` and `TASK-SF-P0-04` implemented (waiting acceptance): orchestrator wired after intake, plus Supabase `issues_dashboard` view and roundtrip integration test. |
| 2026-04-27 16:05 | explicit | SF pack execution progress (`TASK-SF-P0-01` -> `TASK-SF-P0-03`) | [run-summary-20260427-1605](./run-reports/run-summary-20260427-1605.md) | `TASK-SF-P0-01` and `TASK-SF-P0-02` implemented (waiting acceptance), `TASK-SF-P0-03` moved to In Progress; schema parity + env-driven cluster/gate wiring validated by tests (`16 passed, 1 skipped`). |
| 2026-04-27 15:51 | explicit | Gateway Story Builder SF-pack sync run | [run-summary-20260427-1551](./run-reports/run-summary-20260427-1551.md) | SF gap-closure package scaffolded (`TASK-SF-P0-01`…`TASK-SF-P2-03`), backlog/index updated, operative `ACTIVE_TASK_PATH` synchronized P0→P1→P2. |
| 2026-04-23 15:18 | fallback | TASK_BATCH (`TASK-DB-SCHEMA-01` … `TASK-DB-E2E-01`) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | DB/Supabase wave implemented: schema+config+SQL stores+RLS+DB-backed e2e contracts. |
| 2026-04-23 15:05 | fallback | TASK_BATCH (`TASK-ISSUE-CREATE-HTTP-01`, `TASK-STORY-TO-PROJECTION-01`, `TASK-SPA-PROJECTION-DATA-01`, `TASK-E2E-CONTRACT-01`) | [run-summary-20260423-1505](./run-reports/run-summary-20260423-1505.md) | Create-issue orchestration and bridge/policy/e2e wave implemented; intake->create->SPA contract suite green (`21 passed`). |
| 2026-04-23 14:53 | fallback | TASK_BATCH (`TASK-INTAKE-HTTP-01`) | [run-summary-20260423-1453](./run-reports/run-summary-20260423-1453.md) | `POST /intake/stories` implemented in runtime API, parser/service/envelope wiring complete, HTTP tests green (`200/400`) and OpenAPI runtime-state synced. |
| 2026-04-23 14:44 | explicit | Gateway Story Builder process-governance run | [run-summary-20260423-1444](./run-reports/run-summary-20260423-1444.md) | Gateway Story Builder rules re-validated: input source resolution, missing-epic decomposition rule, index sync discipline, registry updated. |
| 2026-04-22 20:38 | explicit | Runtime verification + remove legacy `dev_server` | [run-summary-20260422-2038](./run-reports/run-summary-20260422-2038.md) | Live HTTP smoke OK, Puppeteer mock auth OK, `dev_server.py` removed, full pytest `104 passed`, pilot adapter test env aligned with strict token. |
| 2026-04-22 17:30 | explicit | TASK_BATCH (`TASK-BP-API-01`, `TASK-BP-API-02`, `TASK-BP-API-03`, `TASK-BP-API-04`) | [run-summary-20260422-1730](./run-reports/run-summary-20260422-1730.md) | FastAPI/ASGI runtime added, route auth policy enforced, HTTP transport smoke tests added, demo static/API boundary documented. |
| 2026-04-22 14:29 | explicit | TASK_BATCH (`TASK-DEMO-UI-01`) | [run-summary-20260422-1429](./run-reports/run-summary-20260422-1429.md) | Static demo auth page implemented with loading/success states and runbook. |
| 2026-04-22 14:16 | explicit | TASK_BATCH (`TASK-AUTH-01`) | [run-summary-20260422-1416](./run-reports/run-summary-20260422-1416.md) | Auth gate expanded to metrics, pilot fail-fast policy added, tests green (31 passed). |

Правило синхронизации:
- после каждого запуска (`EPIC_BATCH`/`STORY_BATCH`/`TASK_BATCH`) создать `run-summary-YYYYMMDD-HHMM.md` в `docs/tasks/run-reports/`;
- в той же итерации добавить строку в эту таблицу (newest-first).

