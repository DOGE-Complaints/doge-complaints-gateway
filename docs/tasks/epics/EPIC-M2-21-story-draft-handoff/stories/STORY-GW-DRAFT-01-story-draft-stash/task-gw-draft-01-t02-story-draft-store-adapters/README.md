# task-gw-draft-01-t02-story-draft-store-adapters

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Реализовать 3 адаптера `StoryDraftRepository` (in_memory, sqlite, supabase) и проводку в `ServiceFactory` per `DB_BACKEND`; TTL через `expires_at` (D-DRAFT-2 C+D).

## Code Facts
- In-memory pattern — [`infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- SQLite — [`infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- Supabase — [`infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- DI — [`service_factory.py:48-49`](../../../../../../../src/core/infrastructure/service_factory.py)

## Acceptance / DoD
- Traces parent AC #5: TTL → expired draft returns None / 404 at route layer
- Traces parent AC #6: draft store separate from `StoryRepository`
- All three backends wired in `ServiceFactory`
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`src/core/infrastructure/repositories.py`](../../../../../../../src/core/infrastructure/repositories.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../src/core/infrastructure/service_factory.py)

## Out of scope
HTTP routes; supabase migration file (document in acceptance if deferred)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'StoryDraft' src/core/infrastructure/
```
