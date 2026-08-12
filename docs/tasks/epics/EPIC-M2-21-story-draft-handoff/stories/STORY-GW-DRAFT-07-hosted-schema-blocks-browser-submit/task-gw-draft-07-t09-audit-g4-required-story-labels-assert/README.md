# task-gw-draft-07-t09-audit-g4-required-story-labels-assert

## Meta
- **Story:** [STORY-GW-DRAFT-07](../STORY-GW-DRAFT-07-hosted-schema-blocks-browser-submit.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000057
- **Skill declared:** python-pro
- **Wave:** audit follow-up GW-DRAFT-07
- **Depends on:** T01–T06 Done
- **Audit ref:** [`audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md`](../../../../../../analysis/audit-gw-draft-07-hosted-schema-blocks-browser-submit-2026-08-07.md) **G4**

## Purpose
Добавить точечный unit assert: `story_labels ∈ REQUIRED_READINESS_TABLES` — защита от рецидива «убрать таблицу из REQUIRED» без hosted DDL.

## Code Facts
- Set — [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py) includes `story_labels`
- Probe — [`db_supabase.py:293-303`](../../../../../../../../src/core/infrastructure/db_supabase.py) `required_tables_ready`
- No existing assert (audit G4 grep claim)

## Acceptance / DoD
- [x] Unit test asserts `"story_labels" in REQUIRED_READINESS_TABLES` (or equivalent frozenset membership)
- [x] Test file under `doge-complaints-gateway/tests/` named clearly (`test_gw_draft_07_*` or extend readiness suite)
- [x] `pytest` for that file green offline
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-draft-07-t09.md`](./acceptance-verification-gw-draft-07-t09.md) signed (Date post P6 verify only)

## Where to change
- `doge-complaints-gateway/tests/` (new or existing readiness unit test)
- Import from `core.infrastructure.db_supabase` — **no** change to REQUIRED set itself

## Out of scope
- Changing `REQUIRED_READINESS_TABLES` membership
- Hosted DDL; SPA; TAX-03 migration file

## Verification commands
```bash
cd doge-complaints-gateway && python3 -m pytest -q tests/test_gw_draft_07_required_story_labels.py -m "not live_integration"
# or path chosen in implementation
rg 'story_labels' src/core/infrastructure/db_supabase.py
```
