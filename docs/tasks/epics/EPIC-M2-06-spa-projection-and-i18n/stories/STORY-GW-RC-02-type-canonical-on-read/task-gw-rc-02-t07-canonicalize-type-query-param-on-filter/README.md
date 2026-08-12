# task-gw-rc-02-t07

## Meta
- **Story:** [STORY-GW-RC-02](../STORY-GW-RC-02-type-canonical-on-read.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** — (audit override, вне pkg-000031)
- **Skill declared:** python-pro
- **Depends on:** T01–T06
- **Wave:** audit override (`run_mode=gw_rc_02_audit_followup`)
- **Decision Ref:** [`audit-gw-rc-02-type-canonical-on-read-2026-06-19.md`](../../../../../../analysis/audit-gw-rc-02-type-canonical-on-read-2026-06-19.md) §3 G1

## Purpose
Закрыть audit G1: фильтр `?type=` должен принимать legacy lowercase query так же, как payload. Сейчас канонизируется только `payload.get("type")`, а `issue_type` из query сравнивается как есть.

## Code Facts
- Payload-side канонизация в фильтре — [`read_filters.py:191-197`](../../../../../../../src/core/projection/read_filters.py#L191-L197)
- Query `type` передаётся без нормализации — [`asgi_app.py:347`](../../../../../../../src/core/api/asgi_app.py#L347) → [`handlers.py:345`](../../../../../../../src/core/api/handlers.py#L345) → `filter_projection_rows`
- При `?type=improvement` и payload `type:"improvement"` сравнение `"IMPROVEMENT" != "improvement"` → no match (audit G1)

## Acceptance / DoD
- (P0) Входной `issue_type` канонизируется тем же `canonicalize_issue_type_on_read(..., log_unknown=False)` до сравнения
- (P0) Unit: `filter_projection_rows(..., issue_type="improvement")` матчит row с legacy lowercase payload
- (P0) HTTP: `GET /tallinn/issues?type=improvement` возвращает issue с `type:"improvement"` в payload
- (P1) Существующие GW-RC-02 тесты без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `src/core/projection/read_filters.py` — `filter_projection_rows` и/или `_matches_post_fetch_filters`
- `tests/test_gw_rc_02_type_canonical_on_read.py` — HTTP query lowercase
- `tests/test_filter_projection_rows_contract.py` — unit query-side case

## Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- FE i18n проверка (G2)
- Doc R1/R2 (backlog status, pkg filename date)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_02_type_canonical_on_read.py tests/test_filter_projection_rows_contract.py -q -k type
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
