# task-gw-draft-06-t02-runtime-docs-remove-public-intake-path

## Meta
- **Story:** [STORY-GW-DRAFT-06](../STORY-GW-DRAFT-06-remove-legacy-intake-stories-route.md)
- **Type:** docs
- **Status:** ⚪ Todo
- **Package:** pkg-000050
- **Skill declared:** python-pro
- **Depends on:** T01

## Purpose
Backlog T02: remove public `POST /intake/stories` from runtime OpenAPI, API reference, security SSOT, architecture, and persistence docs — single GPT write path = story-drafts.

## Code Facts
- OpenAPI path — [`openapi.yaml:655`](../../../../../../../runtime-docs/api-reference/openapi.yaml) `/intake/stories`
- API reference — [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md) § intake
- Security SSOT — [`security-env-api-access.md`](../../../../../../../runtime-docs/security-env-api-access.md) dual-path / legacy intake rows
- Architecture — [`architecture-and-layers-as-is.md:50`](../../../../../../../runtime-docs/architecture-and-layers-as-is.md) route table
- Persistence — [`story-persistence-model.md`](../../../../../../../runtime-docs/story-persistence-model.md) intake diagram refs

## Acceptance / DoD
- [ ] Traces parent AC #4: OpenAPI has no public `POST /intake/stories`
- [ ] API_REFERENCE + security-env describe GPT write via `/story-drafts` only
- [ ] Architecture + persistence docs aligned (no public intake HTTP path)
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-06-t02.md`](./acceptance-verification-gw-draft-06-t02.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml`
- `doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md`
- `doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md`
- `doge-complaints-gateway/docs/runtime-docs/architecture-and-layers-as-is.md`
- `doge-complaints-gateway/docs/runtime-docs/story-persistence-model.md`

## Out of scope
- Code route removal (T01); tests (T04–T05)
- Solution architecture modules (unless grep finds stale `/intake/stories` in runtime-docs only)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'POST /intake/stories|/intake/stories' docs/runtime-docs/api-reference/openapi.yaml || test $? -eq 1
cd doge-complaints-gateway && rg '/intake/stories' docs/runtime-docs/api-reference/API_REFERENCE.md docs/runtime-docs/security-env-api-access.md
```
