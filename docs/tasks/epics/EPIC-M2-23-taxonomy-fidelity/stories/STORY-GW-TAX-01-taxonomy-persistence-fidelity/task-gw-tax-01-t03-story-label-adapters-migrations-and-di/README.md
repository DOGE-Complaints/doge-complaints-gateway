# task-gw-tax-01-t03-story-label-adapters-migrations-and-di

## Meta
- **Story:** [STORY-GW-TAX-01](../STORY-GW-TAX-01-taxonomy-persistence-fidelity.md)
- **Type:** implement
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000054
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Адаптеры in-memory/sqlite/supabase `story_labels` + миграция `story_labels(story_id,axis,label,disposition)` + DI (`providers.py`/`dependencies.py`/`service_factory.py`).

## Code Facts
- sqlite story persistence pattern — [`db_sqlite.py`](../../../../../../../../src/core/infrastructure/db_sqlite.py)
- supabase repos pattern — [`db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py)
- in-memory repos — [`repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py)
- DI wiring precedent — [`providers.py`](../../../../../../../../src/core/infrastructure/providers.py), [`service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py)
- `story_labels` table — **отсутствует** (grep src/ → 0)

## Acceptance / DoD
- [ ] Traces parent AC-2: adapters persist all labels with disposition
- [ ] Scope trace: backlog §2 storage D-TAX-2
- [ ] in-memory / sqlite / supabase adapters
- [ ] supabase migration `story_labels(story_id,axis,label,disposition)`
- [ ] DI wired in providers/dependencies/service_factory
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-tax-01-t03.md`](./acceptance-verification-gw-tax-01-t03.md) signed (Date post live-run only)

## Where to change
- [`src/core/infrastructure/repositories.py`](../../../../../../../../src/core/infrastructure/repositories.py)
- [`src/core/infrastructure/db_sqlite.py`](../../../../../../../../src/core/infrastructure/db_sqlite.py)
- [`src/core/infrastructure/db_supabase.py`](../../../../../../../../src/core/infrastructure/db_supabase.py)
- [`src/core/infrastructure/providers.py`](../../../../../../../../src/core/infrastructure/providers.py)
- [`src/core/infrastructure/service_factory.py`](../../../../../../../../src/core/infrastructure/service_factory.py)
- [`src/core/api/dependencies.py`](../../../../../../../../src/core/api/dependencies.py)
- [`supabase/migrations/`](../../../../../../../../supabase/migrations/) — new migration

## Out of scope
- Submit persist bridge (T04)
- Read-filter (T05)

## Verification commands (post live-run only)
```bash
rg -n "StoryLabel|story_labels" doge-complaints-gateway/src/core/infrastructure/
ls doge-complaints-gateway/supabase/migrations/*gw_tax_01* 2>/dev/null || true
```
