# task-gw-rc-04-t08

## Meta
- **Story:** [STORY-GW-RC-04](../STORY-GW-RC-04-columnar-model-migration.md)
- **Type:** tests
- **Status:** 🔵 Done
- **Package:** pkg-000033
- **Skill declared:** python-pro
- **Depends on:** T03–T07

## Purpose
Контракт-тесты: внешняя форма issue идентична до/после; update `reproject_issue_i18n.py` for columnar storage.

## Code Facts
- Contract guarantee — [`test_gw_rc_03_contract_guarantee.py`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py)
- Store contract — [`test_supabase_issue_projection_store_contract.py`](../../../../../../../tests/test_supabase_issue_projection_store_contract.py)
- Backfill script — [`scripts/reproject_issue_i18n.py`](../../../../../../../scripts/reproject_issue_i18n.py)

## Acceptance / DoD
- Traces parent AC#2: contract tests green; API shape unchanged
- Traces D-RC-5: reproject script writes columnar model
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_supabase_issue_projection_store_contract.py`
- `tests/test_db_backed_pipeline_e2e.py`
- `scripts/reproject_issue_i18n.py`
- Add/update GW-RC-04 regression tests as needed

## Out of scope
- Story gate (T09)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py tests/test_supabase_issue_projection_store_contract.py tests/test_db_backed_pipeline_e2e.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
