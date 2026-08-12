# Gateway backlog stories — root index

> **SSOT:** package `INDEX.md` + [`bullrun-launch-index.md`](../bullrun-launch-index.md)  
> **Dashboard (MVP):** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md)  
> **Audit:** [`backlog-status-audit-2026-07-10.md`](../../analysis/backlog-status-audit-2026-07-10.md)  
> **Updated:** 2026-08-10

## Summary

| Packages | Product stories (excl. superseded) | Done | Todo / In Progress | Deferred |
|----------|-----------------------------------|------|--------------------|----------|
| 8 | see MVP dashboard | active **33/35 (~94%)** | **1** In Progress (ES-03) + **1** Todo (TASK-ES-04) | **3** (CAB-03, L10N-04, TAX-04) |

*Канон метрик MVP (incl. doc-tasks): [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — active **33/35**.*

## By package

| Package | Stories | INDEX | Notes |
|---------|---------|-------|-------|
| [story-draft-handoff](story-draft-handoff/INDEX.md) | 7 | 7 Done | EPIC-M2-21; **DRAFT-07** Done pkg-000056 |
| [issues-read-contract](issues-read-contract/INDEX.md) | 8 | 8 Done | package closed |
| [demo-data-seeding](demo-data-seeding/INDEX.md) | 4 | 4 Done | SEED-01..04 closed |
| [localization-l10n](localization-l10n/INDEX.md) | 4 | 3 Done, 1 Deferred | GW-L10N-04 future |
| [gpt-submit-authz](gpt-submit-authz/INDEX.md) | 2 active | 2 Done | GAUTH-01/02 **Superseded** (excluded) |
| [cabinet-api](cabinet-api/INDEX.md) | 3 | 2 Done, 1 Deferred | GW-CAB-03 post-MVP |
| [taxonomy-fidelity](taxonomy-fidelity/INDEX.md) | 4 | 3 Done, 1 Deferred | TAX-01/02/03 Done; **TAX-04** Deferred |
| [early-signal-pre-cluster](early-signal-pre-cluster/INDEX.md) | 4 Story + 2 Task | TASK-ES-01 Done; **ES-02 Done** pkg-000059; **ES-03 In Progress** pkg-000060; TASK-ES-04 Todo; **ES-05** draft (G2); **ES-06** Deferred (G3) | [gap-analysis](early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md); epic [EPIC-M2-24](../epics/EPIC-M2-24-early-signal-pre-cluster.md); REQ-49 |

## Retired

- **GW-DEPLOY-01** — [retire note](../../analysis/retire-STORY-GW-DEPLOY-01-2026-07-10.md); deploy SSOT → [`railpack.json`](../../railpack.json)

## Epic mirror (execution SSOT)

Pipeline stories live under `docs/tasks/epics/`. Backlog files here are product/requirements mirrors; gates and pkgs reference epics paths in package INDEX rows.

| Epic | Backlog package | Status |
|------|-----------------|--------|
| EPIC-M2-21 | story-draft-handoff | Done package (DRAFT-01..07; Awaiting Commits) |
| EPIC-M2-06 | issues-read-contract, localization-l10n | Done package / L10N-04 deferred |
| EPIC-M2-19 | demo-data-seeding | Done (SEED-01..04) |
| EPIC-M2-20 | gpt-submit-authz | Done (superseded path) |
| EPIC-M2-22 | cabinet-api | CAB-01/02 Done; CAB-03 Deferred |
| EPIC-M2-23 | taxonomy-fidelity | TAX-01/02/03 Done; **TAX-04 Deferred** |
| EPIC-M2-24 | early-signal-pre-cluster | ES-02 Done pkg-000059; **ES-03 In Progress** pkg-000060; TASK-ES-04 Todo; ES-05 draft; ES-06 Deferred |

## Traceability (gap docs)

- [`db-gap-traceability-matrix.md`](../db-gap-traceability-matrix.md)
- [`intake-projection-gap-traceability-matrix.md`](../intake-projection-gap-traceability-matrix.md)
- [`db-task-batch-plan.md`](../db-task-batch-plan.md)
- REQ-48 / TASK-ES-01 + ES-02/03 + TASK-ES-04: [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md) §4
