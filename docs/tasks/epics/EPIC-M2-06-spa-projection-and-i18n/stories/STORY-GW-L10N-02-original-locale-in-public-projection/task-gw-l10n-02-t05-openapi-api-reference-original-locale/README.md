# task-gw-l10n-02-t05

## Meta
- **Story:** [STORY-GW-L10N-02](../STORY-GW-L10N-02-original-locale-in-public-projection.md)
- **Type:** docs
- **Status:** 🟢 Done
- **Package:** pkg-000028
- **Skill declared:** python-pro

## Purpose
Описать `original_locale` в `openapi.yaml` и `API_REFERENCE.md` §6/§7 — заменить «planned» на фактическую схему.

## Code Facts
- `docs/runtime-docs/api-reference/openapi.yaml`
- `docs/runtime-docs/api-reference/API_REFERENCE.md` §6/§7

## Acceptance / DoD
- Traces: AC4
- BULLRUN phases complete
- Acceptance file signed

## Where to change
- `openapi.yaml` — Issue schema `original_locale`
- `API_REFERENCE.md` — list + get response fields

## Verification commands
```bash
grep `original_locale` in both files
```
