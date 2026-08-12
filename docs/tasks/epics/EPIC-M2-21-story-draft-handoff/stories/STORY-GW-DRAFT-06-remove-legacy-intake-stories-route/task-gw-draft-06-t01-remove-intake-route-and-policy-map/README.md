# task-gw-draft-06-t01-remove-intake-route-and-policy-map

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** implement
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** GW-DRAFT-05 Done

## Purpose
Backlog T01: change-propagation — remove public `POST /intake/stories` route and policy map entries; confirm `handle_story_intake` has no public HTTP callers left in `asgi_app.py`.

## Code Facts
- Legacy route — [`asgi_app.py:501`](../../../../../../../../src/core/api/asgi_app.py) `@app.post("/intake/stories")`
- PUBLIC_ROUTES — [`asgi_app.py:62`](../../../../../../../../src/core/api/asgi_app.py) includes `"/intake/stories"`
- Internal submit caller — [`handlers.py:688`](../../../../../../../../src/core/api/handlers.py) `handle_story_draft_submit` → `handle_story_intake`
- Config comment — [`schema.py:126`](../../../../../../../../src/core/config/schema.py) mentions `POST /intake/stories`

## Acceptance / DoD
- [ ] Traces parent AC #1: `rg 'POST /intake/stories|"/intake/stories"' src/` = 0
- [ ] Traces parent AC #3: `handle_story_intake` not wired from removed route (only submit-bridge in handlers)
- [ ] `PUBLIC_ROUTES` / route policy no longer lists `/intake/stories`
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-06-t01.md`](./acceptance-verification-gw-draft-06-t01.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/src/core/api/asgi_app.py`
- `doge-complaints-gateway/src/core/config/schema.py` (comment only)

## Out of scope
- Runtime docs (T02); runner (T03); tests (T04–T05)
- Removing `StoryIntakeRequest` / `handle_story_intake` domain logic
- `POST /tallinn/issues`

## Verification commands
```bash
cd doge-complaints-gateway && rg 'POST /intake/stories|"/intake/stories"' src/ || test $? -eq 1
cd doge-complaints-gateway && rg 'handle_story_intake' src/core/api/asgi_app.py || test $? -eq 1
cd doge-complaints-gateway && rg 'handle_story_intake' src/core/api/handlers.py
```
