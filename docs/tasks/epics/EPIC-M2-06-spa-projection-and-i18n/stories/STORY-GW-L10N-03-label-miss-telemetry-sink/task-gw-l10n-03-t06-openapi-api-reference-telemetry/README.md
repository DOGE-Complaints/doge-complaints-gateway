# task-gw-l10n-03-t06

## Meta
- **Story:** [STORY-GW-L10N-03](../STORY-GW-L10N-03-label-miss-telemetry-sink.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000029
- **Skill declared:** python-pro

## Purpose
Document `POST /telemetry/label-misses` in OpenAPI and API_REFERENCE: anonymity, no PII, 202 semantics, payload schema.

## Code Facts
- `docs/runtime-docs/api-reference/openapi.yaml` — no `telemetry` paths (grep → 0)
- `docs/runtime-docs/api-reference/API_REFERENCE.md` — no telemetry section
- Story «Предлагаемый контракт» — canonical payload/response shape

## Acceptance / DoD
- Traces: AC5 (openapi/API_REFERENCE + анонимность)
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `docs/runtime-docs/api-reference/openapi.yaml` — path + schemas
- `docs/runtime-docs/api-reference/API_REFERENCE.md` — new section (telemetry)

## Verification commands
```bash
# Manual: schema matches T03 handler request/response
grep -n telemetry docs/runtime-docs/api-reference/openapi.yaml
grep -n label-miss docs/runtime-docs/api-reference/API_REFERENCE.md
```
