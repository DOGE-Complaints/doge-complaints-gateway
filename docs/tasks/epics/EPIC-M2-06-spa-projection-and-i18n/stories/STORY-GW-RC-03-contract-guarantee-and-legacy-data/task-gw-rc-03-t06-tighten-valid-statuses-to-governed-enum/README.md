# task-gw-rc-03-t06

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** — (audit override, вне pkg-000032)
- **Skill declared:** python-pro
- **Depends on:** T01–T05
- **Wave:** audit override (`run_mode=gw_rc_03_audit_followup`)
- **Decision Ref:** [`audit-gw-rc-03-contract-guarantee-legacy-data-2026-06-19.md`](../../../../../../analysis/audit-gw-rc-03-contract-guarantee-legacy-data-2026-06-19.md) §3 G1

## Purpose
Закрыть audit G1: контракт-тест допускает `status ∈ {NEW, IN_REVIEW, PUBLISHED, DRAFT, ARCHIVED}`, тогда как governed-enum `DOGEIssueStatus` содержит только `{NEW, IN_REVIEW, PUBLISHED}`. Сузить `_VALID_STATUSES` до фактического enum для строгого guard.

## Code Facts
- Тестовый набор статусов шире enum — [`test_gw_rc_03_contract_guarantee.py:20`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py#L20): `_VALID_STATUSES = frozenset({"NEW", "IN_REVIEW", "PUBLISHED", "DRAFT", "ARCHIVED"})`
- Governed enum — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11): `DOGEIssueStatus` = `NEW`, `IN_REVIEW`, `PUBLISHED`
- Проверка статуса в тесте — [`test_gw_rc_03_contract_guarantee.py:62-63`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py#L62-L63): `assert issue["status"] in _VALID_STATUSES`
- Seed использует `PUBLISHED` — остаётся валидным после сужения

## Acceptance / DoD
- (P0) `_VALID_STATUSES` = `{s.value for s in DOGEIssueStatus}` (import из `core.projection.enums`)
- (P0) Существующие 3 теста в `test_gw_rc_03_contract_guarantee.py` проходят без изменения логики seed/assert
- (P1) Unit suite без регрессий
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `tests/test_gw_rc_03_contract_guarantee.py` — import `DOGEIssueStatus`, заменить `_VALID_STATUSES`

## Out of scope
- Новый pkg / смена [`gateway-active-package.current.yaml`](../../../../../../gateway-active-package.current.yaml)
- Prod-код (`src/`)
- Doc R1/R2 (backlog status, pkg filename date)
- G2 legacy data defer (T02 decision)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_03_contract_guarantee.py -q
cd doge-complaints-gateway && python3 -m pytest --ignore=tests/integration --ignore=tests/smoke -q
```
