# task-gw-gauth-03-t06

## Meta
- **Story:** [STORY-GW-GAUTH-03](../STORY-GW-GAUTH-03-verification-gate-403.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000041
- **Skill declared:** python-pro
- **Depends on:** T01–T05

## Purpose
Story acceptance gate: all parent AC verified; verification gate wired on verify-gated public-content writes.

## Code Facts
- Parent AC — [`STORY-GW-GAUTH-03-verification-gate-403.md`](../STORY-GW-GAUTH-03-verification-gate-403.md) §Acceptance Criteria
- Active pkg — [`pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml`](../../../../../../gateway-active-packages/pkg-000041-20260625-gw-gauth-03-verification-gate-403.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- OAUTH-04 SSOT — [`09-gateway-expectations.md`](../../../../../../../../../doge-identity-service/docs/runtime-docs/09-gateway-expectations.md)

## Acceptance / DoD
- All 6 parent AC PASS in [`story-acceptance-gate-STORY-GW-GAUTH-03.md`](./story-acceptance-gate-STORY-GW-GAUTH-03.md)
- `builder_resolve_queue --project gateway --verify` → ok 6 paths
- T01–T05 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-GAUTH-03.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- GW-GAUTH-04 implementation
- GPT Actions OpenAPI update

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_03_verification_gate_contract.py
```
