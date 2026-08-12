# Acceptance verification — task-gw-draft-06-t08-audit-g2-stale-intake-comment-cleanup

- **Task:** T08 audit G2 stale intake comment cleanup
- **Status:** PASS
- **Date:** 2026-07-11

## Checklist

- [x] `rg '"/intake/stories"|POST /intake/stories' tests/integration/supabase/test_supabase_dotenv_connectivity.py` = 0
- [x] Comment describes stash-only / in_memory semantics (no legacy route)
- [x] Audit G2 traceability ([`audit-gw-draft-06-...`](../../../../../../analysis/audit-gw-draft-06-remove-legacy-intake-stories-route-2026-07-11.md) §G2)

## Live verification

```bash
cd doge-complaints-gateway && rg '"/intake/stories"|POST /intake/stories' tests/integration/supabase/test_supabase_dotenv_connectivity.py || test $? -eq 1
```

→ 0 matches
