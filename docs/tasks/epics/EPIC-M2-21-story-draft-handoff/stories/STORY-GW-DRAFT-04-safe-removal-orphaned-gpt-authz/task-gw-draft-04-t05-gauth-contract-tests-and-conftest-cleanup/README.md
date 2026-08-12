# task-gw-draft-04-t05-gauth-contract-tests-and-conftest-cleanup

## Meta
- **Story:** [STORY-GW-DRAFT-04](../STORY-GW-DRAFT-04-safe-removal-orphaned-gpt-authz.md)
- **Type:** tests
- **Status:** 🟢 Done
- **Package:** pkg-000046
- **Skill declared:** python-pro
- **Depends on:** T04

## Purpose
Backlog T04 (part 1): обновить [`tests/conftest.py`](../../../../../../../tests/conftest.py) — убрать auto GAUTH headers + mock `IdentityIntrospectionClient.introspect`; пересмотреть `test_gw_gauth_02_*` / `test_gw_gauth_03_*` — сохранить gate/author coverage, удалить OAuth-introspect-specific assertions.

## Code Facts
- Conftest GAUTH hooks — [`tests/conftest.py`](../../../../../../../tests/conftest.py)
- OAuth contract tests — [`test_gw_gauth_02_user_token_introspection_contract.py`](../../../../../../../tests/test_gw_gauth_02_user_token_introspection_contract.py), [`test_gw_gauth_03_verification_gate_contract.py`](../../../../../../../tests/test_gw_gauth_03_verification_gate_contract.py)
- KEEP coverage — GW-DRAFT-02 [`test_gw_draft_02_*`](../../../../../../../tests/), GAUTH-04 author tests
- Baseline — 574 unit (pre-removal)

## Acceptance / DoD
- Traces parent AC #3: suite green **after** removal; not by deleting live gate/author tests
- Conftest no longer injects `X-User-Token` / mocks removed client
- `test_gw_gauth_03` gate logic tests still cover `evaluate_verification_gate` where applicable
- GW-DRAFT-02 draft submit + GET auth contract tests pass
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3)

## Where to change
- [`tests/conftest.py`](../../../../../../../tests/conftest.py)
- [`tests/test_gw_gauth_02_user_token_introspection_contract.py`](../../../../../../../tests/test_gw_gauth_02_user_token_introspection_contract.py)
- [`tests/test_gw_gauth_03_verification_gate_contract.py`](../../../../../../../tests/test_gw_gauth_03_verification_gate_contract.py)

## Out of scope
`simulation_runner.py` (T06); prod code (T02–T04)

## Verification commands
```bash
cd doge-complaints-gateway && pytest tests/test_gw_gauth_03_verification_gate_contract.py tests/test_gw_gauth_04_authoritative_author_contract.py tests/test_gw_draft_02_story_draft_submit_contract.py tests/test_gw_draft_02_get_auth_contract.py -q
```
