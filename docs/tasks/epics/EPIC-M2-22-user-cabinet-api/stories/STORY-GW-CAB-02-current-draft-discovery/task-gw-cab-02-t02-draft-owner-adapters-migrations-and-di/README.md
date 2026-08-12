# task-gw-cab-02-t02-draft-owner-adapters-migrations-and-di

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Адаптеры `DraftOwnerRepository` (in-memory / sqlite / supabase), миграция `draft_owner` + `story_drafts.updated_at` backfill, DI-проводка (backlog B.3–B.4).

## Code Facts
- sqlite `story_drafts` без `updated_at` — [`db_sqlite.py:202-207`](../../../../../../../../src/core/infrastructure/db_sqlite.py#L202)
- `SupabaseStoryDraftRepository` — [`db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py)
- `StoryDraftRepository` wired in-memory/sqlite/supabase — [`providers.py:146-248`](../../../../../../../../src/core/infrastructure/providers.py#L146)
- supabase migration `story_drafts` exists — [`supabase/migrations/20260703_1200_gw_draft_01_story_drafts.sql`](../../../../../../../../supabase/migrations/20260703_1200_gw_draft_01_story_drafts.sql)
- new migration path under `supabase/migrations/` for `draft_owner` + `updated_at`

## Acceptance / DoD
- [x] Traces parent AC-1, AC-4: TTL/expiry query in `get_current_draft` (`expires_at > now`)
- [x] Traces parent AC-5: `updated_at` column backfill `= created_at`
- [x] Scope trace: backlog §B.3–B.4
- [x] All backends: in-memory, sqlite, supabase
- [x] DI wiring in `providers.py` / `dependencies.py`
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t02.md`](./acceptance-verification-gw-cab-02-t02.md) signed

## Where to change
- [`src/core/infrastructure/repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/providers.py`](../../../../../../../../src/core/infrastructure/providers.py)
- [`supabase/migrations/`](../../../../../../../../supabase/migrations/) — new migration

## Out of scope
- HTTP association on read (T03)
- Route `/story-drafts/current` (T04)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -k 'draft_owner or cab_02' --tb=short
```
