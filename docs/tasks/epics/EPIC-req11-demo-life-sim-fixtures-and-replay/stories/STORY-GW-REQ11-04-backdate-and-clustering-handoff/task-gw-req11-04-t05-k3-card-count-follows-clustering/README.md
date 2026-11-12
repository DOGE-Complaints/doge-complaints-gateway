# task-gw-req11-04-t05-k3-card-count-follows-clustering

## Task: docs — K3 card count follows clustering (T05)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** docs
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Package:** pkg-000103
- **Skill declared:** python-pro
- **Depends on:** T04 preferred
- **Scaffolded:** 2026-09-29T14:33:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`

## Purpose
Explicit note: board card count follows clustering (K3); no invent of new cluster product APIs. Scope #2 · AC-GW-REQ1104-03.

## Code Facts
1. K3 lock in parent REQ / INDEX.
2. Clustering produces board cards — product already; this story only documents handoff expectation.
3. **As-of-Done (P3):** K3 life-sim handoff note Present — note T05 (card count follows clustering; no invent cluster APIs).
4. **Historical (pre-P3):** K3 life-sim handoff note Absent.

## Gap
**As-of-Done (P3):** closed — explicit K3 note for life-sim handoff.  
**Historical:** No explicit K3 note tying card count to clustering for life-sim handoff.

## Acceptance / DoD
- [x] Note states board card count follows clustering (K3)
- [x] Explicit: no invent new cluster product APIs
- [x] Cross-link T04 wait runbook
- [x] BULLRUN phases complete when closed

## Where to change
- Same note family as T04 or short sibling under docs/analysis (P3)

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
rg -n 'K3|card count|clustering' doge-complaints-gateway/docs/analysis --glob '*req11*' | head -20
```
