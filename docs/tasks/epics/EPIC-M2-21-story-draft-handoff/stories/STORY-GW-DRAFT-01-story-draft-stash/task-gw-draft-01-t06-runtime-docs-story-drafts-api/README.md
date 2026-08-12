# task-gw-draft-01-t06-runtime-docs-story-drafts-api

## Meta
- **Story:** [STORY-GW-DRAFT-01](../STORY-GW-DRAFT-01-story-draft-stash.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000043
- **Skill declared:** python-pro
- **Depends on:** T03, T04

## Purpose
Runtime-docs дельта: openapi paths `/story-drafts`, API_REFERENCE section, story-persistence-model draft-store + TTL.

## Code Facts
- OpenAPI intake pattern — [`runtime-docs/api-reference/openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- API_REFERENCE — [`runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- Persistence model — [`runtime-docs/story-persistence-model.md`](../../../../../../../runtime-docs/story-persistence-model.md)

## Acceptance / DoD
- OpenAPI POST/GET `/story-drafts` documented
- API_REFERENCE stash section added
- story-persistence-model draft-store + TTL documented
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- [`docs/runtime-docs/api-reference/openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- [`docs/runtime-docs/api-reference/API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- [`docs/runtime-docs/story-persistence-model.md`](../../../../../../../runtime-docs/story-persistence-model.md)

## Out of scope
GPT/SPA cross-repo docs

## Verification commands
```bash
cd doge-complaints-gateway && rg '/story-drafts' docs/runtime-docs/
```
