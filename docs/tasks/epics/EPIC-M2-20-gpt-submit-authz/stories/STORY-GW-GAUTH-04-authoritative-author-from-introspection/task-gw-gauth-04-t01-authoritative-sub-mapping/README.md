# task-gw-gauth-04-t01

## Meta
- **Story:** [STORY-GW-GAUTH-04](../STORY-GW-GAUTH-04-authoritative-author-from-introspection.md)
- **Type:** implement
- **Status:** 🔵 Done
- **Package:** pkg-000042
- **Skill declared:** python-pro
- **Depends on:** GW-GAUTH-02/03 (Done)

## Purpose
Зафиксировать mapping policy: при успешном introspection `IntrospectionResult.sub` → `StoryRecord.submitter_external_user_id` (истина = `sub`); политика `submitter_identity_issuer` — из payload или фиксированный issuer identity (config), без новой колонки Story Store.

## Code Facts
- `IntrospectionResult` — [`introspection_client.py:16-19`](../../../../../../../src/core/identity/introspection_client.py)
- Persist сейчас из payload — [`services.py:237-238`](../../../../../../../src/core/application/services.py)
- Story columns — [`domain/contracts.py:48-49`](../../../../../../../src/core/domain/contracts.py)
- Intake `Submitter` — [`intake/contracts.py:25-27`](../../../../../../../src/core/intake/contracts.py)

## Acceptance / DoD
- Traces parent AC #1: helper resolves authoritative `submitter_external_user_id` from introspection `sub`
- Mapping documented in module docstring; no Story Store schema change
- `identity_issuer` policy explicit (payload vs `IDENTITY_*` base URL)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- New module e.g. [`src/core/identity/authoritative_submitter.py`](../../../../../../../src/core/identity/authoritative_submitter.py) or [`src/core/application/authoritative_author.py`](../../../../../../../src/core/application/authoritative_author.py)
- Export from [`src/core/identity/__init__.py`](../../../../../../../src/core/identity/__init__.py) if public API

## Out of scope
- Plumbing introspection from request state (T02)
- Mismatch logging (T03)
- req-19 doc edits (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'authoritative|IntrospectionResult' src/core/identity/ src/core/application/
```
