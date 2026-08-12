# Acceptance verification — task-gw-draft-06-t01-remove-intake-route-and-policy-map

- **Task:** T01 remove intake route and policy map
- **Status:** PASS
- **Date:** 2026-07-11T10:15:42Z

## Checklist

- [x] `PUBLIC_ROUTES` no `/intake/stories`
- [x] `rg 'POST /intake/stories|"/intake/stories"' src/` = 0
- [x] `handle_story_intake` not wired in `asgi_app.py`

## Evidence

```
cd doge-complaints-gateway && rg 'POST /intake/stories|"/intake/stories"' src/ || test $? -eq 1 → ok
cd doge-complaints-gateway && rg 'handle_story_intake' src/core/api/asgi_app.py || test $? -eq 1 → ok
cd doge-complaints-gateway && rg 'handle_story_intake' src/core/api/handlers.py → submit-bridge only
```
