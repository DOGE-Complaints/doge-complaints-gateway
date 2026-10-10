# Gateway · scope dashboard

> **Scope-Id:** mvp  
> **Scope:** MVP  
> **SSOT:** package `INDEX.md` files + [bullrun-launch-index.md](bullrun-launch-index.md)  
> **Updated:** 2026-10-10T15:30:33Z  
> **Last change:** REQ56-01 P3 Done pkg-000111 (gate PASS · offline 10); REQ56-02 Todo; param `search` locked.

## Summary

| Metric | Value |
|--------|-------|
| Backlog packages | 12 |
| Active work items | 46 |
| Done | 42 |
| Todo / In Progress | 4 |
| Deferred | 3 |
| **Overall progress (active)** | **~91%** `███████████░` |

*Active = prior MVP Done + TASK-ES-04 Todo + REQ56-01 Done pkg-000111 + REQ56-02 Todo. Deferred вне %.*  
*SSR + REQ7 THR packages remain outside this denominator (separate scope dashboards).*  
*REQ9 + REQ10 + REQ11 + REQ56 packages are on this board (operator lock).*

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
| [req10-lifecycle-status-normalize](backlog-stories/req10-lifecycle-status-normalize/INDEX.md) | 2 | 2 | 0 | 0 | 100% `████████████` |
| [req11-demo-life-sim-fixtures-and-replay](backlog-stories/req11-demo-life-sim-fixtures-and-replay/INDEX.md) | 5 | 5 | 0 | 0 | 100% `████████████` |
| [req56-issues-server-text-search](backlog-stories/req56-issues-server-text-search/INDEX.md) | 2 | 0 | 1 | 1 | 50% `██████░░░░░░` |

*gpt-submit-authz: GAUTH-01/02 Superseded — excluded from story counts.*  
*cabinet-api: GW-CAB-03 Deferred (post-MVP web3).*  
*taxonomy-fidelity: TAX-01/02/03 Done; **TAX-04 Deferred**.*  
*early-signal: TASK-ES-01/ES-02/ES-03 Done; TASK-ES-04 Todo.*  
*req9-ops-parity-env-naming: REQ9-01 **Done** pkg-000096; REQ9-02 **Done** pkg-000097.*  
*req10-lifecycle-status-normalize: REQ10-01 **Done** pkg-000098; REQ10-02 **Done** pkg-000099; H8 skip this wave.*  
*req11-demo-life-sim: REQ11-01…05 **Done** pkg-000100…104 (05 PASS* live signup 429); auth lock → secrets file 1:1.*  
*req56-issues-server-text-search: REQ56-01 **Done** [`pkg-000111`](gateway-active-packages/pkg-000111-20261010-gw-req56-01-issues-list-search-filter.yaml) P3 gate PASS; REQ56-02 Todo; param `search`; TECH-ARCH linked.*

## Remaining

| Type | Key | Title | Package/Epic | Status | Priority | Essence |
|------|-----|-------|--------------|--------|----------|---------|
| Story | [STORY-GW-REQ56-01](backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md) → [pipeline](epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md) | Issues list `search` D-S1 filter | req56 | 🔵 Done | pkg-000111 | P3 gate PASS · offline 10 |
| Story | [STORY-GW-REQ56-02](backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md) | Document `search` API | req56 | ⚪ Todo | — | API_REFERENCE + openapi.yaml |
| Task | [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md) | REQ-48 PA.2 + spa-15 seam | early-signal | ⚪ Todo | — | Docs/contract; no API |

## Requirements (intake)

| REQ | Title | Status | Notes |
|-----|-------|--------|-------|
| [56](../requirements/56-issues-server-text-search.md) | Issues server text search (`search`) | Draft — PA.2 sync done | REQ56-01 pkg-000111 P1 scaffold; REQ56-02 Todo; TECH-ARCH linked; no product-root; SPA consumer after Ready |
| [55](../requirements/55-req11-demo-life-sim-fixtures-and-replay.md) | REQ11 — demo life sim fixtures + replay | Draft — stories Done | REQ11-01…05 Done pkg-000100…104 (05 PASS* live signup 429); Q3 auth → 05; siblings threads `04-…`, spa `20-…` |
| [54](../requirements/54-req10-lifecycle-status-normalize.md) | REQ10 — lifecycle_status normalize | Draft — awaiting PA.2 | REQ10-01/02 Done pkg-000098/099; siblings threads 03, spa 19; H8 skip |
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
| [EPIC-req10-lifecycle-status-normalize](epics/EPIC-req10-lifecycle-status-normalize.md) | 🔵 Done | pkg-000098 + pkg-000099 Done; not `EPIC-M2-*` |
| [EPIC-req11-demo-life-sim-fixtures-and-replay](epics/EPIC-req11-demo-life-sim-fixtures-and-replay.md) | 🔵 Done* | REQ11-01…05 Done pkg-000100…104 (05 PASS* live signup 429 ops leftover); not `EPIC-M2-*` |

## Roadmap → 100%

**Текущая точка:** active **43/46 (~93%)**. Remaining: **REQ56-02**, **TASK-ES-04**. Deferred: GW-CAB-03, GW-L10N-04, **GW-TAX-04**.

| Цель | Знаменатель | Как закрыть |
|------|-------------|-------------|
| **Активные 100%** | 46 work items | REQ56-01 → REQ56-02; TASK-ES-04 |
| **Полные 100%** | + 3 deferred | CAB-03, L10N-04, TAX-04 после web3 / product / ops residual |

### Упорядоченный остаток (active then deferred)

| # | Item | Почему здесь |
|---|------|--------------|
| 1 | [STORY-GW-REQ56-01](backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-01-issues-list-search-filter.md) | Server `search` filter (D-S1) |
| 2 | [STORY-GW-REQ56-02](backlog-stories/req56-issues-server-text-search/STORY-GW-REQ56-02-api-docs-search-param.md) | Docs after 01 |
| 3 | [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md) | Docs/PA.2 seam |
| — | [GW-TAX-04](backlog-stories/taxonomy-fidelity/STORY-GW-TAX-04-alter-story-labels-uuid-residual-hosts.md) | ALTER residual UUID hosts |
| — | [GW-CAB-03](backlog-stories/cabinet-api/STORY-GW-CAB-03-contribution-layer-api.md) / [GW-L10N-04](backlog-stories/localization-l10n/STORY-GW-L10N-04-label-taxonomy-registry-future.md) | Deferred post-MVP |

## §Now

1. **REQ56-01 Done pkg-000111:** [pipeline](epics/EPIC-req56-issues-server-text-search/stories/STORY-GW-REQ56-01-issues-list-search-filter/STORY-GW-REQ56-01-issues-list-search-filter.md) · next REQ56-02 docs; param **`search`** locked.
2. Lead product seam: [TASK-GW-ES-04](backlog-stories/early-signal-pre-cluster/TASK-GW-ES-04-req48-spa15-contract-seam.md).
3. REQ11 / REQ10 / REQ9 packages **closed** on this board.
4. Deferred TAX-04 / CAB-03 / L10N-04 — только по явному решению.

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
    "Done" : 38
    "Todo" : 5
```

## How to refresh

1. Recount: package `INDEX.md` + doc-task files (не из памяти).
2. Обновить этот файл по [`backlog-dashboard-template.md`](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-template.md).
3. `npm run dashboard:aggregate`
4. [`backlog-dashboard-maintenance.md`](../../../docs/methodology/Zeya888-builder-queue/workflow/backlog-dashboard-maintenance.md)
