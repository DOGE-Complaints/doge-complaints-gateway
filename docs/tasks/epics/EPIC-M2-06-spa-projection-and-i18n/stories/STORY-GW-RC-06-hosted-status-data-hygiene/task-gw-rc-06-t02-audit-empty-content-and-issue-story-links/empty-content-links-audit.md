# Empty content + issue_story_links audit — GW-RC-06 T02

**Date:** 2026-06-20  
**Source:** hosted Supabase REST (post-T01 status migration)

## Per-row audit

| issue_id | empty title_json & summary_json | link count | recoverable (reproject) |
|----------|--------------------------------|------------|-------------------------|
| test-7ef193be-dc51-4ddb-a582-24a6977dfd51 | **N** (title en/et/ru populated) | 0 | N/A — content already present |
| test-5e350194-30dc-4ad6-b3d6-b68c3c66bfb3 | **Y** | 0 | **N** |
| test-bdcae6aa-1663-41ca-871b-2b4cdd43f9dc | **Y** | 0 | **N** |
| test-9bc69528-123b-4f00-a7ea-333a7791ffe3 | **Y** | 0 | **N** |
| test-2f10a3c8-5269-40ba-a917-025f4d5f2e60 | **Y** | 0 | **N** |

## Summary

- **Total hosted rows (pre-T03 delete):** 5
- **Empty content:** 4/5
- **Total `issue_story_links` on hosted:** 0
- **Recoverable via `reproject_issue_i18n.py`:** 0

## Conclusion

Reproject cannot restore empty content — no story links exist. T03 disposition required for 4 empty integration test-seed rows.
