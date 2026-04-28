## Task: implement — Promotion and linkage repositories via Supabase HTTP

Key: TASK-SH-P1-02  
Priority: P1  
Status: Todo  
Closes: SH-REPO-HTTP-03  
Supersedes: TASK-DB-SUPABASE-REPOS-02  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Мигрировать `issue_candidates`, `review_audit_log`, `issue_story_links` на HTTP-репозитории Supabase.

### AC/DoD
- [ ] Promotion candidate store работает через HTTP.
- [ ] Review audit log store работает через HTTP.
- [ ] Issue-story linkage store работает через HTTP.
- [ ] Story-first pipeline e2e не теряет linkage/provenance.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "issue_candidate or review_audit or issue_story_links" -q
```
