# Inventory — STORY-GW-REQ10-01 lifecycle_status (P3)

- **Date:** 2026-09-28T17:16:40Z
- **Package:** `pkg-000098-20260928-gw-req10-01-lifecycle-status-inventory.yaml` (immutable)
- **Story:** STORY-GW-REQ10-01
- **Branch:** `dev`
- **Scope:** inventory only — no mapper/backfill/debug changes (→ REQ10-02)
- **H8:** skipped (operator lock)

## Method

- Hosted/test Supabase: PostgREST `GET /rest/v1/stories?select=lifecycle_status` (paginate; Prefer count=exact). Credentials from local `.env` / `.env.test` (not logged).
- Table used: `stories` (probe `doge_stories` → 404; `stories` → 162 rows).
- Fixtures/SQL: `rg` over `tests/`, `supabase/`, `src/` for `RECEIVED` / `received` / lifecycle string literals. No checked-in `*.db` / `*.sqlite` files.

## T01 — Hosted/test DISTINCT (`AC-GW-REQ1001-01`)

| Fact | Value |
|------|-------|
| Reachability | **OK** — `SUPABASE_URL` host reachable; service role present |
| Row count | 162 (`content-range` 0-161/162) |
| Distinct values | 4 |

| `lifecycle_status` | Count | Bucket (preview) |
|--------------------|------:|------------------|
| `clustered` | 140 | enum-legal |
| `ready_for_profile` | 20 | enum-legal |
| `RECEIVED` | 1 | normalize-to-accepted |
| `accepted` | 1 | enum-legal |

- `partial_ready`: **0** rows (enum-legal, not observed).
- lowercase `received`: **0** rows.
- RECEIVED row id (identifiers only): `story_id=6019633d-3876-469e-abe4-6002136ac84b` · created/updated `2026-05-27T10:22:47Z`.

No operator blocker — DB reachable.

## T02 — Fixture / sqlite / seed scan (`AC-GW-REQ1001-02`)

| Surface | `RECEIVED` / `received` as data | Notes |
|---------|----------------------------------|-------|
| `tests/**/*.py` | **absent** as lifecycle fixture values | Tests use `StoryLifecycleStatus.*` enum members |
| `supabase/**/*.sql` | **absent** as inserted values | Column declared `lifecycle_status text not null` only |
| Checked-in sqlite DB files | **none found** | — |
| `src/core/infrastructure/db_supabase.py:186-187` | present as **mapper keys** | Legacy map → `ACCEPTED` (product code; not a fixture) |
| `src/core/infrastructure/db_sqlite.py:225` | no legacy map | Strict `StoryLifecycleStatus(str(...))` |

Other non-enum lifecycle strings in fixtures/seeds: **none found** for story `lifecycle_status`.

## T03 — Closed list (`AC-GW-REQ1001-03`)

Canon enum (`src/core/domain/contracts.py:20-24`):

| Bucket | Values | Evidence |
|--------|--------|----------|
| **enum-legal** | `accepted`, `partial_ready`, `ready_for_profile`, `clustered` | contracts.py; hosted has 3 of 4 (`partial_ready` absent) |
| **normalize-to-accepted** | `RECEIVED`, `received` | Hosted: `RECEIVED`×1; `received`×0. Code-known map: `db_supabase.py:185-188` |
| **unexpected / fail-closed** | *(none observed in hosted DISTINCT)* | Any other non-enum string → fail-closed candidates for REQ10-02 |

Feeds REQ10-02: backfill the one `RECEIVED` row → `accepted`; then slim mapper / remove debug I/O. Do **not** keep permanent RECEIVED map.

## Non-goals (confirmed)

- No production UPDATE/backfill in this story.
- No mapper / debug-log removal.
- No H8 / `list_all` scale work.
- §Актуальная точка not rewritten.
