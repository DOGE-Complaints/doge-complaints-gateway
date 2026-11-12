# task-gw-req11-06-t02-fk-safe-gateway-deletes

## Task: implement / tooling — FK-safe gateway deletes (T02)

## Meta
- **Story:** [STORY-GW-REQ11-06](../STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md)
- **Type:** implement / tooling
- **Status:** ✅ Done
- **Done at:** 2026-09-30T07:56:35Z
- **Package:** pkg-000105
- **Skill declared:** python-pro
- **Depends on:** T01
- **Scaffolded:** 2026-09-30T07:51:07Z
- **Decision Ref:** `doge-complaints-gateway/docs/tasks/backlog-stories/req11-demo-life-sim-fixtures-and-replay/STORY-GW-REQ11-06-wipe-node-content-stories-derivatives.md`

## Purpose
Service-role DELETE for **only** `REQUIRED_READINESS_TABLES` in FK-safe order (child→parent from verified schema). Scope #2 · AC-GW-REQ1106-02 (gateway stack). Name ≠ create until P3.

## Code Facts
1. Verified table set (`src/core/infrastructure/db_supabase.py` `REQUIRED_READINESS_TABLES`): `stories`, `idempotency_keys`, `story_embeddings`, `doge_issues`, `doge_issue_embeddings`, `issue_candidates`, `review_audit_log`, `issue_story_links`, `story_signals`, `cluster_memberships`, `story_drafts`, `story_labels`.
2. Env: `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE` (profile from REQ11-02).
3. **Do not invent** table names outside this frozenset / sqlite schema evidence.
4. **Do not** touch Identity `auth.users` / admin.

## Gap
**As-of-Done (P3):** closed.

No ordered gateway wipe path on disk.

## Acceptance / DoD
- [x] Deletes cover readiness tables only (AC-02 gateway)
- [x] FK-safe order documented in code/comments from schema evidence
- [x] No Identity / auth.users paths
- [x] BULLRUN phases complete when closed

## Where to change
- `tests/sandbox/life_sim_wipe_node_content.py` (gateway delete plan; P3)
- Evidence: `db_supabase.py` `REQUIRED_READINESS_TABLES`; sqlite schema as needed

## Out of scope
Confirm gate (T01); threads (T03); dry-run/docs (T04); tests (T05); gate (T06); invent tables/HTTP; DROP schema; Identity DELETE.
- Overlay bans:
  - Stay `dev`.
  - Confirm: `--confirm-wipe` / `LIFE_SIM_WIPE_CONFIRMED=1`.
  - Tables: `REQUIRED_READINESS_TABLES` only for gateway.
  - No Identity DELETE; no invent wipe HTTP.
  - Pointer pkg-000105; do not mutate pkg-000100…104.
  - Do not rewrite §Актуальная точка.

## Verification commands
```bash
rg -n 'REQUIRED_READINESS_TABLES' doge-complaints-gateway/src/core/infrastructure/db_supabase.py | head -20
# after P3: assert wipe script table list ⊆ REQUIRED_READINESS_TABLES
```
