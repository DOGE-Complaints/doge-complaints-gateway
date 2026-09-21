# Gateway backlog stories — root index

> **SSOT:** package `INDEX.md` + [`bullrun-launch-index.md`](../bullrun-launch-index.md)  
> **Dashboard (MVP):** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md)  
> **Dashboard (Semantic Schema Runtime — not MVP):** [`gateway-semantic-schema-runtime-dashboard.md`](../gateway-semantic-schema-runtime-dashboard.md)  
> **Dashboard (REQ7 threads shell — not MVP):** [`gateway-req7-threads-shell-dashboard.md`](../gateway-req7-threads-shell-dashboard.md)  
> **Audit:** [`backlog-status-audit-2026-07-10.md`](../../analysis/backlog-status-audit-2026-07-10.md)  
> **Updated:** 2026-09-21T20:39:55Z

## Summary

| Packages | Product stories (excl. superseded) | Done | Todo / In Progress | Deferred |
|----------|-----------------------------------|------|--------------------|----------|
| 9 | see MVP dashboard + non-MVP scopes | active **33/35 (~94%)** MVP | **1** In Progress (ES-03) + **1** Todo (TASK-ES-04) MVP; **+1** Done / **+2** Todo REQ7 shell (THR-01 Done; THR-02/03) | **3** (CAB-03, L10N-04, TAX-04) |

*Канон метрик MVP (incl. doc-tasks): [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — active **33/35**. Пакеты `semantic-schema-runtime` и `issue-thread-context-and-node-verification` **не** в этом знаменателе.*

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
| [semantic-schema-runtime](semantic-schema-runtime/INDEX.md) | 5 T-wave Done + 2 Draft later | **не MVP**; git `semantic-schema-runtime`; [scope dashboard](../gateway-semantic-schema-runtime-dashboard.md) | REQ-51; parent REQ3 |
| [issue-thread-context-and-node-verification](issue-thread-context-and-node-verification/INDEX.md) | 1 Done + 2 Todo (THR-01 Done; THR-02/03) | **не MVP**; [scope dashboard](../gateway-req7-threads-shell-dashboard.md) | REQ52; parent REQ7 shell |

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
| [EPIC-semantic-schema-runtime](../epics/EPIC-semantic-schema-runtime.md) | semantic-schema-runtime | REQ-51 T-wave; not `EPIC-M2-*`; исполнение на ветке `semantic-schema-runtime` |
| [EPIC-issue-thread-context-and-node-verification](../epics/EPIC-issue-thread-context-and-node-verification.md) | issue-thread-context-and-node-verification | THR-01 Done pkg-000093; THR-02/03 Todo; not `EPIC-M2-*` |

## Traceability (gap docs)

- [`db-gap-traceability-matrix.md`](../db-gap-traceability-matrix.md)
- [`intake-projection-gap-traceability-matrix.md`](../intake-projection-gap-traceability-matrix.md)
- [`db-task-batch-plan.md`](../db-task-batch-plan.md)
- REQ-48 / TASK-ES-01 + ES-02/03 + TASK-ES-04: [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md) §4
- REQ-51 Semantic Schema Runtime: [`semantic-schema-runtime/INDEX.md`](semantic-schema-runtime/INDEX.md) · [`51-semantic-schema-runtime.md`](../../requirements/51-semantic-schema-runtime.md)
- REQ-52 Issue thread context + node verification (REQ7 shell): [`issue-thread-context-and-node-verification/INDEX.md`](issue-thread-context-and-node-verification/INDEX.md) · [`52-issue-thread-context-and-node-verification.md`](../../requirements/52-issue-thread-context-and-node-verification.md) · [`gateway-req7-threads-shell-dashboard.md`](../gateway-req7-threads-shell-dashboard.md)
