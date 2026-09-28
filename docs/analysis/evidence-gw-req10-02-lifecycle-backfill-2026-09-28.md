# Evidence — STORY-GW-REQ10-02 lifecycle backfill + fixtures (P3)

- **Date:** 2026-09-28T17:44:10Z
- **Package:** `pkg-000099-20260928-gw-req10-02-lifecycle-backfill-and-mapper-cleanup.yaml` (immutable)
- **Story:** STORY-GW-REQ10-02
- **Branch:** `dev`
- **H8:** skipped

## T01 — Hosted/test RECEIVED → accepted (`AC-GW-REQ1002-01`)

| Fact | Value |
|------|-------|
| Inventory feed | [`inventory-gw-req10-01-lifecycle-status-2026-09-28.md`](./inventory-gw-req10-01-lifecycle-status-2026-09-28.md) — `RECEIVED`×1 · `story_id=6019633d-3876-469e-abe4-6002136ac84b` |
| PostgREST reachability (P3 re-probe) | **OK** — HTTP 200 to `/rest/v1/stories` (host `*.supabase.co`) |
| `lifecycle_status=eq.RECEIVED` | **0** rows (`content-range */0`) |
| Inventory target row by `story_id` | **not found** (`n=0`) |
| Full `stories` SELECT lifecycle | **`content-range */0`** (0 rows) — **≠** inventory 162-row DISTINCT |

### Operator blocker (T01)

Hosted endpoint is reachable but returns an **empty** `stories` table relative to REQ10-01 inventory (162 rows). Cannot evidence PATCH of inventory `RECEIVED`→`accepted` against the inventory project/data set. Possible env/project mismatch or emptied DB — **operator must re-point credentials / re-verify** when the inventory project is available.

No elaborate migration written. Simple cleanup deferred until hosted data matches inventory.

## T02 — Fixture / SQL confirm (`AC-GW-REQ1002-01` fixtures branch)

Re-`rg` at P3 (2026-09-28T17:44:10Z):

| Surface | Result |
|---------|--------|
| `tests/`, `supabase/` `*.{sql,py,json,yml,yaml}` as **data** | **absent** `RECEIVED`/`received` fixture/seed values |
| Mentions of `RECEIVED` | only in new assert/test file `tests/test_gw_req10_02_lifecycle_parse.py` (fail-closed / source-scan — not fixture data) |
| Checked-in sqlite | none |

**Decision:** fixture rewrite **N/A** (inventory claim confirmed).

## Product follow-through (same wave)

- Mapper slim + debug I/O removal: `src/core/infrastructure/db_supabase.py` `_parse_lifecycle_status`
- Tests: `tests/test_gw_req10_02_lifecycle_parse.py` — 11 passed (story file); lifecycle suite 24 passed with repository tests
