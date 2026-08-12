# task-gw-cab-01-t02-repository-list-stories-by-submitter

## Meta
- **Story:** [STORY-GW-CAB-01](../STORY-GW-CAB-01-story-activity-api.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000052
- **Skill declared:** python-pro
- **Depends on:** T01 (D-CAB01-4)

## Purpose
Добавить эффективный user-scoping на уровне persistence: `StoryRepository.list_stories_by_submitter(submitter_external_user_id)` в sqlite + supabase (per D-CAB01-4).

## Code Facts
- Protocol — [`contracts.py:70-87`](../../../../../../../../src/core/domain/contracts.py#L70) `StoryRepository` (no list_by_submitter)
- Sqlite stories table — [`db_sqlite.py:183`](../../../../../../../../src/core/infrastructure/db_sqlite.py#L183) `submitter_external_user_id TEXT NOT NULL`
- Supabase select columns — [`db_supabase.py:65`](../../../../../../../../src/core/infrastructure/db_supabase.py#L65) includes `submitter_external_user_id`
- In-memory repo — [`repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py) `StoryRepository` impl

## Acceptance / DoD
- [x] Traces parent AC-2: filter by author `sub` via `submitter_external_user_id`
- [x] `list_stories_by_submitter` on `StoryRepository` protocol + all backends (sqlite, supabase, in-memory)
- [x] DB-level filter (not `list_stories()` + app filter) per D-CAB01-4
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-01-t02.md`](./acceptance-verification-gw-cab-01-t02.md) signed

## Where to change
- [`src/core/domain/contracts.py`](../../../../../../../../src/core/domain/contracts.py) — protocol method
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py)

## Out of scope
- HTTP route (T04)
- Status/metrics aggregation (T03)

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q -k 'cab_01 and submitter' --tb=short
# or unit tests added in T05
```
