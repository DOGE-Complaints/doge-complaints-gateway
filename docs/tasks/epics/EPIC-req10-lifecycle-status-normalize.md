# EPIC-req10-lifecycle-status-normalize: REQ10 lifecycle_status normalize (gateway)

## Epic Meta
- Status: 🟢 Done product wave (REQ10-01 + REQ10-02 P3 Done pkg-000098/099; H8 skip)
- Priority: High (REQ10 / REQ54)
- Type: backlog package epic (not EPIC-M2-*)
- **Пакет:** [`req10-lifecycle-status-normalize/`](../backlog-stories/req10-lifecycle-status-normalize/INDEX.md)
- **Parent REQ:** [`54-req10-lifecycle-status-normalize.md`](../requirements/54-req10-lifecycle-status-normalize.md)
- **Parent product:** REQ10 §3.4, §6.3, §7.1 H1/H4
- **Justification:** [`audit-threads-board-persist-clean-vs-hack-2026-09-27.md`](../../../docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md) §3, §8
- **Dashboard:** [`gateway-mvp-dashboard.md`](../gateway-mvp-dashboard.md) — ops/hardening (operator lock)
- **Git:** `dev` (no separate package branch)
- **Scaffolded:** 2026-09-28T17:11:07Z
- **Updated:** 2026-09-28T17:44:10Z (REQ10-02 P3 Done pkg-000099)

## Problem Statement

Gateway: inventory distinct hosted/test `lifecycle_status` values; normalize legacy `RECEIVED`→`accepted`, slim mapper, remove debug file I/O. Unknown values fail closed. H8 `list_all` scale — out of this wave.

## Soft (backlog)

- Soft (backlog): REQ10-01 lifecycle_status inventory — **Done** P3 2026-09-28T17:16:40Z pkg-000098 T01–T04 · [inventory](../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md)
- Soft (backlog): REQ10-02 backfill + mapper cleanup — **Done** P3 2026-09-28T17:44:10Z pkg-000099 T01–T06 · [evidence](../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) · [run-summary](../run-reports/run-summary-20260928-1744-gw-req10-02-p3.md)

## Stories

| Story | Pipeline / backlog | Status |
|-------|--------------------|--------|
| STORY-GW-REQ10-01 | [pipeline](./EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/STORY-GW-REQ10-01-lifecycle-status-inventory.md) → [backlog](../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-01-lifecycle-status-inventory.md) · [pkg-000098](../gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml) | 🔵 Done P3 2026-09-28T17:16:40Z |
| STORY-GW-REQ10-02 | [pipeline](./EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md) → [backlog](../backlog-stories/req10-lifecycle-status-normalize/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md) · [pkg-000099](../gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml) | 🔵 Done P3 2026-09-28T17:44:10Z |

## Decision Ref
- Backlog INDEX + `$storyFile` REQ10-02
- REQ 54 · REQ10 · audit §3/§8 · inventory feed REQ10-01
- Operator locks: dashboard sync; H8 skip; clean to canon; no permanent RECEIVED map
