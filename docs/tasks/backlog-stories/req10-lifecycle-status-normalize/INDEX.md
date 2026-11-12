# REQ10 lifecycle_status normalize (gateway) · index

**Зона:** `doge-complaints-gateway/docs/tasks/backlog-stories/req10-lifecycle-status-normalize/`  
**Тип:** backlog (постановки; P1.3/P3 — после активации pkg).  
**Метод:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc)  
**Parent REQ:** [`54-req10-lifecycle-status-normalize.md`](../../../requirements/54-req10-lifecycle-status-normalize.md)  
**Parent product:** [`REQ10-DOGEstonia-Threads-Board-Architecture-Hardening.md`](../../../../../docs/requirements%20backlog/REQ10-DOGEstonia-Threads-Board-Architecture-Hardening.md) §3.4, §6.3, §7.1 H1/H4  
**Justification:** [`audit-threads-board-persist-clean-vs-hack-2026-09-27.md`](../../../../../docs/analysis/audit-threads-board-persist-clean-vs-hack-2026-09-27.md) §3, §8  
**Dashboard:** [`gateway-mvp-dashboard.md`](../../gateway-mvp-dashboard.md) (operator lock: sync MVP board)  
**Naming:** `STORY-GW-REQ10-*`  
**Updated:** 2026-09-28T17:52:28Z · REQ10-02 P6 T07 G3 CLOSED (`gw_req10_02_audit_followup`)  
**Epic:** [`EPIC-req10-lifecycle-status-normalize.md`](../../epics/EPIC-req10-lifecycle-status-normalize.md)  
**Active pkg:** [`pkg-000099`](../../gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml)
---

## Контекст одной фразой

Gateway: нормализовать тестовые/hosted `lifecycle_status` (`RECEIVED`→`accepted`), убрать постоянный legacy map и debug file I/O; unknown — fail closed. H8 `list_all` scale — вне этой волны.

---

## Operator locks (clarifying 2026-09-28)

| Theme | Decision |
|-------|----------|
| Dashboard | sync `gateway-mvp-dashboard.md` (no separate REQ10 scope dashboard) |
| H8 / `list_all` scale | **skip** этой волны — не AC, не Deferred story |
| Test/hosted data | **чистим в канон сразу**; без усложнения dual-path; permanent RECEIVED map не оставлять |

---

## Stories

| Key | File | Status | Depends |
|-----|------|--------|---------|
| STORY-GW-REQ10-01 | [backlog](./STORY-GW-REQ10-01-lifecycle-status-inventory.md) → [pipeline](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/STORY-GW-REQ10-01-lifecycle-status-inventory.md) · [pkg-000098](../../gateway-active-packages/pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml) | Done P3 2026-09-28T17:16:40Z · [inventory](../../analysis/inventory-gw-req10-01-lifecycle-status-2026-09-28.md) · [gate](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-01-lifecycle-status-inventory/task-gw-req10-01-t04-story-gate/story-acceptance-gate-STORY-GW-REQ10-01.md) | — |
| STORY-GW-REQ10-02 | [backlog](./STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md) → [pipeline](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup.md) · [pkg-000099](../../gateway-active-packages/pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml) | Done P3 2026-09-28T17:44:10Z · [evidence](../../analysis/evidence-gw-req10-02-lifecycle-backfill-2026-09-28.md) · [gate](../../epics/EPIC-req10-lifecycle-status-normalize/stories/STORY-GW-REQ10-02-lifecycle-backfill-and-mapper-cleanup/task-gw-req10-02-t06-story-gate/story-acceptance-gate-STORY-GW-REQ10-02.md) · [run-summary](../../run-reports/run-summary-20260928-1744-gw-req10-02-p3.md) | REQ10-01 Done |

---

## Out of package

- Threads tree/reactions; spa UI  
- Invent new public APIs; REQ8  
- H8 stretch (document `list_all` / SQL aggregate) — Wave F later  
- Mandatory pulse SQL aggregate  
