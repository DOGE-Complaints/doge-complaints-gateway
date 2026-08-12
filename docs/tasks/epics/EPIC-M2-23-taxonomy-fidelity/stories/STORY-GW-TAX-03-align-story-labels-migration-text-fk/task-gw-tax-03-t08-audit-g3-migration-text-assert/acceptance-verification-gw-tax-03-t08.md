# Acceptance verification — GW-TAX-03 T08 (audit G3)

**Task:** `task-gw-tax-03-t08-audit-g3-migration-text-assert`  
**Status:** 🟢 Done  
**Scaffolded:** 2026-08-07T10:21:47Z  
**Date:** 2026-08-07T10:30:10Z

## Checks
- [x] Unit test asserts migration `story_id text` / no UUID DDL
- [x] pytest green offline (1 passed)
- [x] Verification commands from README green

## Evidence
- Test: `tests/test_gw_tax_03_migration_story_labels_text_fk.py`
- `pytest -q tests/test_gw_tax_03_migration_story_labels_text_fk.py -m "not live_integration"` → **1 passed**
- `rg 'story_id UUID'` on migration → no match; `story_id text` at `:11`
