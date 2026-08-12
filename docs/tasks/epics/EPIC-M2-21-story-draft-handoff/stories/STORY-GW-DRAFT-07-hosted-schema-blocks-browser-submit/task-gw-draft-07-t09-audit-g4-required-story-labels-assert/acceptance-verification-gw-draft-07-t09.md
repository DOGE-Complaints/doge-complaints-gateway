# Acceptance verification — GW-DRAFT-07 T09

- **Task:** task-gw-draft-07-t09-audit-g4-required-story-labels-assert
- **Result:** PASS
- **Date:** 2026-08-07T09:19:57Z

## Evidence

- New unit: [`tests/test_gw_draft_07_required_story_labels.py`](../../../../../../../../tests/test_gw_draft_07_required_story_labels.py)
- Assert: `"story_labels" in REQUIRED_READINESS_TABLES`
- Source set: [`db_supabase.py:29-43`](../../../../../../../../src/core/infrastructure/db_supabase.py) (membership unchanged)
- Command: `python3 -m pytest -q tests/test_gw_draft_07_required_story_labels.py -m "not live_integration"` → **1 passed**
