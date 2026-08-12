# task-gw-l10n-03-t02

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
Domain port + InMemory/Sqlite/Supabase repositories; upsert increment `count`, touch `last_seen_at`; wire `providers.py` and `DefaultServiceFactory`.

## Code Facts
- `src/core/infrastructure/providers.py:133-156` — sqlite backend wiring
- `src/core/infrastructure/db_supabase.py` — Supabase repository pattern
- `src/core/infrastructure/service_factory.py:42-60` — factory fields

## Acceptance / DoD
- Traces: AC2 (повтор агрегируется/накапливается)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- New port (e.g. `LabelTranslationMissRepository` protocol)
- `core/infrastructure/repositories/` or `db_sqlite.py` / `db_supabase.py` implementations
- `providers.py` + `DefaultServiceFactory` + `ApiDependencies` if needed

## Verification commands
```bash
pytest tests/ -q -k label_miss_repository --ignore=tests/smoke --ignore=tests/integration
```
