# DOGE Complaints Gateway — Bullrun launch index (Module 2)

**Зона:** `doge-complaints-gateway/docs/tasks/`  
**Команда:** [`.cursor/commands/bullrun-start.md`](../../../.cursor/commands/bullrun-start.md)  
**Коды статусов (S):** ⚪ Todo, 🟡 In Progress, 🔵 Implemented (Waiting Acceptance), 🟢 Done (Committed).

**Pipeline (SSOT):** [`docs/tasks/m2-epic-story-execution-pipeline.md`](./m2-epic-story-execution-pipeline.md)  
**User Manual (Cursor):** [`docs/tasks/m2-pipeline-user-manual-cursor.md`](./m2-pipeline-user-manual-cursor.md)

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
| ⚪ | M2-07 | [EPIC-M2-07 Evidence Pack](./epics/EPIC-M2-07-evidence-pack-and-lineage.md) | epic | Draft | Декомпозиция stories — см. файл эпика. |

## EPIC-M2-08 — Geo Intelligence

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-08 | [EPIC-M2-08 Geo Intelligence](./epics/EPIC-M2-08-geo-intelligence-module.md) | epic | Draft | Декомпозиция stories — см. файл эпика. |

## EPIC-M2-09 — Security, Config, Observability

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-09 | [EPIC-M2-09 Security Config Observability](./epics/EPIC-M2-09-security-config-observability.md) | epic | Draft | Декомпозиция stories — см. файл эпика; метрики job runs — см. EPIC-M2-11. |

## EPIC-M2-10 — Demo-to-Pilot Adapters

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-10 | [EPIC-M2-10 Demo-to-Pilot Adapters](./epics/EPIC-M2-10-demo-to-pilot-adapters.md) | epic | Draft | Декомпозиция stories — см. файл эпика; story-level токенизация — см. EPIC-M2-12. |

## EPIC-M2-11 — Post-demo: Orchestration and Scheduled Automation

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-11 | [EPIC-M2-11 Post-demo orchestration](./epics/EPIC-M2-11-post-demo-orchestration-and-scheduled-automation.md) | epic | Draft | `solution architecture/16`, `requirements/20`; не блокирует demo. |

## EPIC-M2-12 — Post-demo: Story Tokenization and Contributor Notifications

| S | Key | Story | Type | Status | Scope / Notes |
|---|-----|-------|------|--------|---------------|
| ⚪ | M2-12 | [EPIC-M2-12 Post-demo tokenization](./epics/EPIC-M2-12-post-demo-story-tokenization-and-contributor-notifications.md) | epic | Draft | `requirements/21` (дисклеймер); срок не зафиксирован. |

