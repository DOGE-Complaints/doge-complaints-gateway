# Acceptance verification — task-gw-draft-06-t02-runtime-docs-remove-public-intake-path

- **Task:** T02 runtime docs remove public intake path
- **Status:** PASS
- **Date:** 2026-07-11T10:15:42Z

## Checklist

- [x] OpenAPI: no `/intake/stories` path
- [x] API_REFERENCE + security-env: GPT write via `/story-drafts`
- [x] Architecture + persistence docs aligned

## Evidence

```
cd doge-complaints-gateway && rg 'POST /intake/stories|/intake/stories' docs/runtime-docs/api-reference/openapi.yaml || test $? -eq 1 → ok
cd doge-complaints-gateway && rg '/intake/stories' docs/runtime-docs/api-reference/API_REFERENCE.md docs/runtime-docs/security-env-api-access.md docs/runtime-docs/architecture-and-layers-as-is.md docs/runtime-docs/story-persistence-model.md || test $? -eq 1 → ok (GW-DRAFT-06 removal notes only in §6 header)
```
