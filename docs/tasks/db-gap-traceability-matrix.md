# DB Gap Traceability Matrix

SSOT source: `docs/analysis/db-gap-register.md`.

| gap_id | Owner task | Task status | Run-summary evidence | Closure state | Notes |
|---|---|---|---|---|---|
| GAP-DB-001 | `TASK-DB-STORIES-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | SQL-backed stories persistence |
| GAP-DB-002 | `TASK-DB-SCHEMA-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | Migration baseline |
| GAP-DB-003 | `TASK-DB-CONFIG-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | DB config + readiness |
| GAP-DB-004 | `TASK-DB-SPA-PROJECTIONS-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | Persistent SPA read-model |
| GAP-DB-005 | `TASK-DB-STORY-EMBEDDINGS-01`, `TASK-DB-SPA-EMBEDDINGS-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | Separate embeddings layers |
| GAP-DB-006 | `TASK-DB-STORIES-01`, `TASK-DB-SPA-PROJECTIONS-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | Integrity constraints/linkage |
| GAP-DB-007 | `TASK-DB-RLS-01` | Implemented (Waiting Acceptance/Commits) | [run-summary-20260423-1518](./run-reports/run-summary-20260423-1518.md) | Implemented | RLS/policy baseline |
| GAP-DB-008 | `TASK-DB-CONFIG-SUPABASE-02` | Todo | — | Planned (Supabase-native wave) | Strict fail-fast config and deterministic backend selection |
| GAP-DB-009 | `TASK-DB-SUPABASE-REPOS-02` | Todo | — | Planned (Supabase-native wave) | Native supabase repositories replace sqlite-centric SQL path |
| GAP-DB-010 | `TASK-DB-READINESS-SUPABASE-02` | Todo | — | Planned (Supabase-native wave) | Connectivity/schema/policy readiness probes for supabase backend |
| GAP-DB-011 | `TASK-DB-RLS-VALIDATION-02` | Todo | — | Planned (Supabase-native wave) | Automated deny/allow policy validation on live supabase |
| GAP-DB-012 | `TASK-TEST-INTEGRATION-SUPABASE-LIVE-01` | Todo | — | Planned (Supabase-native wave) | End-to-end live DB integration proof for intake->issues->projection |
| GAP-DB-013 | `TASK-TEST-UNIT-API-APP-01`, `TASK-TEST-UNIT-INFRA-CONFIG-01`, `TASK-TEST-UNIT-DOMAIN-FLOWS-01`, `TASK-TEST-COVERAGE-GATE-01` | Todo | — | Planned (Supabase-native wave) | Formal unit/mock coverage buckets and quality gate enforcement |

## Closure rule

`Closed` выставляется только если:

1. owner task в `Done (Committed)` в bullrun индексе;
2. есть run-summary evidence;
3. acceptance файлы отмечают `PM gate` + `CTO gate`.

Для supabase-native wave дополнительно обязательно:

4. пройден live bucket `tests/integration/supabase`;
5. `test-matrix-by-type-layer-mocks.md` синхронизирован с фактическими unit/integration buckets.
