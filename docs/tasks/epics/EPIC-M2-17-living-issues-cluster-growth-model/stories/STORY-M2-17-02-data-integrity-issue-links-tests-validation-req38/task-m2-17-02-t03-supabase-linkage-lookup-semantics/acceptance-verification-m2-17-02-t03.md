# Acceptance verification — TASK-M2-17-02-T03

- **Task:** Supabase/SQLite linkage lookup semantics (Variant A)
- **Result:** PASS
- **Evidence:** `db_sqlite.py` JOIN/subquery on `issue_story_links`; `db_supabase.py` resolves via `issue_story_links` then `issue_candidates`; `ClusterMembershipStore.save_membership` unchanged
- **Commands:** `python3 -m pytest tests/test_process_linkage_sqlite.py tests/test_living_issues_extend_existing.py -q`
