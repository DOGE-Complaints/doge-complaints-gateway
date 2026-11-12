# acceptance-verification — GW-SSR-03 t06

- **Result:** PASS
- **Date:** 2026-08-28T14:13:05Z
- **Package:** pkg-000063

## Evidence

`SchemaBinding` on existing `StoryIntakeRequest` / `StoryDraftStashRequest` in `openapi.yaml`; `API_REFERENCE.md` sidecar section; `GET /tallinn/issues` stays; no new HTTP path.

## Commands

```bash
rg -n "schema_binding" doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md
rg -n '"/tallinn/issues"' doge-complaints-gateway/src/core/api/asgi_app.py
```
