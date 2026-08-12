# Early Signal / Pre-Cluster — data readiness (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/early-signal-pre-cluster/`  
**Тип:** backlog (inventory Task Done; Pulse L1 Done; Emerging L2 Done pkg-000060; seam Task Todo; hygiene drafts ES-05–ES-08).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`48-early-signal-pre-cluster-data-readiness.md`](../../../requirements/48-early-signal-pre-cluster-data-readiness.md)  
**Pulse API REQ:** [`49-early-signal-network-pulse-l1-api.md`](../../../requirements/49-early-signal-network-pulse-l1-api.md)  
**Emerging API REQ:** [`50-early-signal-emerging-l2-api.md`](../../../requirements/50-early-signal-emerging-l2-api.md)  
**Sibling:** [`spa-app/…/15-early-signal-pre-cluster-public-dashboard.md`](../../../../spa-app/docs/requirements/15-early-signal-pre-cluster-public-dashboard.md)  
**SSOT inventory:** [`gap-analysis-early-signal-data-readiness-2026-08-09.md`](./gap-analysis-early-signal-data-readiness-2026-08-09.md) — L1 Pulse Public=**Y** (`GET /tallinn/network-pulse`); L2 Emerging Public=**Y** (`GET /tallinn/emerging-signals` REQ-50); G-ES-PUB-01/02/03 Closed by ES-02/ES-03  
**Эпик-дом:** [`EPIC-M2-24-early-signal-pre-cluster`](../../epics/EPIC-M2-24-early-signal-pre-cluster.md)

## Tasks (docs — не код)

| S | Key | Task | Status | Depends |
|---|-----|------|--------|---------|
| 🔵 | GW-ES-01 | [Data readiness inventory](./TASK-GW-ES-01-early-signal-data-readiness-inventory.md) | 🔵 Done (Awaiting Commits) | — |
| ⚪ | GW-ES-04 | [REQ-48 PA.2 + spa-15 contract seam](./TASK-GW-ES-04-req48-spa15-contract-seam.md) | ⚪ Todo | TASK-ES-01 gap; operator PA.2 |

## Stories (код / закрытие public gaps)

| S | Key | Story | Status | Depends |
|---|-----|-------|--------|---------|
| 🔵 | GW-ES-02 | [Public Network Pulse L1 aggregates](./STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) → [pipeline](../../epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-02-public-network-pulse-l1-aggregates/STORY-GW-ES-02-public-network-pulse-l1-aggregates.md) | 🔵 Done (Awaiting Commits) pkg-000059 | REQ-49; gate PASS 2026-08-10 |
| 🔵 | GW-ES-03 | [Public Emerging L2 read](./STORY-GW-ES-03-public-emerging-l2-read.md) → [pipeline](../../epics/EPIC-M2-24-early-signal-pre-cluster/stories/STORY-GW-ES-03-public-emerging-l2-read/STORY-GW-ES-03-public-emerging-l2-read.md) | 🔵 Done (Awaiting Commits) pkg-000060 | REQ-50; P6 audit T08–T10 Done; G-ES-PUB-03 Closed |
| ⚪ | GW-ES-05 | [Network Pulse handler error-envelope](./STORY-GW-ES-05-network-pulse-handler-error-envelope.md) | ⚪ Todo (draft) | audit ES-02 G2; after ES-02 |
| ⏸ | GW-ES-06 | [Network Pulse SQL count perf](./STORY-GW-ES-06-network-pulse-sql-count-perf.md) | ⏸ Deferred (evidence-gated) | audit ES-02 G3 / open Q5 |
| ⚪ | GW-ES-07 | [Emerging Signals handler error-envelope](./STORY-GW-ES-07-emerging-signals-handler-error-envelope.md) | ⚪ Todo (draft) | audit ES-03 G1; after ES-03 |
| ⏸ | GW-ES-08 | [Emerging label-fold perf](./STORY-GW-ES-08-emerging-label-fold-perf.md) | ⏸ Deferred (evidence-gated) | audit ES-03 G2 |

**Progress:** Tasks **1 Done / 1 Todo**; Stories **2 Done** (ES-02/ES-03) + hygiene drafts ES-05/ES-07; Deferred ES-06/ES-08.

## Порядок

**TASK-ES-01** Done → **ES-02** Done → **ES-03** Done pkg-000060 + P6 T08–T10 → **TASK-ES-04**. Hygiene: **ES-05**–**ES-08** — not blocking.
