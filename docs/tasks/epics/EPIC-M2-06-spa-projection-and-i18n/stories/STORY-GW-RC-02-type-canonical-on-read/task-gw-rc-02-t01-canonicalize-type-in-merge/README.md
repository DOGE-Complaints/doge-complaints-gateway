# task-gw-rc-02-t01

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro

## Purpose
В сборке ответа read-path нормализовать `type` к канону (после merge из RC-01). Единый choke-point в `merge_projection_columns` — все бэкенды (Supabase, SQLite, InMemory) наследуют без отдельных store-тасков.

## Code Facts
- `merge_projection_columns` не трогает `type` — [`read_filters.py:188-200`](../../../../../../../src/core/projection/read_filters.py#L188-L200)
- Канон enum UPPERCASE — [`enums.py:14-19`](../../../../../../../src/core/projection/enums.py#L14-L19)
- Все list/get вызывают merge — [`db_supabase.py:720`](../../../../../../../src/core/infrastructure/db_supabase.py), [`db_sqlite.py:672`](../../../../../../../src/core/infrastructure/db_sqlite.py), [`repositories.py:249`](../../../../../../../src/core/infrastructure/repositories.py)
- Write-path уже канон — [`dto.py:26-31`](../../../../../../../src/core/projection/dto.py#L26-L31)

## Acceptance / DoD
- Traces parent AC: `GET` list/get отдают `type` в каноне для known legacy lowercase (unit via `merge_projection_columns`)
- Helper `canonicalize_issue_type_on_read()` (или эквивалент) вызывается из `merge_projection_columns`
- Known values `improvement`/`service_request`/`incident` (any case) → `{IMPROVEMENT, SERVICE_REQUEST, INCIDENT}`
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — helper + wire в `merge_projection_columns`
- Опц. `src/core/projection/validation.py` — рядом с `validate_governed_enums`

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_filter_projection_rows_contract.py -q -k type
```
