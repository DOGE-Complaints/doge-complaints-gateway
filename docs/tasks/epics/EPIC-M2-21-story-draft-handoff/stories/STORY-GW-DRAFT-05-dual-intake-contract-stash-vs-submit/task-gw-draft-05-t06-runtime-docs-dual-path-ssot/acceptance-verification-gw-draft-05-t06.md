# Acceptance verification — task-gw-draft-05-t06-runtime-docs-dual-path-ssot

- **Task:** T06 runtime docs dual-path SSOT
- **Status:** PASS
- **Date:** 2026-07-11T07:52:43Z

## Checklist

- [x] security + architecture describe two request contracts (stash vs intake bridge)
- [x] API_REFERENCE §6.8, architecture §4.1, story-persistence-model updated for stash shape without submitter

## Evidence

```
cd doge-complaints-gateway && rg 'StoryDraftStashRequest|stash vs|без submitter' docs/runtime-docs/ → matches in API_REFERENCE, architecture, security, persistence
cd doge-complaints-gateway && rg 'всегда требует submitter' docs/runtime-docs/security-env-api-access.md || test $? -eq 1 → ok
```
