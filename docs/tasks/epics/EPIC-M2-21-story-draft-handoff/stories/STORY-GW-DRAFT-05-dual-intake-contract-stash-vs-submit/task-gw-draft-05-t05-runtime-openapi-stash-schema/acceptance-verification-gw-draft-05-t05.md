# Acceptance verification — task-gw-draft-05-t05-runtime-openapi-stash-schema

- **Task:** T05 runtime OpenAPI stash schema
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] `StoryDraftStashRequest` schema in runtime OpenAPI
- [x] `POST /story-drafts` requestBody refs `StoryDraftStashRequest` (not `StoryIntakeRequest`)
- [x] GET draft envelope data refs `StoryDraftStashRequest`

## Evidence

```
cd doge-complaints-gateway && rg 'StoryDraftStashRequest' docs/runtime-docs/api-reference/openapi.yaml → 4 matches
cd doge-complaints-gateway && rg 'postStoryDraft' -A20 docs/runtime-docs/api-reference/openapi.yaml | rg StoryDraftStashRequest → ok
```
