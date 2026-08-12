# task-gw-rc-07-t04

## Meta
- **Story:** [STORY-GW-RC-07](../STORY-GW-RC-07-hosted-tallinn-issues-internal-error.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000047
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Исправить root cause CF-B: code fix in `src/core/` and/or hosted data repair — scope определяется по T03 findings.

## Code Facts
- Read path — [`read_filters.py`](../../../../../../../src/core/projection/read_filters.py), [`handlers.py:368`](../../../../../../../src/core/api/handlers.py)
- T03 probe — [`../task-gw-rc-07-t03-per-row-read-probe-seven-incident-issues/per-row-read-probe.md`](../task-gw-rc-07-t03-per-row-read-probe-seven-incident-issues/per-row-read-probe.md) (after P3)
- Regression surface — [`test_req24_tallinn_issues_read_api.py`](../../../../../../../tests/test_req24_tallinn_issues_read_api.py), [`test_gw_rc_03_contract_guarantee.py`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py) (if applicable)

## Acceptance / DoD
- Traces parent AC #2 (fix leg): Root cause исправлен (T04)
- `pytest` relevant read-path tests green locally
- Deploy/redeploy hosted if code fix
- Artifact [`fix-summary.md`](./fix-summary.md) documents change + evidence
- BULLRUN phases complete
- [`acceptance-verification-gw-rc-07-t04.md`](./acceptance-verification-gw-rc-07-t04.md) signed

## Where to change
- `src/core/` (if code fix) **or** hosted data ops (if data repair) — per T03
- Task artifact: `fix-summary.md`
- Optional: new/extended test in `tests/`

## Out of scope
- SEED-03 E2E runbook
- Changing clustering thresholds

## Verification commands
```bash
cd doge-complaints-gateway
python3 -m pytest -q tests/test_req24_tallinn_issues_read_api.py
python3 -m pytest -q tests/ -k "tallinn or projection or read"
```
