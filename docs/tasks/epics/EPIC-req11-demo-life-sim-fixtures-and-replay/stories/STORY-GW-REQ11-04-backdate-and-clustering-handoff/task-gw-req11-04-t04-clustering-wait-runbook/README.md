# task-gw-req11-04-t04-clustering-wait-runbook

## Task: docs / tooling — clustering wait runbook (T04)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** docs / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Package:** pkg-000103
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-29T14:33:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`

## Purpose
Runbook/script documents wait for clustering (`CLUSTER_MIN_SIZE` / cron) before sibling threads social seed handoff (GW-11-07). Scope #2 · AC-GW-REQ1104-02. Do **not** invent new cluster product APIs.

## Code Facts
1. `CLUSTER_MIN_SIZE=8` — `example.env:69`.
2. `CLUSTER_CRON_ENABLED` / `CLUSTER_CRON_INTERVAL_S` — `example.env:99–100`.
3. **As-of-Done (P3):** Clustering wait handoff Present — note T04 + `tests/sandbox/life_sim_wait_clustering.sh`.
4. **Historical (pre-P3):** Life-sim clustering wait handoff Absent.

## Gap
**As-of-Done (P3):** closed — runbook/script documents wait before threads seed handoff.  
**Historical:** No runbook/script for clustering wait before threads seed handoff.

## Acceptance / DoD
- [x] Runbook/script documents wait using CLUSTER_MIN_SIZE / cron knobs
- [x] Handoff points to sibling threads seed (out of scope to implement)
- [x] No invent new cluster product APIs
- [x] BULLRUN phases complete when closed

## Where to change
- docs/analysis or docs/runtime-docs note + optional helper script (P3)

## Out of scope
Threads seed; spa verify; public intake timestamp invent; SQL dump Pass; invent public/cluster APIs; reopen REQ11-01…03 product.
- Overlay bans:
  - Stay `dev`.
  - Lock **B**: service-auth after stash→submit; **no invent** public intake timestamp fields.
  - Pointer pkg-000103; do not mutate pkg-000100…102.
  - No threads seed / spa verify / SQL dump Pass; no invent public/cluster APIs.
  - No secrets in git.

## Verification commands
```bash
rg -n 'CLUSTER_MIN_SIZE|CLUSTER_CRON' doge-complaints-gateway/example.env doge-complaints-gateway/docs | head -20
```
