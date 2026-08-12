# task-gw-rc-02-t05

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000031
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Acceptance-тесты: seed payload с `type:"improvement"` → ответ `IMPROVEMENT`; список и одиночный endpoint; memory + sqlite + HTTP. Покрыть unknown/empty type (AC-3).

## Code Facts
- Прецедент GW-RC-01 acceptance — [`test_gw_rc_01_read_path_column_merge.py`](../../../../../../../tests/test_gw_rc_01_read_path_column_merge.py)
- REQ-24 read API — [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py)

## Acceptance / DoD
- Traces parent AC-1: list + `/{id}` → `type: IMPROVEMENT` для legacy lowercase seed
- Traces parent AC-2: HTTP `?type=IMPROVEMENT` с lowercase payload
- Traces parent AC-3: unknown type → `IMPROVEMENT` + anomaly log test (if T03 done)
- Parametrize `memory` + `sqlite` stores; HTTP E2E via TestClient
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_rc_02_type_canonical_on_read.py` (новый)
- Touch `tests/test_filter_projection_rows_contract.py` при необходимости

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_02_type_canonical_on_read.py -q
```
