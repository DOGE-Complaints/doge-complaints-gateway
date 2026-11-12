# task-gw-req11-04-t02-lock-b-service-auth-backdate

## Task: implement — lock-B service-auth backdate (T02)

## Meta
- **Story:** [STORY-GW-REQ11-04](../STORY-GW-REQ11-04-backdate-and-clustering-handoff.md)
- **Type:** implement
- **Status:** ✅ Done
- **Done at:** 2026-09-29T14:39:37Z
- **Package:** pkg-000103
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-29T14:33:30Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-04-backdate-and-clustering-handoff.md`

## Purpose
Implement **B**: service-auth controlled backdate **after** API create so fixture times can survive. Exact route/field names at P3 under lock B — **do not invent** public intake timestamp fields. Scope #1 · AC-GW-REQ1104-01.

## Code Facts
1. `created_at=now` at submit — `services.py:313`.
2. stash→submit: `tests/simulation_intake_http.py` `post_stash_and_submit_http`.
3. Operator lock B: service-auth after stash→submit (INDEX).
4. **As-of-Done (P3):** Lock-B path Present — `PATCH /ops/stories/{story_id}/created-at` + `StoryRepository.update_created_at` (InMemory/SQLite/Supabase).
5. **Historical (pre-P3):** Lock-B backdate product path Absent.

## Gap
**As-of-Done (P3):** closed — service-auth gated backdate after create (lock B).  
**Historical:** No service-auth controlled backdate after create (lock B).

## Acceptance / DoD
- [x] Service-auth gated backdate path exists (lock B; exact names from P3 proof)
- [x] No public intake timestamp field invent
- [x] No SQL dump as Pass
- [x] BULLRUN phases complete when closed

## Where to change
- Product service-auth surface + docs (P3); prefer extend existing authz

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
rg -n 'created_at|backdate|SERVICE_API' doge-complaints-gateway/src doge-complaints-gateway/tests --glob '*sim*' --glob '*intake*' | head -40
```
