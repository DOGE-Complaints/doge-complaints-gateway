# task-gw-rc-03-t01

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000032
- **Skill declared:** python-pro
- **Depends on:** GW-RC-01, GW-RC-02 (merged read path + type canon)

## Purpose
Контракт-тест неполного payload → валидный ответ (list + get; все бэкенды). Зеркалит D-RC-4: seed `issue_id`+`status` + payload без id/status и со строчным type → GET возвращает `id`, `status ∈ {…}`, `type` в каноне.

## Code Facts
- Intake seed pattern — [`test_req24_tallinn_issues_read_api.py:159-167`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py#L159-L167)
- Incomplete payload id/status (RC-01) — [`test_gw_rc_01_read_path_column_merge.py`](../../../../../../../tests/test_gw_rc_01_read_path_column_merge.py)
- Column merge + type canon — [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py) (`merge_projection_columns`, `canonicalize_issue_type_on_read`)
- Handlers — [`handlers.py`](../../../../../../../src/core/api/handlers.py), [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py)

## Acceptance / DoD
- Traces parent AC: неполный payload → ответ содержит `id`, `status`, канон `type`
- List + get endpoints covered
- Supabase / SQLite / InMemory (parametrize or separate cases)
- Full unit suite без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_rc_03_contract_guarantee.py` (новый)

## Out of scope
- Legacy SQL audit (T02)
- FE `assertIssue` (T04 handoff)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
