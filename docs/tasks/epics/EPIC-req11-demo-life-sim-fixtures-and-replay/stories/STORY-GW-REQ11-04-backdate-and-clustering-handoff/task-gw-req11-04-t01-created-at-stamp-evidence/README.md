# task-gw-req11-04-t01-created-at-stamp-evidence

## Task: docs / evidence — created_at stamp evidence (T01)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** docs / evidence
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Package:** pkg-000103
- **Skill declared:** python-pro
- **Depends on:** —
- **Scaffolded:** 2026-09-29T14:33:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`

## Purpose
Evidence note: `created_at=now` write sites + existing service-auth surfaces usable for lock B. Scope #1 prep · AC-GW-REQ1104-01. Do **not** invent public intake timestamp fields.

## Code Facts
1. Submit stamps `created_at=now` — `src/core/application/services.py:313` (story also cites `:579`).
2. Service-auth patterns exist elsewhere (e.g. draft/stash routes); reuse surfaces at P3 under lock B — do not invent public intake fields.
3. Fixture `created_at` values on disk: REQ11-01 `dogestonia_life_sim_stories_v0_1.json`.
4. **As-of-Done (P3):** stamp evidence + service-auth candidates in [`note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md`](../../../../../../analysis/note-gw-req11-04-backdate-and-clustering-handoff-2026-09-29.md) T01.
5. **Historical (pre-P3):** Intake backdate path Absent; no written evidence note of stamp sites + lock-B candidates.

## Gap
**As-of-Done (P3):** closed — evidence note lists stamp sites + service-auth surfaces.  
**Historical:** No written evidence of stamp sites + candidate service-auth surfaces for lock B.

## Acceptance / DoD
- [x] Evidence note lists `created_at=now` sites with paths
- [x] Candidate service-auth surfaces named without inventing public intake timestamp fields
- [x] BULLRUN phases complete when closed

## Where to change
- docs/analysis/ note (path chosen at P3); cite services.py only

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
rg -n 'created_at=now|created_at' doge-complaints-gateway/src/core/application/services.py | head -20
```
