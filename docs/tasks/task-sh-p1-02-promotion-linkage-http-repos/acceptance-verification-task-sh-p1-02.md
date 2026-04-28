# Acceptance verification — TASK-SH-P1-02

## Checklist
- [ ] Promotion/linkage repositories в supabase режиме используют HTTP adapter.
- [ ] Issue-story linkage сохраняется детерминированно.
- [ ] Regression для story-first pipeline проходит.

## Verification commands
- `python3 -m pytest tests -k "issue_candidate or review_audit or issue_story_links or cluster_issue_pipeline" -q`
