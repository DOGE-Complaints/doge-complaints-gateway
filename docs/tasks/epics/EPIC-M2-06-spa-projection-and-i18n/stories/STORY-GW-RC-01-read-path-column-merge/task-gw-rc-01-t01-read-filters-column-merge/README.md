# task-gw-rc-01-t01

## Meta
- **Story:** [STORY-GW-RC-01](../STORY-GW-RC-01-read-path-column-merge.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000030
- **Skill declared:** python-pro

## Purpose
Ввести column-as-truth merge в read-path: 4-tuple rows `(issue_id, row_status, payload, created_at)`, helper `merge_projection_columns`, фильтр `?status=` по колонке `row_status` (D-RC-2).

## Code Facts
- `filter_projection_rows` возвращает только `dict(payload)` — [`read_filters.py:209-235`](../../../../../../../src/core/projection/read_filters.py#L209-L235)
- Фильтр статуса по `payload.get("status")` — [`read_filters.py:210-213`](../../../../../../../src/core/projection/read_filters.py#L210-L213)
- Unit-тесты фильтра используют 3-tuple rows — [`test_filter_projection_rows_contract.py`](../../../../../../../tests/test_filter_projection_rows_contract.py)

## Acceptance / DoD
- Traces parent AC: неполный payload → ответ содержит `id`/`status` из колонок (unit level)
- Traces parent AC: фильтр `?status=` по колонке (unit level)
- `merge_projection_columns`: column overrides JSON; `created_at` опционален если колонка пуста
- `test_filter_projection_rows_contract.py` обновлён под 4-tuple + merge
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — `merge_projection_columns`, `filter_projection_rows` signature + status filter
- `tests/test_filter_projection_rows_contract.py` — row tuples + merge assertions

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_filter_projection_rows_contract.py -q
```
