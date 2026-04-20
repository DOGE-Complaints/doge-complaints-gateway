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
