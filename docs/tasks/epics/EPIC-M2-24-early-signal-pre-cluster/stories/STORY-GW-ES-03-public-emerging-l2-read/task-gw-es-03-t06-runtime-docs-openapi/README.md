# task-gw-es-03-t06-runtime-docs-openapi

## Meta
- **Story:** [STORY-GW-ES-03](../STORY-GW-ES-03-public-emerging-l2-read.md)
- **Type:** docs
- **Status:** 🔵 Done (Awaiting Commits)
- **Package:** pkg-000060
- **Skill declared:** python-pro
- **Depends on:** T00 Done; T03
- **Scaffolded:** 2026-08-10T12:06:12Z

## Purpose
OpenAPI + API_REFERENCE для Emerging L2; explicit «not Issues» note; optional EarlySignal tag reuse; cross-link gap / TASK-ES-04 if seam touched.

## Code Facts
- OpenAPI — [`openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml) (Pulse + `EarlySignal` tag from ES-02)
- API_REFERENCE — [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)
- Path SSOT — T00 REQ/ADR only

## Acceptance / DoD
- [ ] Traces AC: MVP rule documented in runtime-docs; Emerging L2 path+payload mirrored
- [ ] OpenAPI path operation + «not Issues» description
- [ ] API_REFERENCE section for Emerging L2
- [ ] No invented path if T00 incomplete
- [ ] BULLRUN phases complete
- [ ] `acceptance-verification-gw-es-03-t06.md` signed (Date post P3 verify only)

## Where to change
- [`openapi.yaml`](../../../../../../../runtime-docs/api-reference/openapi.yaml)
- [`API_REFERENCE.md`](../../../../../../../runtime-docs/api-reference/API_REFERENCE.md)

## Out of scope
- Handler implementation (T03); spa-15 layout

## Verification commands
```bash
rg -n 'Emerging|emerging|not Issues' doge-complaints-gateway/docs/runtime-docs/api-reference/openapi.yaml doge-complaints-gateway/docs/runtime-docs/api-reference/API_REFERENCE.md
```
