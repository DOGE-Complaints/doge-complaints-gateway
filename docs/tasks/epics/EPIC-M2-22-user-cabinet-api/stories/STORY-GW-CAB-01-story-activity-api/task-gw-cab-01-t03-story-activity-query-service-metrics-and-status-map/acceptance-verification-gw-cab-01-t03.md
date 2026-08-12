# Acceptance — TASK-GW-CAB-01-T03

- **Result:** PASS
- **Date:** 2026-07-13T09:59:00Z

| AC (parent) | Status | Evidence |
|-------------|--------|----------|
| MVP `data.metrics` + `data.stories[]` shape | PASS | `story_activity.py` `build_activity` return dict |
| Row status `published` \| `under_review` only | PASS | `map_issue_status_to_cabinet` |
| Metrics per D-CAB01-3 | PASS | submitted/published/under_review counts in service |
| No issue link → under_review | PASS | D-CAB01-1; T05 metrics test |
