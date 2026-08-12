# task-gw-draft-04-t02-introspection-result-module-extract

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** refactor
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T01 (inventory)

## Purpose
Backlog T02: вынести `IntrospectionResult` в нейтральный модуль `src/core/identity/introspection_result.py`; переключить импорты `verification_gate`, `authoritative_submitter`, `me_client` на него. **Не** удалять `introspection_client.py` yet (T03).

## Code Facts
- Value object today — [`introspection_client.py:16-19`](../../../../../../../src/core/identity/introspection_client.py#L16)
- Consumers — [`verification_gate.py:5`](../../../../../../../src/core/identity/verification_gate.py#L5), [`authoritative_submitter.py:7`](../../../../../../../src/core/identity/authoritative_submitter.py#L7), [`me_client.py`](../../../../../../../src/core/identity/me_client.py)
- GW-DRAFT-02 submit path uses `IntrospectionResult` via `/me` — must stay green

## Acceptance / DoD
- Traces parent AC #2: `IntrospectionResult` works after extract
- New module `introspection_result.py` with frozen dataclass/value object
- All KEEP-module imports updated; no circular imports
- `introspection_client.py` still exists (re-exports or imports from new module until T03)
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- `src/core/identity/introspection_result.py` (new)
- [`src/core/identity/verification_gate.py`](../../../../../../../src/core/identity/verification_gate.py)
- [`src/core/identity/authoritative_submitter.py`](../../../../../../../src/core/identity/authoritative_submitter.py)
- [`src/core/identity/me_client.py`](../../../../../../../src/core/identity/me_client.py)
- [`src/core/identity/__init__.py`](../../../../../../../src/core/identity/__init__.py)

## Out of scope
Removing `IdentityIntrospectionClient` (T03); route deps (T04)

## Verification commands
```bash
cd doge-complaints-gateway && rg 'from core.identity.introspection_result|IntrospectionResult' src/core/identity/
pytest tests/test_gw_draft_02_story_draft_submit_contract.py -q
```
