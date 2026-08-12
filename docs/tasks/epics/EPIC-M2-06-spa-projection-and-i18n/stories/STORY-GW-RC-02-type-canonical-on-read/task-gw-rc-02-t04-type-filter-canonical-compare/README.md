# task-gw-rc-02-t04

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Фильтр `?type=IMPROVEMENT` должен матчить payload с legacy `type:"improvement"`. Бэк гарантирует канон для фильтрации (parent AC-2, бэкенд-часть).

## Code Facts
- `_matches_post_fetch_filters` сравнивает сырой `payload.get("type")` — [`read_filters.py:161`](../../../../../../../src/core/projection/read_filters.py#L161)
- Фильтр применяется **до** merge в `filter_projection_rows` — [`read_filters.py:231-246`](../../../../../../../src/core/projection/read_filters.py#L231-L246)

## Acceptance / DoD
- Traces parent AC: `?type=IMPROVEMENT` возвращает issue с payload `type:"improvement"`
- Canonical compare (reuse `canonicalize_issue_type_on_read` или shared helper)
- Unit test в `test_filter_projection_rows_contract.py`
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — `_matches_post_fetch_filters` или pre-canonicalize before type compare

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_filter_projection_rows_contract.py -q -k type
```
