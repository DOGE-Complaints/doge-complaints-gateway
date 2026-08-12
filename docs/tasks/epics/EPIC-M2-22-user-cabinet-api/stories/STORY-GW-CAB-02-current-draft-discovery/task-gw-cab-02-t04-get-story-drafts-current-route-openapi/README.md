# task-gw-cab-02-t04-get-story-drafts-current-route-openapi

## Meta
- **Story:** [STORY-GW-CAB-02](../STORY-GW-CAB-02-current-draft-discovery.md)
- **Type:** implement
- **Status:** 🟢 Done
- **Package:** pkg-000053
- **Skill declared:** python-pro
- **Depends on:** T03

## Purpose
Новый эндпоинт `GET /story-drafts/current`: route + `handle_story_draft_current` + DTO `{draft_id, last_edited_at}` / `{data: null}`; OpenAPI (backlog D.7–D.8).

## Code Facts
- Reuse `_STORY_DRAFT_READ_DEPS` (browser Bearer→`/me`) — [`asgi_app.py:302-357`](../../../../../../../../src/core/api/asgi_app.py#L302)
- SPA contract `GET /story-drafts/current` — [`STORY-SPA-CAB-api-requirements.md:19`](../../../../../../../../spa-app/docs/tasks/backlog-stories/cabinet/STORY-SPA-CAB-api-requirements.md)
- OpenAPI — [`openapi.yaml`](../../../../../../runtime-docs/api-reference/openapi.yaml)
- Нет `GET /story-drafts/current` в коде — grep по `src/` отсутствует

## Acceptance / DoD
- [x] Traces parent AC-1: `GET /story-drafts/current` under browser Bearer
- [x] Traces parent AC-5: `last_edited_at` = `updated_at.isoformat()`
- [x] Scope trace: backlog §D.7–D.8
- [x] OpenAPI describes `/story-drafts/current` (+ nullable data)
- [x] BULLRUN phases complete
- [x] [`acceptance-verification-gw-cab-02-t04.md`](./acceptance-verification-gw-cab-02-t04.md) signed

## Where to change
- [`src/core/api/handlers.py`](../../../../../../../../src/core/api/handlers.py) — `handle_story_draft_current`
- [`src/core/api/asgi_app.py`](../../../../../../../../src/core/api/asgi_app.py) — route `/story-drafts/current`
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../runtime-docs/api-reference/openapi.yaml)

## Out of scope
- Contract/integration tests (T05)
- Story gate (T06)

## Verification commands
```bash
rg '/story-drafts/current' doge-complaints-gateway/src doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml
```
