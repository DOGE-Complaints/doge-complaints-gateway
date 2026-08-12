# task-gw-rc-05-t01

## Meta
- **Story:** [STORY-GW-RC-05](../STORY-GW-RC-05-status-vocabulary-canonicalization.md)
- **Type:** fix
- **Status:** 🟢 Done
- **Package:** pkg-000034
- **Skill declared:** python-pro

## Purpose
Write-fix: extend-path (+ ревизия всех save_projection вызовов в application layer) использует projection board-status, не candidate `*.status.value`.

## Code Facts
- Extend-path BUG — [`issue_create.py:332-334`](../../../../../../../src/core/application/issue_create.py#L332-L334) `status=updated.status.value` → `promoted`
- Create-path OK — [`issue_create.py:250-252`](../../../../../../../src/core/application/issue_create.py#L250-L252) `status=str(projection_payload.get("status", projection.status))`
- Manual create path OK — [`issue_create.py:394-396`](../../../../../../../src/core/application/issue_create.py#L394-L396) `status=projection.status`
- Board enum — [`enums.py:6-11`](../../../../../../../src/core/projection/enums.py#L6-L11) `DOGEIssueStatus`
- Candidate enum — [`promotion/types.py:8-13`](../../../../../../../src/core/promotion/types.py#L8-L13) `IssueCandidateStatus.promoted`

## Acceptance / DoD
- Traces parent AC: после write-fix реальный create→extend кладёт в `doge_issues.status` board-vocab (PUBLISHED), не `promoted`
- Extend `save_projection` uses projection board-status (same pattern as create-path :252)
- Grep audit: all `save_projection` in `src/core/application/` write projection status, not candidate
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- [`src/core/application/issue_create.py`](../../../../../../../src/core/application/issue_create.py) — extend block `_extend_issue` save_projection call
- Audit `save_projection` in `src/core/application/` (no other candidate-status writes expected)

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest tests/test_gw_rc_05_status_vocabulary_contract.py -q -k extend 2>/dev/null || python3 -m pytest tests/ -q -k issue_create --ignore=tests/integration --ignore=tests/smoke
```
