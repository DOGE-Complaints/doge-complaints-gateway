## Task: implement — Projection and embeddings repositories via Supabase HTTP

Key: TASK-SH-P1-01  
Priority: P1  
Status: Todo  
Closes: SH-REPO-HTTP-02  
Supersedes: TASK-DB-SUPABASE-REPOS-02  
Decision Ref: `docs/analysis/story-first-supabase-verification-report.md`

### Goal
Перевести `spa_issue_projections`, `story_embeddings`, `spa_issue_projection_embeddings` на HTTP client.

### AC/DoD
- [ ] Projection store работает через HTTP.
- [ ] Story embedding store работает через HTTP.
- [ ] Issue projection embedding store работает через HTTP.
- [ ] Контракты policy/source checksum не деградировали.

### Verification commands
```bash
cd /Users/eslinko/Development/DOGEstonia/doge-complaints-gateway
python3 -m pytest tests -k "projection and embedding and supabase" -q
rg -n "spa_issue_projections|story_embeddings|spa_issue_projection_embeddings" src/core/infrastructure
```
