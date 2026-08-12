# task-gw-rc-03-t04

## Meta
- **Story:** [STORY-GW-RC-03](../STORY-GW-RC-03-contract-guarantee-and-legacy-data.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000032
- **Skill declared:** python-pro
- **Depends on:** T01 (contract tests exist)

## Purpose
Backend handoff: зафиксировать для фронта, что форма ответа гарантирована на бэке; FE может включить `assertIssue`/контракт-тест.

## Code Facts
- FE path без `assertIssue` — [`interview-issues-read-contract-2026-06-19.md`](../../../../../../backlog-stories/issues-read-contract/interview-issues-read-contract-2026-06-19.md) §1
- Issues read API — [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md)
- Contract tests — `tests/test_gw_rc_03_contract_guarantee.py` (T01)

## Acceptance / DoD
- Handoff doc in task folder (`handoff-fe-contract-guarantee.md`) or minimal API_REFERENCE touch
- States: backend guarantees `id`, `status`, canonical `type` on read for incomplete legacy payload
- FE `assertIssue` explicitly out of scope (SPA team)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `handoff-fe-contract-guarantee.md` (task folder)
- Optional minimal note in `docs/runtime-docs/api-reference/API_REFERENCE.md`

## Out of scope
- SPA code / `assertIssue` implementation
- Runtime code changes

## Verification commands
```bash
# Doc review only — no pytest required for scaffold
```
