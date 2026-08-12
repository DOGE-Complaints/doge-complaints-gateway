# task-gw-rc-05-t04

## Meta
- **Story:** [STORY-GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000034
- **Skill declared:** python-pro
- **Depends on:** T01, T02

## Purpose
Контракт-тест на реальном выводе пайплайна: прогнать create→extend, assert `status ∈ board`; и тест канонизации legacy `promoted`→`PUBLISHED`.

## Code Facts
- D-RC05-4 — [`interview-rc05-rc06-status-vocabulary-2026-06-20.md`](../../../../../../backlog-stories/issues-read-contract/interview-rc05-rc06-status-vocabulary-2026-06-20.md) — contract test on **real** pipeline output, not happy-seed
- RC-03 gap — [`test_gw_rc_03_contract_guarantee.py`](../../../../../../../tests/test_gw_rc_03_contract_guarantee.py) seeded `PUBLISHED` directly, missed extend-path bug
- Extend-path write — [`issue_create.py:276-337`](../../../../../../../src/core/application/issue_create.py#L276-L337) `_extend_issue`
- Board vocab — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11)

## Acceptance / DoD
- Traces parent AC: после write-fix create→extend → `doge_issues.status` board-vocab (PUBLISHED)
- Traces parent AC: контракт-тест гоняет **реальный** пайплайн (не happy-seed) и ловит невалидный status
- Unit test `tests/test_gw_rc_05_status_vocabulary_contract.py` covers create→extend via IssueCreateService + in-memory projection store
- Legacy read canon: row with `promoted` in store → API output `PUBLISHED`
- Assert `status ∈ {NEW, IN_REVIEW, PUBLISHED}` on all projection outputs
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- New [`tests/test_gw_rc_05_status_vocabulary_contract.py`](../../../../../../../tests/test_gw_rc_05_status_vocabulary_contract.py)
- Optional: extend live pipeline test after T03 changes

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_05_status_vocabulary_contract.py -q
```
