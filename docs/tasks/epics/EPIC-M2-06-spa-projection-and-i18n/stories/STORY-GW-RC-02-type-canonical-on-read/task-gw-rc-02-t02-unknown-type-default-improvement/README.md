# task-gw-rc-02-t02

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Решить кейс неизвестного `type` (не в enum) и пустого/missing `type`: дефолт **`IMPROVEMENT`** в ответе API (Product decision P1).

## Code Facts
- `validate_governed_enums` на write-path отклоняет unknown — [`validation.py:14-18`](../../../../../../../src/core/projection/validation.py#L14-L18); read-path должен быть устойчивым (D-RC-3)
- T01 helper — choke-point для политики unknown/empty

## Acceptance / DoD
- Traces parent AC: поведение неизвестного `type` определено и покрыто тестом
- `type` not in `DOGEIssueType` → `IMPROVEMENT` в merged output
- Missing/empty `type` → `IMPROVEMENT`
- Unit tests для edge cases (unknown string, `""`, absent key)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — логика в `canonicalize_issue_type_on_read()` (T01)
- `tests/test_filter_projection_rows_contract.py` или dedicated unit tests

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_filter_projection_rows_contract.py -q -k canonical
```
