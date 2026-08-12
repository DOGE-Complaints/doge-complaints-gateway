# task-gw-draft-05-t06-runtime-docs-dual-path-ssot

## Meta
- **Story:** [STORY-GW-DRAFT-05](../STORY-GW-DRAFT-05-dual-intake-contract-stash-vs-submit.md)
- **Type:** docs
- **Status:** ⚪ Todo
- **Package:** pkg-000049
- **Skill declared:** python-pro
- **Depends on:** T05

## Purpose
Backlog T06: sync runtime SSOT — dual path (GPT stash without submitter vs browser submit with authoritative submitter); fix stale «always requires submitter» and «stash = StoryIntakeRequest» claims.

## Code Facts
- API reference §6.8 — [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- Security §1.1 stale — [`security-env-api-access.md`](../../../../../../../runtime-docs/security-env-api-access.md)
- Architecture L51 stale — [`architecture-and-layers-as-is.md`](../../../../../../../runtime-docs/architecture-and-layers-as-is.md)
- Persistence model — [`story-persistence-model.md`](../../../../../../../runtime-docs/story-persistence-model.md)

## Acceptance / DoD
- [ ] Traces parent AC #5: security + architecture describe two request contracts (stash vs intake bridge)
- [ ] API_REFERENCE §6.8, architecture §4.1, story-persistence-model updated for stash shape without submitter
- [ ] BULLRUN phases complete
- [ ] [`acceptance-verification-gw-draft-05-t06.md`](./acceptance-verification-gw-draft-05-t06.md) signed (Date post P3 verify only)

## Where to change
- `doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md`
- `doge-complaints-gateway/docs/runtime-docs/security-env-api-access.md`
- `doge-complaints-gateway/docs/runtime-docs/architecture-and-layers-as-is.md`
- `doge-complaints-gateway/docs/runtime-docs/story-persistence-model.md`

## Out of scope
- GPT UI instructions; identity canon; `POST /intake/stories` removal → GW-DRAFT-06

## Verification commands
```bash
cd doge-complaints-gateway && rg 'StoryDraftStashRequest|stash vs|без submitter' docs/runtime-docs/
cd doge-complaints-gateway && rg 'всегда требует submitter' docs/runtime-docs/security-env-api-access.md || test $? -eq 1
```
