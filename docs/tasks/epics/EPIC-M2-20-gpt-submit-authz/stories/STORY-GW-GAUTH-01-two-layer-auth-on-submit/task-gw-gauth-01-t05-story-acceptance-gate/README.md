# task-gw-gauth-01-t05

## Meta
- **Story:** [STORY-GW-GAUTH-01](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md)
- **Type:** tests
- **Status:** ⚪ Todo
- **Package:** pkg-000039
- **Skill declared:** python-pro
- **Depends on:** T01–T04

## Purpose
Story acceptance gate: all parent AC verified; two-layer service auth on public content writes complete.

## Code Facts
- Parent AC — [`STORY-GW-GAUTH-01-two-layer-auth-on-submit.md`](../STORY-GW-GAUTH-01-two-layer-auth-on-submit.md) §Acceptance Criteria
- Active pkg — [`pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml`](../../../../../../gateway-active-packages/pkg-000039-20260625-gw-gauth-01-two-layer-auth-on-submit.yaml)
- Gate template — [`story-acceptance-gate-template.md`](../../../../../../../../docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md)
- Identity SSOT — [`04-security §A`](../../../../../../../../../doge-identity-service/docs/runtime-docs/04-security.md)

## Acceptance / DoD
- All 5 parent AC PASS in [`story-acceptance-gate-STORY-GW-GAUTH-01.md`](./story-acceptance-gate-STORY-GW-GAUTH-01.md)
- `builder_resolve_queue --project gateway --verify` → ok 5 paths
- T01–T04 acceptance artifacts referenced in gate
- BULLRUN phases complete
- Acceptance file signed (Date only after live verify in P3/P6)

## Where to change
- `story-acceptance-gate-STORY-GW-GAUTH-01.md` (gate Date after live verify only)
- `bullrun-launch-index.md` story row

## Out of scope
- GW-GAUTH-02..04 implementation
- GPT Actions OpenAPI update

## Verification commands
```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project gateway --verify
cd doge-complaints-gateway && PYTHONPATH=src:. python3 -m pytest -q tests/test_gw_gauth_01_two_layer_auth_contract.py
```
