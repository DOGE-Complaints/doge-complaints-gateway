# Acceptance verification — task-gw-public-01-t02-get-tallinn-issue-by-id-without-auth-not-401

- **Task:** T02 GET /tallinn/issues/{id} without auth → 200/404, not 401/403
- **Status:** PASS
- **Date:** 2026-07-10

## Checklist

- [x] GET by id without headers: 200 or 404
- [x] Never 401 or 403
- [x] pytest PASS offline
