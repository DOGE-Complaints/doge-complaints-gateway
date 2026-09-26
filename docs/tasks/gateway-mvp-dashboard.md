# Gateway · scope dashboard

> **Scope-Id:** mvp  
> **Scope:** MVP  
> **SSOT:** package `INDEX.md` files + [bullrun-launch-index.md](bullrun-launch-index.md)  
> **Updated:** 2026-09-26T12:31:20Z  
> **Last change:** STORY-GW-REQ9-02 **Done** pkg-000097 T01–T04 — `make test` / `test-live`; audit G1 CLOSED (ops lock C); REQ9 package complete.

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | 9 |
| Active work items | 37 |
| Done | 36 |
| Todo / In Progress | 1 |
| Deferred | 3 |
| **Overall progress (active)** | **~97%** `███████████░` |

*Active = prior 35 MVP items + 2 REQ9 ops stories. Deferred вне %.*  
*SSR + REQ7 THR packages remain outside this denominator (separate scope dashboards).*  
*REQ9 package is **ops parity** on this board (operator lock B) — not a product feature slice.*

## By package

| Package | Stories | Done | Todo | Deferred | Progress |
|---------|---------|------|------|----------|----------|
| [story-draft-handoff](backlog-stories/story-draft-handoff/INDEX.md) | 7 | 7 | 0 | 0 | 100% `████████████` |
| [issues-read-contract](backlog-stories/issues-read-contract/INDEX.md) | 8 | 8 | 0 | 0 | 100% `████████████` |
| [demo-data-seeding](backlog-stories/demo-data-seeding/INDEX.md) | 4 | 4 | 0 | 0 | 100% `████████████` |
| [localization-l10n](backlog-stories/localization-l10n/INDEX.md) | 4 | 3 | 0 | 1 | 75% `█████████░░░` |
| [gpt-submit-authz](backlog-stories/gpt-submit-authz/INDEX.md) | 2 | 2 | 0 | 0 | 100% `████████████` |
| [cabinet-api](backlog-stories/cabinet-api/INDEX.md) | 3 | 2 | 0 | 1 | 67% `████████░░░░` |
| [taxonomy-fidelity](backlog-stories/taxonomy-fidelity/INDEX.md) | 4 | 3 | 0 | 1 | 100% active `████████████` |
| [early-signal-pre-cluster](backlog-stories/early-signal-pre-cluster/INDEX.md) | 4 items | 3 | 1 | 0 | 75% `█████████░░░` |
| [req9-ops-parity-env-naming](backlog-stories/req9-ops-parity-env-naming/INDEX.md) | 2 | 2 | 0 | 0 | 100% `████████████` |

*gpt-submit-authz: GAUTH-01/02 Superseded — excluded from story counts.*  
*cabinet-api: GW-CAB-03 Deferred (post-MVP web3).*  
*taxonomy-fidelity: TAX-01/02/03 Done; **TAX-04 Deferred**.*  
*early-signal: TASK-ES-01/ES-02/ES-03 Done; TASK-ES-04 Todo.*  
*req9-ops-parity-env-naming: REQ9-01 **Done** pkg-000096; REQ9-02 **Done** pkg-000097.*

## Remaining

| Type | Key | Title | Package/Epic | Status | Priority | Essence |
|------|-----|-------|--------------|--------|----------|---------|
| Task | [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md) | REQ-48 PA.2 + spa-15 seam | early-signal | ⚪ Todo | — | Docs/contract; no API |

## Requirements (intake)

| REQ | Title | Status | Notes |
|-----|-------|--------|-------|
| [53](../requirements/53-req9-ops-parity-env-naming.md) | REQ9 — ops parity & env naming | Draft — awaiting PA.2 | REQ9-01/02 Done pkg-000096/097; siblings aibridge REQ-08, threads 02, identity 22, spa 18 |
| [48](../requirements/48-early-signal-pre-cluster-data-readiness.md) | Early Signal / Pre-Cluster — Data Readiness (no invented API) | Draft — awaiting PA.2 | ES-02/03 Done; TASK-ES-04 Todo; sibling spa 15 |

## Doc-tasks Done (в active %)

| Key | Package | Evidence |
|-----|---------|----------|
| [DOC-TASK-CRON-SCOPE-01](backlog-stories/demo-data-seeding/DOC-TASK-CRON-SCOPE-01-clarify-cron-in-mvp.md) | demo-data-seeding | Done 2026-07-23 — MVP-cron vs post-demo automation в доке |
| [DOC-TASK-CRON-SCOPE-02](backlog-stories/demo-data-seeding/DOC-TASK-CRON-SCOPE-02-architecture-ssot-mvp-cron.md) | demo-data-seeding | Done 2026-07-23 — Architecture SSOT G1–G4 caveat MVP-cron |
| [DOC-TASK-DRAFT-OWNERSHIP-01](backlog-stories/cabinet-api/DOC-TASK-DRAFT-OWNERSHIP-01-clarify-capability-model.md) | cabinet-api | Done 2026-07-23 — capability + first-wins `set_owner` для story-drafts |
| [TASK-GW-ES-01](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-01-early-signal-data-readiness-inventory.md) | early-signal-pre-cluster | Done 2026-08-09 — [gap-analysis](backlog-stories/early-signal-pre-cluster/gap-analysis-early-signal-data-readiness-2026-08-09.md) SSOT |

## Epic rollup

| Epic | Status | Notes |
|------|--------|-------|
| [EPIC-M2-21](epics/) | Done (Awaiting Commits) | DRAFT-01..07 Done; pkg-000056 |
| EPIC-M2-06 | Done (package) | PUBLIC-01 Done; L10N-04 deferred |
| EPIC-M2-19 | Done (Awaiting Commits) | SEED-01..04 Done; hosted board 9 cards |
| EPIC-M2-20 | Done | GAUTH historical; superseded user path |
| EPIC-M2-22 | In Progress | CAB-01/02 Done; **GW-CAB-03 Deferred** post-MVP |
| EPIC-M2-23 | Done active / Deferred hygiene | TAX-01/02/03 Done; **TAX-04 Deferred** |
| [EPIC-M2-24](epics/EPIC-M2-24-early-signal-pre-cluster.md) | ES-02/ES-03 Done | TASK-ES-04 Todo |
| [EPIC-req9-ops-parity-env-naming](epics/EPIC-req9-ops-parity-env-naming.md) | 🔵 Done | pkg-000096 + pkg-000097 Done; not `EPIC-M2-*` |

## Roadmap → 100%

**Текущая точка:** active **36/37 (~97%)**. Remaining: **TASK-ES-04**. Deferred: GW-CAB-03, GW-L10N-04, **GW-TAX-04**.

| Цель | Знаменатель | Как закрыть |
|------|-------------|-------------|
| **Активные 100%** | 37 work items | TASK-ES-04 |
| **Полные 100%** | + 3 deferred | CAB-03, L10N-04, TAX-04 после web3 / product / ops residual |

### Упорядоченный остаток (active then deferred)

| # | Item | Почему здесь |
|---|------|--------------|
| 1 | [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md) | Docs/PA.2 seam |
| — | [GW-TAX-04](backlog-stories/taxonomy-fidelity/STORY-GW-TAX-04-alter-story-labels-uuid-residual-hosts.md) | ALTER residual UUID hosts |
| — | [GW-CAB-03](backlog-stories/cabinet-api/STORY-GW-CAB-03-contribution-layer-api.md) / [GW-L10N-04](backlog-stories/localization-l10n/STORY-GW-L10N-04-label-taxonomy-registry-future.md) | Deferred post-MVP |

## §Now

1. Lead product seam: [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md).
2. REQ9 ops package **closed** (REQ9-01 pkg-000096; REQ9-02 pkg-000097).
3. Deferred TAX-04 / CAB-03 / L10N-04 — только по явному решению.

## §Deferred

- [GW-TAX-04](backlog-stories/taxonomy-fidelity/STORY-GW-TAX-04-alter-story-labels-uuid-residual-hosts.md) — ALTER `story_labels` на residual UUID hosts (TAX-03 audit G2).
- [GW-CAB-03](backlog-stories/cabinet-api/STORY-GW-CAB-03-contribution-layer-api.md) — contribution API; нет MVP-источника `TxReceipt` (отложено 2026-07-14).
- [GW-L10N-04](backlog-stories/localization-l10n/STORY-GW-L10N-04-label-taxonomy-registry-future.md) — полный реестр меток; порог ≥50 label-miss / 7 дней.

## §Retired (optional)

- **GW-DEPLOY-01** — удалён; as-built [`railpack.json`](../../railpack.json). Closure: [retire-STORY-GW-DEPLOY-01-2026-07-10.md](../analysis/retire-STORY-GW-DEPLOY-01-2026-07-10.md)

## §Deploy (optional)

Gateway на Railway: [`railpack.json`](../../railpack.json) + env (`SERVICE_API_TOKEN`, `IDENTITY_BASE_URL`, `SPA_BASE_URL`, `DB_BACKEND=supabase`, `CORS_ALLOWED_ORIGINS`). Hosted readiness: [`REQUIRED_READINESS_TABLES`](../../src/core/infrastructure/db_supabase.py) incl. `story_labels` (DRAFT-07 Done).

## Mermaid — completion

```mermaid
pie title Active work items (MVP)
    "Done" : 34
    "Todo" : 3
```

## How to refresh

1. Recount: package `INDEX.md` + doc-task files (не из памяти).
2. Обновить этот файл по [`backlog-dashboard-template.md`](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-template.md).
3. `npm run dashboard:aggregate`
4. [`backlog-dashboard-maintenance.md`](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md)
