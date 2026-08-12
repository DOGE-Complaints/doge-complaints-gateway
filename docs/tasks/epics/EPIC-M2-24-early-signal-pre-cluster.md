# EPIC-M2-24: Early Signal / Pre-Cluster (gateway)

## Epic Meta
- Status: In Progress (ES-02 Done pkg-000059; **ES-03** Done pkg-000060; TASK-ES-04 Todo)
- Priority: Medium
- Owner: TBD
- Target: Sprint Early Signal
- **Materialized:** 2026-08-10 (P1.3 backlog_story STORY-GW-ES-02); ES-03 P1.3 2026-08-10T12:06:12Z
- **ES-02 gate:** PASS 2026-08-10T10:55:48Z — `GET /tallinn/network-pulse` (REQ-49)
- **ES-03 gate:** PASS 2026-08-10T12:17:38Z — `GET /tallinn/emerging-signals` (REQ-50)

## Business Goal
Публичные **честные** L1 Network Pulse aggregates (Stories collected + dims) и L2 Emerging — без выдачи Topics за Issues, без PII/Voices. L1: **REQ-49** / ES-02 Done. L2: **REQ-50** / ES-03 Done.

## Problem Statement
До ES-02/ES-03: данные Stories/labels внутри gateway были, но публичных Pulse/Emerging aggregates не было. **Сейчас:** L1 `GET /tallinn/network-pulse`; L2 `GET /tallinn/emerging-signals` (`EmergingSignalsService` + DI). Issues L3 остаётся отдельным. `/metrics` unfit. **Открыто:** TASK-ES-04 spa-15 seam / PA.2 docs.

## Scope
### In Scope
- STORY-GW-ES-02: Public Network Pulse L1 — **Done** pkg-000059 (`GET /tallinn/network-pulse`, REQ-49)
- STORY-GW-ES-03: Public Emerging L2 read — **Done** pkg-000060 (`GET /tallinn/emerging-signals`, REQ-50)
- Soft: TASK-GW-ES-04 seam (docs; backlog package)
- Hygiene drafts: ES-05 (error envelope), ES-06 (SQL count, Deferred)

### Out of Scope
- Voices (identity); spa layout; clustering math; EmergingSignal table; changing Issues L3
- SQL/`count` RPC as ES-02 DoD (follow-up ES-06 / open Q5)

## Stakeholders
- Product Owner
- Backend (gateway)
- SPA (spa-15 Network Pulse / Emerging consumer)

## Dependencies
- TASK-GW-ES-01 Done — [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md)
- REQ-48 Draft — [`48-early-signal-pre-cluster-data-readiness.md`](../../requirements/48-early-signal-pre-cluster-data-readiness.md)
- REQ-49 Accepted — [`49-early-signal-network-pulse-l1-api.md`](../../requirements/49-early-signal-network-pulse-l1-api.md)
- REQ-50 Accepted — [`50-early-signal-emerging-l2-api.md`](../../requirements/50-early-signal-emerging-l2-api.md)
- Sibling spa-15 — L1/L2 paths known; board seam TASK-ES-04

## Success Metrics
- GW-ES-02 story gate PASS: Pulse service + public GET + Topic≠Issue + Issues regression — **met** 2026-08-10
- GW-ES-03 story gate PASS: Emerging service + public GET + ≠ Issues + no EmergingSignal DDL — **met** 2026-08-10
- spa-15 Pulse/Emerging wiring unblocked after contract (TASK-ES-04 / spa)

## Epic Acceptance Criteria
- GW-ES-02 story gate PASS (pkg-000059) — **met**
- GW-ES-03 story gate PASS (pkg-000060) — **met** (P3 2026-08-10T12:17:38Z)

## Risks and Mitigation
- **Topic≠Issue leak / Emerging=Issues confuse:** ES-03 T04/T05 contract — addressed
- **Cabinet DI anti-pattern:** factory + `ApiDependencies.emerging_signals_service` only — addressed
- **Path invent:** REQ-50 SSOT — addressed

## Definition of Done
- ES-02 product Done (pkg-000059 T00–T07); audit follow-up T08–T10 docs
- ES-03 product Done (pkg-000060 T00–T07); gate PASS; Bullrun synced

## Stories (decomposed)

| Key | Story | Status |
|---|---|---|
| STORY-GW-ES-02 | [Public Network Pulse L1 aggregates](./EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-02-public-network-pulse-l1-aggregates/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) → [backlog](../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) | 🔵 Done (Awaiting Commits) pkg-000059 gate PASS 2026-08-10T10:55:48Z |
| STORY-GW-ES-03 | [Public Emerging L2 read](./EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/STORY-GW-ES-03-public-emerging-l2-read.md) → [backlog](../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md) | 🔵 Done (Awaiting Commits) pkg-000060 gate PASS 2026-08-10T12:17:38Z |

## Decision Ref
- [`backlog-stories/early-signal-pre-cluster/INDEX.md`](../backlog-stories/early-signal-pre-cluster/INDEX.md)
- [`STORY-GW-ES-02-public-network-pulse-l1-aggregates.md`](../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md)
- [`STORY-GW-ES-03-public-emerging-l2-read.md`](../backlog-stories/early-signal-pre-cluster/STORY-GW-ES-03-public-emerging-l2-read.md)
- [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](../backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md)
- REQ-48; REQ-49; REQ-50; parent Early Signal product REQ; spa-15 sibling
