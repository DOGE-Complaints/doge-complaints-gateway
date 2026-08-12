# task-gw-gauth-02-t06

## Meta
- **Story:** [STORY-GW-GAUTH-02](../STORY-GW-GAUTH-02-user-token-introspection.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000040
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Story acceptance gate: all parent AC verified; gateway introspection client wired on verify-gated public-content writes.

## Code Facts
- Parent AC — [`STORY-GW-GAUTH-02-user-token-introspection.md`](../STORY-GW-GAUTH-02-user-token-introspection.md) §Acceptance Criteria
- Active pkg — [`pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml`](../../../../../../gateway-active-packages/pkg-000040-20260625-gw-gauth-02-user-token-introspection.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Identity SSOT — [`04-security §A`](../../../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md)

## Acceptance / DoD
- All 5 parent AC PASS in [`story-acceptance-gate-STORY-GW-GAUTH-02.md`](./story-acceptance-gate-STORY-GW-GAUTH-02.md)
- `builder_resolve_queue --project gateway --verify` → ok 6 paths
- T01–T05 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-GAUTH-02.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- GW-GAUTH-03/04 implementation
- GPT Actions OpenAPI update

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_02_user_token_introspection_contract.py
```
