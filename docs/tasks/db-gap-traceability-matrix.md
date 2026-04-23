# DB Gap Traceability Matrix

SSOT source: `docs/analysis/db-gap-register.md`.

| gap_id | Owner task | Task status | Run-summary evidence | Closure state | Notes |
|---|---|---|---|---|---|
| GAP-DB-001 | `TASK-DB-STORIES-01` | Todo | — | Planned | SQL-backed stories persistence |
| GAP-DB-002 | `TASK-DB-SCHEMA-01` | Todo | — | Planned | Migration baseline |
| GAP-DB-003 | `TASK-DB-CONFIG-01` | Todo | — | Planned | DB config + readiness |
| GAP-DB-004 | `TASK-DB-SPA-PROJECTIONS-01` | Todo | — | Planned | Persistent SPA read-model |
| GAP-DB-005 | `TASK-DB-STORY-EMBEDDINGS-01`, `TASK-DB-SPA-EMBEDDINGS-01` | Todo | — | Planned | Separate embeddings layers |
| GAP-DB-006 | `TASK-DB-STORIES-01`, `TASK-DB-SPA-PROJECTIONS-01` | Todo | — | Planned | Integrity constraints/linkage |
| GAP-DB-007 | `TASK-DB-RLS-01` | Todo | — | Planned | RLS/policy baseline |

## Closure rule

`Closed` выставляется только если:

1. owner task в `Done (Committed)` в bullrun индексе;
2. есть run-summary evidence;
3. acceptance файлы отмечают `PM gate` + `CTO gate`.
