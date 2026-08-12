# task-gw-draft-03-t02-gateway-runtime-docs-browser-submit-as-built

## Meta
- **Story:** [STORY-GW-DRAFT-03](../STORY-GW-DRAFT-03-supersede-gpt-submit-authz-canon.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000045
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
D-DRAFT-5 **C:** зафиксировать browser-submit handoff как as-built в gateway runtime-docs (`architecture-and-layers-as-is.md` + кросс-ссылки api-reference).

## Code Facts
- Routes live — [`asgi_app.py`](../../../../../../../src/core/api/asgi_app.py): `POST /story-drafts`, `GET /story-drafts/{id}`, `POST /story-drafts/{id}/submit`
- API docs already have submit — [`API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) §6.8
- Architecture **устарел** — [`architecture-and-layers-as-is.md`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md) L39–50: только `POST /intake/stories`, нет `/story-drafts*`
- Draft persistence — [`story-persistence-model.md`](../../../../../../../docs/runtime-docs/story-persistence-model.md) §draft store

## Acceptance / DoD
- Traces parent AC#3: gateway runtime-docs отражают browser-submit as-built
- `architecture-and-layers-as-is.md`: таблица routes + mermaid handoff flow (GPT stash → browser GET/submit)
- Кросс-ссылка из architecture → API_REFERENCE §6.8
- Опционально: pointer в `story-persistence-model.md` §draft на browser-submit path
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`docs/runtime-docs/architecture-and-layers-as-is.md`](../../../../../../../docs/runtime-docs/architecture-and-layers-as-is.md)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../docs/runtime-docs/api-reference/API_REFERENCE.md) (cross-link only, если нужен back-link)
- [`docs/runtime-docs/story-persistence-model.md`](../../../../../../../docs/runtime-docs/story-persistence-model.md) (optional)

## Out of scope
- Identity canon docs; gpt-submit-authz INDEX (T01)
- Gateway pointer на identity рассинхрон (T03)

## Verification commands
```bash
rg 'story-drafts|browser.submit|handoff' doge-complaints-gateway/docs/runtime-docs/architecture-and-layers-as-is.md
```
