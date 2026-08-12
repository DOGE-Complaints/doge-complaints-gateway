# task-gw-draft-05-t05-runtime-openapi-stash-schema

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** docs
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T01–T02

## Purpose
Backlog T05: add `StoryDraftStashRequest` schema to runtime OpenAPI; point `POST /story-drafts` request and GET response `$ref` to stash schema (lockstep GPT Actions v0.6.0).

## Code Facts
- Runtime drift — [`openapi.yaml:674-693`](../../../../../../../runtime-docs/api-reference/openapi.yaml) `POST /story-drafts` → `StoryIntakeRequest`
- GPT SSOT stash schema — [`GPT UI/docs/custom-gpt-story-intake-actions.openapi.yaml`](../../../../../../../../../GPT%20UI/docs/custom-gpt-story-intake-actions.openapi.yaml)
- Implemented handler — [`handlers.py:523`](../../../../../../../../src/core/api/handlers.py) `handle_story_draft_create`

## Acceptance / DoD
- [ ] Traces parent AC #5: runtime OpenAPI describes stash contract without required submitter
- [ ] `components/schemas/StoryDraftStashRequest` added; `/story-drafts` POST body + GET response use stash schema
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t05.md`](./acceptance-verification-gw-draft-05-t05.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml`

## Out of scope
- Narrative runtime docs (T06); GPT UI OpenAPI edits; prod code (T01–T02)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'StoryDraftStashRequest' docs/runtime-docs/api-reference/openapi.yaml
cd doge-complaints-gateway && rg '/story-drafts' docs/runtime-docs/api-reference/openapi.yaml -A5 | head -40
```
