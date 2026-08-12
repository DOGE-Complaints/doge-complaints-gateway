# task-gw-gauth-04-t03

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** T02

## Purpose
Контракт расхождения: `payload.submitter.external_user_id != introspected sub` → persist с **sub**; structured log event (e.g. `story_intake_submitter_mismatch`) с claimed vs authoritative ids — опциональное хранение claimed submitter только в логах (backlog open question).

## Code Facts
- Payload submitter parse — [`intake/contracts.py:223-227`](../../../../../../../src/core/intake/contracts.py)
- Intake log uses payload id — [`handlers.py:170`](../../../../../../../src/core/api/handlers.py)
- `log_api_event` pattern — [`handlers.py:165-178`](../../../../../../../src/core/api/handlers.py)

## Acceptance / DoD
- Traces parent AC #2: mismatch resolves in favor of `sub` at persist
- Traces parent AC #2: contract documented (module docstring or runtime-docs note)
- On mismatch: structured log includes `claimed_external_user_id` and `authoritative_sub` (no PII beyond opaque ids)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- T02 path in [`handlers.py`](../../../../../../../src/core/api/handlers.py) and/or [`services.py`](../../../../../../../src/core/application/services.py)
- Optional brief in [`docs/runtime-docs/`](../../../../../../../docs/runtime-docs/) if needed for contract visibility

## Out of scope
- New DB column for claimed submitter audit
- req-19 full rewrite (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'submitter_mismatch|claimed_external' src/core/
```
